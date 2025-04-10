import feedparser

feeds = [
    {
        "file": "PatchnotesEnhancedRSS.rss",
        "start_marker": "<!-- RSS-PATCH-START -->",
        "end_marker": "<!-- RSS-PATCH-END -->",
        "max_items": 5
    },
    {
        "file": "PatchnotesLegacyRSS.rss",
        "start_marker": "<!-- RSS-NEWS-START -->",
        "end_marker": "<!-- RSS-NEWS-END -->",
        "max_items": 5
    }
]

# Load the README
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

# Process each feed
for feed_info in feeds:
    with open(feed_info["file"], "r", encoding="utf-8") as f:
        feed_data = feedparser.parse(f.read())

    entries = [
        f"- [{entry.title}]({entry.link})"
        for entry in feed_data.entries[:feed_info["max_items"]]
    ]

    start = content.find(feed_info["start_marker"])
    end = content.find(feed_info["end_marker"])

    if start == -1 or end == -1:
        raise ValueError(f"Markers not found for {feed_info['file']}")

    content = (
        content[:start + len(feed_info["start_marker"])] + "\n"
        + "\n".join(entries) + "\n"
        + content[end:]
    )

# Save the updated README
with open("README.md", "w", encoding="utf-8") as f:
    f.write(content)