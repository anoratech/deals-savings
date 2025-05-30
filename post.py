import os
import requests
import frontmatter


def convert_image_url(image_path):
    if image_path.startswith("img/"):
        return f"https://slicksavers.com/{image_path}"
    return image_path  # Return unchanged if it doesn't match

# Facebook API settings
PAGE_ID = "100735221776559"
ACCESS_TOKEN = "EAAEk6BgYXGUBO0w4kedg8ZAjbZCUfx6RZCvFVxx4mizdJXJOlkjS0pianZC1zDV2yOtFZB1kkelCexvcLCtI0pguhK2ozSxNIFIQvZB9csxZCLHIBZB8ZAwZBW6A2crPsaGKc6ILHEX0cya68ZBSMIcZBGXl8zNMd6JWA6eZAFdZA1GI5JgWpnKfATsIzZAXhZBptDCiriLCYq1ZCnekZD"
GRAPH_API_URL = f"https://graph.facebook.com/v23.0/100735221776559/feed"



# Get new content filename from GitHub Actions
new_content_file = os.getenv("NEW_CONTENT")
#new_content_file = "bed.md"

if not new_content_file:
    print("No new content detected.")
    exit()

# Read Hugo Markdown file
with open(new_content_file, "r", encoding="utf-8") as file:
    post = frontmatter.load(file)

title = post.get("title")
description = post.get("description")
image_url = convert_image_url(post.get("image"))
 
# Prepare post message
post_data = f"**{title}**\n{description}\n{post.content}"
 

GRAPH_API_URL = f"https://graph.facebook.com/{PAGE_ID}/photos"

response = requests.post(
    GRAPH_API_URL,
    params={"caption": post_data, "url": image_url, "access_token": ACCESS_TOKEN},
)


# Print response
print(response.json())







