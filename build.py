import os
import re
import codecs
import shutil
import yaml
import markdown

cwd = os.getcwd()

dir_destination = '_site/'
dir_templates = 'toolbox/templates/'
dir_blocks = 'toolbox/blocks/'
dir_assets = 'assets/'
dir_pages = 'pages/'
dir_posts = 'posts/'

path_site_info = 'site.yaml'
path_css = ''

site_info = {}

blocks = {}
templates = {}

pages = {}
posts = {}

# TODO: Check tags for posts if correct or if they became site tags
# TODO: Check description for same reason as tags


def build():
  # Building the website starts with this function.
  global site_info
  global templates
  global cwd

  # Getting the correct working directory based on where site.yaml is saved.
  while not os.path.isfile(os.path.join(cwd, "site.yaml")):
    cwd = os.path.dirname(cwd)
    if cwd == '/':
      raise FileNotFoundError('The file "site.yaml" was not found in any parent directory.')


  # We have a file called site.yaml, where all basic site information
  # has been put such as categories, default site tags ...
  print('Loading site info ...')
  with open('site.yaml', 'r') as f:
    loader = yaml.Loader
    site_info = yaml.load(f, loader)
  for file_path in os.listdir(dir_assets): # Getting the css file path
    if file_path.startswith("style_") and file_path.endswith(".css"):
      site_info['css_file'] = '/' + file_path 
  

  # Blocks are parts which can be used inside of templates, pages and posts.
  # Default blocks are head, and footer. In future I may put other things there such
  # as Youtube video blocks, column blocks, breadcrumbs, ...
  print('Getting blocks ...')
  for file in os.listdir(dir_blocks):
    file_path = os.path.join(dir_blocks, file)
    with codecs.open(file_path, 'r', encoding='utf-8') as f:
      contents = f.read()
    blocks[file.replace('.html', '')] = contents


  # Templates are used for pages and posts mainly. This will advance to
  # category pages (and tag pages) in the future, but that's a worry for later.
  print('Getting template files ...')
  for file in os.listdir(dir_templates):
    file_path = os.path.join(dir_templates, file)
    with codecs.open(file_path, 'r', encoding='utf-8') as f:
      contents = f.read()
    for block in blocks:
      contents = contents.replace('{{ %s }}' % block, blocks[block])
    templates[file.replace('.html', '')] = _md_url_changer(contents)


  # Loading in all pages with their path, metadata and content inside of
  # their assigned variables 'pages' and 'posts'.
  _get_files('page', dir_pages)
  _get_files('post', dir_posts)


  # Removing the entire _site folder and remaking it whilst also copying over
  # the assets again. We do this to make certain no old files remain such as
  # old css files or old posts/pages we deleted. Could probably have some
  # improvements later on but works good enough for now.
  print('Cleaning up previous site')
  if os.path.isdir(dir_destination):
    shutil.rmtree(dir_destination)
    os.mkdir(dir_destination)
  print('Copying assets ...')
  shutil.copytree(dir_assets, dir_destination, dirs_exist_ok = True)


  # Generating all pages/posts and putting the final results inside of _site.
  print('Generating content ...')
  for location, content in list(pages.items()) + list(posts.items()):
    build_page(location, content[0], content[1])


def _get_files(type, dir):
  # This is a looping function used to check the pages and posts
  # folders whilst running the same function on each subfolder they come accross
  print("Getting %s files ..." % type)
  global pages
  global posts

  for file in os.listdir(dir):
    path = os.path.join(dir, file)
    if os.path.isdir(path):
      _get_files(type, path)
      continue
    with codecs.open(path, 'r', encoding='utf-8') as f:
      contents = f.read()
    if type == 'page':
      pages[path.replace(dir_pages, '')] = _get_contents_array(contents, templates[type])
    elif type == 'post':
      posts[path.replace(dir_posts, '')] = _get_contents_array(contents, templates[type])


def _get_contents_array(contents, template):
  # Splitting the metadata from the actual page content and returning
  # it in an array with value 0 being the metadata and value 1 being content.
  # We also do a bit of beautification here by removing unnecessary double enter's.
  temp_data = re.search(r'---(.*?)---', contents, re.DOTALL).group(1).split('\n')
  data = {}
  for entry in temp_data:
    if entry == '': continue # empty
    data[entry.split(':')[0]] = entry.replace(entry.split(':')[0] + ':', '').strip()
  content = contents.split("---", 2)[2].strip() # Getting the content separate from metadata
  content = _md_url_changer(content) # Changing markdown url data
  content = markdown.markdown(content) # Updating all other markdown to html
  content = template.replace('{{ content }}', content) # Adding the template data
  content = content.replace('\n\n', '\n') # Replacing double enters because not needed
  return [data, content]


def _md_url_changer(old_content):
  # Replacing markdown urls to html code with the benefit of using _blank
  # at the end of the url to make certain the target is a new tab.
  content = []
  for line in old_content.split('\n'):
    if len(re.findall(r"\[(.*?)\]\((.*?)\)", line)) > 0: # LINKS
      for text, url in re.findall(r'\[(.*?)\]\((.*?)\)', line):
        new_link = '<a %(target)shref="%(url)s">%(text)s</a>' % {
          'target': 'target="_blank" ' if url.endswith('_blank') else '',
          'url': url.rstrip('_blank') if url.endswith('_blank') else url,
          'text': text
        }
        line = line.replace('[%s](%s)' % (text, url), new_link)
    content.append(line)
  content_string = ''
  for line in content:
    content_string += line + '\n'
  return content_string


def build_page(url, metadata, content):
  # We build every page/post here. We replace all missing brackets in an order
  # which hopefully makes sense and makes certain everything gets filles in
  # correctly.
  url = url.replace('.md', '.html')

  # Filling in brackets
  brackets = re.findall(r"\{\{.*?\}\}", content)
  no_key = []
  for entry in brackets:
    key = entry.lstrip('{{ ').rstrip(' }}').strip()
    if key == 'site_title': # Site title - needs extra formatting
      content = content.replace(entry, '%(page)s - %(site)s'  % {
        'page': metadata['title'],
        'site': site_info[key]
      })
      continue
    elif key in site_info.keys(): # Site info
      value = site_info[key]
      if isinstance(value, list):
        value = ','.join(str(x) for x in value)
      content = content.replace(entry, value)
      continue
    elif key in blocks.keys(): # Blocks
      content = content.replace(entry, blocks[key])
      continue
    elif key in metadata.keys(): # Page/Post meta data
      content = content.replace(entry, metadata[key])
      continue
    elif key == 'author': #  No author present
      content = content.replace('  %s\n' % entry, '')
      continue
    elif key == 'description': # No description present
      content = content.replace(entry, site_info['site_description'])
      continue
    elif 'post_list' in key: # Post lists for all posts or specific categories
      value = key.replace('post_list', '').strip()
      data = {entry.split('=')[0]: entry.split('=')[1] for entry in value.split(' ')}
      for entry in data:
        if ',' in data[entry]:
          data[entry] = List(data[entry].split(','))
        elif entry == 'categories':
          data[entry] = [data[entry]]
      # Checking if category exist in site info
      for cat in data['categories']:
        if not cat in site_info['categories']:
          print('No site category with name "%s"!' % cat)
      
      
      
      
      #content = content.replace(entry, blocks[key])
      continue
    no_key.append(entry)
      
  if len(no_key) > 0: # In case we missed certain brackets
    print('Missed brackets in "%s":\n\t%s' % (url, no_key))

  # Writing contents to file in the correct url
  os.makedirs(dir_destination + url.replace(url.split('/')[-1], ''), exist_ok=True)
  with open(dir_destination + url, 'w', encoding='utf-8') as f:
    f.write(content)


if __name__ == "__main__":
  build()