import os
import json
import readline


def get_user_input(prompt):
  return input(prompt).strip()


def main():
  # Get post variables
  year = get_user_input("Enter the year: ")
  month = get_user_input("Enter the month: ").zfill(2)
  day = get_user_input("Enter the day: ").zfill(2)
  title = get_user_input("Enter the title: ")
  author = get_user_input("Enter the author (leave blank for default): ")

  # Formatting title
  formatted_title = '_'.join(word.lower() for word in title.split())

  # Creating file path
  file_path = f"posts/{year}/{month}/{formatted_title}.md"

  # Getting categories
  with open("site_info.json", 'r') as file:
    site_data = json.load(file)
  print("Select category/categories (comma-separated):")
  for i, category in enumerate(site_data['categories'], 1):
    print(f"{i}. {category}")

  selected_categories = input("Enter category numbers: ").split(',')
  selected_categories = [site_data['categories'][int(index) - 1] for index in selected_categories]

  # Get other inputs
  tags = get_user_input("Enter tags (comma-separated): ")
  thumb = f"{year}/{month}/{formatted_title}.webp"
  video_url = get_user_input("Enter video URL (leave blank if none): ")
  publish_date = f"{year}/{month}/{day}"

  # Create document content
  content = f"Title: {title}\n"
  content += "Description: \n"
  content += f"Category: {', '.join(selected_categories)} \n"
  content += f"Tags: {tags}\n"
  content += f"Thumb: {thumb}\n"
  if video_url:
    content += f"Video: {video_url}\n"
  if author:
    content += f"Author: {author}\n"
  content += f"Publish date: {publish_date}\n"
  content +=  "DRAFT\n"
  content +=  "===\n"

  # Create file
  os.makedirs(os.path.dirname(file_path), exist_ok=True)
  with open(file_path, 'w') as file:
    file.write(content)

  print(f"Document created at: {file_path}")


if __name__ == "__main__":
  main()
