import feedparser

feeds = [
    {
        "name": "PatchnotesEnhanced",
        "file": "PatchnotesEnhancedRSS.rss",
        "start_marker": "<!-- RSS-ENHANCED-START -->",
        "end_marker": "<!-- RSS-ENHANCED-END -->",
        "title_format": "{title}"
    },
    {
        "name": "PatchnotesLegacy",
        "file": "PatchnotesLegacyRSS.rss",
        "start_marker": "<!-- RSS-LEGACY-START -->",
        "end_marker": "<!-- RSS-LEGACY-END -->",
        "title_format": "{title}"
    },
    {
        "name": "CodeWalker",
        "url": "https://github.com/dexyfex/CodeWalker/releases.atom",
        "start_marker": "<!-- RSS-CODEWALKER-START -->",
        "end_marker": "<!-- RSS-CODEWALKER-END -->",
        "title_format": "CodeWalker update for {published}"
    },
    {
        "name": "SHVDN Nightly",
        "url": "https://github.com/scripthookvdotnet/scripthookvdotnet-nightly/releases.atom",
        "start_marker": "<!-- RSS-SHVDN-START -->",
        "end_marker": "<!-- RSS-SHVDN-END -->",
        "title_format": "SHVDN Nightly update for {published}"
    }
]

# Load the README
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

# Process each feed
for feed_info in feeds:
    try:
        if "file" in feed_info:
            root = ET.parse(feed_info["file"]).getroot()
        elif "url" in feed_info:
            response = requests.get(feed_info["url"])
            response.raise_for_status()
            root = ET.fromstring(response.content)
        else:
            print(f"Skipping feed '{feed_info['name']}' (no source)")
            continue

        entries = []
        for item in root.findall(".//item"):
            title = item.findtext("title", "No Title")
            pub_date = item.findtext("pubDate", "")
            try:
                published = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %Z").strftime("%d %B %Y")
            except Exception:
                published = "Unknown date"
            entries.append(feed_info["title_format"].format(title=title, published=published))

        for entry in root.findall(".//{http://www.w3.org/2005/Atom}entry"):
            title = entry.findtext("{http://www.w3.org/2005/Atom}title", "No Title")
            updated = entry.findtext("{http://www.w3.org/2005/Atom}updated", "")
            try:
                published = datetime.strptime(updated, "%Y-%m-%dT%H:%M:%SZ").strftime("%d %B %Y")
            except Exception:
                published = "Unknown date"
            entries.append(feed_info["title_format"].format(title=title, published=published))

        entries = entries[:5]

        start = content.find(feed_info["start_marker"])
        end = content.find(feed_info["end_marker"])

        if start == -1 or end == -1:
            raise ValueError(f"Markers not found for {feed_info.get('file', feed_info.get('url', feed_info.get('name', 'unknown')))}")

        content = (
            content[:start + len(feed_info["start_marker"])] + "\n"
            + "\n".join(f"- {entry}" for entry in entries) + "\n"
            + content[end:]
        )

    except Exception as e:
        print(f"Error processing feed '{feed_info.get('name', feed_info.get('file', feed_info.get('url', 'unknown')))}': {e}")

# Save the updated README
with open("README.md", "w", encoding="utf-8") as f:
    f.write(content)
