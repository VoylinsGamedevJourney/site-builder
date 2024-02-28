import os
import json
import readline

# Add categorie of big adventure to fitting articles
# Divide First Japan trip into a category and separate articles.

# Replace site-title, site-description, and site-tags for posts by different values compared to pages
# For tags append ', {post-tags}'

# For pages, remove {{ author }}, for posts replace by:
# <meta name="author" content="{{ author-name }}">
# author name needs to come from site_data "default-author",
# but check if an author variable was given in post info.


# For posts content, replace urls 'https://***' by a <a> unless the url is given as [url](https://***)
# Could be achieved by checking for spaces before and after url
# When link is a youtube video, make it embedded if not []() format
# Also turn [URl](https://***) into a

# Go line by line, normal text should be <p>
# Headers should be set correctly

# For {{ post-thumb }} if video url is given, don't show the thumb but show video instead

# Change '1.' lines to a numbered list and
# '-' to unordered lists

# an RSS feed

# a sitemap

def main():
  with open(json_file, 'r') as file:
    site_data = json.load(file)
  


if __name__ == "__main__":
  main()
