import os
import readline


def get_user_input(prompt):
  return input(prompt).strip()


def create_folder_structure():
  print("Creating folder structure ...")
  for folder in [
      "_site", 
      "toolbox", "toolbox/templates", "toolbox/blocks",
      "assets", "assets/thumbs",
      "posts"]:
    os.makedirs(folder, exist_ok=True)
  

def create_css_file(path):
  print("Creating CSS file ...")
  with open(path, "w") as f:
    lines = [
      '/* This is your main CSS file */',
      '/* When updating this, add 1 filename number */)']
    f.writelines(line + '\n' for line in lines)
  

def create_site_info(path):
  print("Creating site info ...")
  with open(path, "w") as f:
    site_title = get_user_input("Enter site title: ")
    site_desc = get_user_input("Enter site description: ")
    site_url = get_user_input("Enter site url: ")
    site_tags = get_user_input("Enter site tags (comma separated): ")
    site_author = get_user_input("Enter main author: ")

    site_cat_string = ""
    value = get_user_input("Enter main category: ")
    while value != "":
      value = get_user_input("Add new category (leave empty to skip): ")
      site_cat_string += value + ', '

    lines = []
    lines.append('{')
    lines.append('  "site_title": "' + site_title + '",')
    lines.append('  "site_description": "' + site_desc + '",')
    lines.append('  "site-address": "' + site_url + '",')
    lines.append('  "site-tags": "' + site_tags + '",')
    lines.append('  "default-author": "' + site_author + '",')
    lines.append('  "categories": [' + site_cat_string + ']')
    lines.append('}')
    f.writelines(line + '\n' for line in lines)
    
    
if __name__ == "__main__":
  css_path = "assets/style_001.css"
  site_info_path = "site_info.json"

  print("--== Generating site template ==--")
  if os.getcwd().endswith("site-builder"):
    os.chdir("..")
  
  create_folder_structure()
  if not os.path.isfile(css_path):
    create_css_file(css_path)
  if not os.path.isfile(site_info_path):
    create_site_info(site_info_path)