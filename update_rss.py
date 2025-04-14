import os
import re
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import feedparser

feeds = [
    {
        "name": "PatchnotesEnhanced",
        "file": "PatchnotesEnhancedRSS.rss",
        "start_marker": "<!-- RSS-ENHANCED-START -->",
        "end_marker": "<!-- RSS-ENHANCED-END -->",
        "title_format": "[{title}]({link})"
    },
    {
        "name": "PatchnotesLegacy",
        "file": "PatchnotesLegacyRSS.rss",
        "start_marker": "<!-- RSS-LEGACY-START -->",
        "end_marker": "<!-- RSS-LEGACY-END -->",
        "title_format": "[{title}]({link})"
    },
    {
        "name": "CodeWalker",
        "url": "https://github.com/dexyfex/CodeWalker/releases.atom",
        "start_marker": "<!-- RSS-CODEWALKER-START -->",
        "end_marker": "<!-- RSS-CODEWALKER-END -->",
        "title_format": "[CodeWalker update for {published}]({link})"
    },
    {
        "name": "SHVDN Nightly",
        "url": "https://github.com/scripthookvdotnet/scripthookvdotnet-nightly/releases.atom",
        "start_marker": "<!-- RSS-SHVDN-START -->",
        "end_marker": "<!-- RSS-SHVDN-END -->",
        "title_format": "[SHVDN Nightly update for {published}]({link})"
    }
]

# Load the README
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

# Process each feed
for feed_info in feeds:
    try:
        entries = []

        if "file" in feed_info:
            root = ET.parse(feed_info["file"]).getroot()
            for item in root.findall(".//item"):
                title = item.findtext("title", "No Title")
                pub_date = item.findtext("pubDate", "")
                link = item.findtext("link", "#")
                try:
                    published = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %Z").strftime("%d %B %Y")
                except Exception:
                    published = "Unknown date"
                entries.append(feed_info["title_format"].format(title=title, published=published, link=link))

        elif "url" in feed_info:
            feed = feedparser.parse(feed_info["url"])
            for entry in feed.entries[:5]:
                title = entry.title
                link = entry.link
                updated = entry.get("updated", "")
                try:
                    published = datetime.strptime(updated, "%Y-%m-%dT%H:%M:%SZ").strftime("%d %B %Y")
                except Exception:
                    published = "Unknown date"
                entries.append(feed_info["title_format"].format(title=title, published=published, link=link))

        if not entries:
            print(f"No entries found for {feed_info['name']}")
            continue

        start = content.find(feed_info["start_marker"])
        end = content.find(feed_info["end_marker"])

        if start == -1 or end == -1:
            raise ValueError(f"Markers not found for section '{feed_info['name']}'")

        content = (
            content[:start + len(feed_info["start_marker"])] + "\n"
            + "\n".join(f"- {entry}" for entry in entries) + "\n"
            + content[end:]
        )

        print(f"Updated section for {feed_info['name']} with {len(entries)} entries.")

    except Exception as e:
        print(f"Error processing feed '{feed_info['name']}': {e}")

# Save the updated README
with open("README.md", "w", encoding="utf-8") as f:
    f.write(content)
