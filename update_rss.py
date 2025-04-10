import feedparser

RSS_FILE_PATH = "PatchnotesRSS.rss"
MAX_ITEMS = 5
START_MARKER = "<!-- RSS-START -->"
END_MARKER = "<!-- RSS-END -->"

# Read and parse the local RSS feed
with open(RSS_FILE_PATH, "r", encoding="utf-8") as f:
    feed_content = f.read()
feed = feedparser.parse(feed_content)

# Format entries
rss_items = [
    f"- [{entry.title}]({entry.link})"
    for entry in feed.entries[:MAX_ITEMS]
]

# Update the README
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

start_index = content.find(START_MARKER)
end_index = content.find(END_MARKER)

if start_index == -1 or end_index == -1:
    raise ValueError("Markers not found in README.md")

new_content = (
    content[:start_index + len(START_MARKER)] + "\n"
    + "\n".join(rss_items) + "\n"
    + content[end_index:]
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_content)
