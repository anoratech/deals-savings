import os
import frontmatter
from datetime import datetime, timedelta

content_dir = "site/content/post/"
cutoff_date = datetime.now() - timedelta(days=365)

for root, _, files in os.walk(content_dir):
    for file in files:
        if file.endswith(".md"):
            path = os.path.join(root, file)
            try:
                post = frontmatter.load(path)
                post_date = post.get('date')

                if not post_date:
                    print(f"Skipping {path}: no date found in front matter")
                    continue

                # Ensure post_date is timezone-aware (default to UTC if naive)
                if post_date.tzinfo is None:
                    post_date = post_date.replace(tzinfo=timezone.utc)

                # Compare dates safely
                if post_date < cutoff_date:
                    print(f"Deleting {path} (dated {post_date.date()})")
                    os.remove(path)

            except Exception as e:
                print(f"Error processing {path}: {e}")
