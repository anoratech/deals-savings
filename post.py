import os
import requests
import frontmatter
from slugify import slugify


def convert_image_url(image_path):
    if not image_path.startswith("http"):
        return f"https://slicksavers.com/{image_path}"
    return image_path  # Return unchanged if it already starts with http

# Facebook API settings

ACCESS_TOKEN = "EAAEk6BgYXGUBO0w4kedg8ZAjbZCUfx6RZCvFVxx4mizdJXJOlkjS0pianZC1zDV2yOtFZB1kkelCexvcLCtI0pguhK2ozSxNIFIQvZB9csxZCLHIBZB8ZAwZBW6A2crPsaGKc6ILHEX0cya68ZBSMIcZBGXl8zNMd6JWA6eZAFdZA1GI5JgWpnKfATsIzZAXhZBptDCiriLCYq1ZCnekZD"

ACCESS_TOKEN_S = "EAAEk6BgYXGUBOw3Nc4msOR51mpfUyQBxHr7pI5SSwLwgiSZC3VOqAUQoK3KM8pdU4GiYq7fVlreD0S916nCQERYkWUZCeKeL6A32biZBoAOVOGrwTS13pX1RLc2h0S4aDJrvZBgh4xOZBDl0SzwLqSa0ZBq2AAZABgTMhxwBideakXzhRsyUuexug2JFZAXfKya9nuYZD"



# Get new content filename from GitHub Actions
new_content_file = os.getenv("NEW_CONTENT")
#new_content_file = new_content_file.replace("–", "-")

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
post_data = f"**{title}** --  {description}  --   {post.content}"
 


tag = post.get("Category", "")

if tag.lower() == "style":
    token = ACCESS_TOKEN_S
    PAGE_ID = "108657551794426"
else:
    token = ACCESS_TOKEN
    PAGE_ID = "100735221776559"

GRAPH_API_URL = f"https://graph.facebook.com/{PAGE_ID}/photos"
response = requests.post(
    GRAPH_API_URL,
    params={"caption": post_data, "url": image_url, "access_token": token},
)


# Print response
print(response.json())

# Your Telegram bot token and chat ID
BOT_TOKEN = "7996232875:AAG8NyHSLNBfUIlAe_baCq47U5Vz17lX_MM"
CHAT_ID = "-1001186001218"

CAPTION = f"{title}\n\n{description}\n\n{post.content}"

# Telegram API endpoint
URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

# Sending the image with a caption
response = requests.post(URL, data={"chat_id": CHAT_ID, "photo": image_url, "caption": CAPTION})

# Check response
if response.status_code == 200:
    print("Image sent successfully!")
else:
    print("Failed to send image:", response.text)





