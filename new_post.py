import os
import json


def get_user_input(prompt):
  return input(prompt).strip()


def get_categories():
  with open('categories', 'r') as file:
    return [line.strip() for line in file if line.strip()]


def main():
  # Get post variables
  year = get_user_input("Enter the year: ")
  month = get_user_input("Enter the month: ").zfill(2)
  day = get_user_input("Enter the day: ")
  title = get_user_input("Enter the title: ")

  # Formating title
  formatted_title = title.replace('_', ' ').capitalize()
  format_title_path = '_'.join(word.lower() for word in title.split())

  # Creating file path
  file_path = f"posts/{year}/{month}/{format_title_path}.md"

  # Getting categories
  categories = get_categories()
  print("Select category/categories (comma-separated):")
  for i, category in enumerate(categories, 1):
    print(f"{i}. {category}")

  selected_categories = input("Enter category numbers: ").split(',')
  selected_categories = [categories[int(index) - 1] for index in selected_categories]

  # Get other inputs
  tags = get_user_input("Enter tags (comma-separated): ")
  thumb = f"assets/{year}/{month}/{title}.webp"
  video_url = get_user_input("Enter video URL (leave blank if none): ")
  publish_date = f"{year}/{month}/{day}"

  # Create document content
  content = f"Title: {formatted_title}\n"
  content += "Description: \n"
  content += f"Category: {', '.join(selected_categories)} \n"
  content += f"Tags: {tags}\n"
  content += f"Thumb: {thumb}\n"
  if video_url:
    content += f"Video: {video_url}\n"
  content += f"Publish date: {publish_date}\n"
  content +=  "DRAFT\n"
  content +=  "===\n"

  # Write to file
  os.makedirs(os.path.dirname(file_path), exist_ok=True)
  with open(file_path, 'w') as file:
    file.write(content)

  print(f"Document created at: {file_path}")


if __name__ == "__main__":
  main()
