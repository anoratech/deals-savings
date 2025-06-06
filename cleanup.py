import os
import subprocess
import frontmatter 
from datetime import datetime, timedelta

# Set directory and cutoff time
content_dir = "site/content/post/"
cutoff_date = datetime.now() - timedelta(days=365)
print(cutoff_date)

def get_last_git_commit_date(path):
    try:
        # Get last commit timestamp (epoch seconds) for the file
        output = subprocess.check_output(
            ["git", "log", "-1", "--format=%ct", path],
            universal_newlines=True
        ).strip()
        return datetime.fromtimestamp(int(output))
    except subprocess.CalledProcessError:
        print(f"⚠️ No commit history for {path}")
        return None

for root, _, files in os.walk(content_dir):
    for file in files:
        if file.endswith(".md"):
            path = os.path.join(root, file)

            #last_commit_date = get_last_git_commit_date(path)
            #print (path, "           ", last_commit_date)
            #if not last_commit_date:
                #continue

              # Read front matter for tags
            with open(path, "r", encoding="utf-8") as f:
                try:
                    post = frontmatter.load(f)
                except ValueError as e:
                    print(f"⚠️ Skipping {path} due to invalid date format: {e}")
                    continue
     
                tags = post.get("tags", "")
                print(f"Tags: {tags}  {f}")
            
           # Ensure tags are handled correctly
            if isinstance(tags, list):
                tags = [tag.lower().strip() for tag in tags]  # Clean tags
            elif isinstance(tags, str):
                tags = [tag.lower().strip() for tag in tags.split(",")]  # Convert comma-separated string to list
            else:
                tags = []  # Default to empty list if unexpected type

           # Delete if tags don't start with '2025-05' or '2025-06'
            if not any(tag.startswith(("2025-05", "2025-06")) for tag in tags):
                print(f"🗑 Deleting {path} (tags do not start with '2025-05' or '2025-06')")
                try:
                    os.remove(path)
                    print(f"✅ Successfully deleted {path}")
                except Exception as e:
                    print(f"❌ Failed to delete {path}: {e}")
            
                   
