import feedparser
import requests
from datetime import datetime

def fetch_feed_entries(path, limit=10):
    feed = feedparser.parse(path)
    entries = []

    for entry in feed.entries[:limit]:
        title = entry.get("title", "No title")
        link = entry.get("link", "#")
        if "20" in link:  # keep date if it's part of the link
            entries.append(f"- [{title}]({link})")
        else:
            entries.append(f"- [{title}]({link})")
    return entries

def fetch_codewalker_commits(limit=10):
    url = "https://api.github.com/repos/dexyfex/CodeWalker/commits"
    response = requests.get(url)
    commits = response.json()
    entries = []

    for commit in commits[:limit]:
        sha = commit["sha"][:7]
        msg = commit["commit"]["message"].split("\n")[0]
        url = commit["html_url"]
        entries.append(f"- [{msg} ({sha})]({url})")

    return entries

def fetch_shvdn_releases(limit=10):
    url = "https://api.github.com/repos/scripthookvdotnet/scripthookvdotnet-nightly/releases"
    response = requests.get(url)
    releases = response.json()
    entries = []

    for release in releases[:limit]:
        tag = release["tag_name"]
        html_url = release["html_url"]
        entries.append(f"- [SHVDN Nightly {tag}]({html_url})")

    return entries

def update_readme_section(prefix, name, entries):
    start_marker = f"<!-- {prefix}-{name}-START -->"
    end_marker = f"<!-- {prefix}-{name}-END -->"

    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        raise ValueError(f"Markers not found: {start_marker} / {end_marker}")

    section = f"{start_marker}\n" + "\n".join(entries[:10]) + f"\n{end_marker}"
    updated = content[:start_idx] + section + content[end_idx + len(end_marker):]

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated)

def main():
    sources = [
        ("ENHANCED", "RSS", "PatchnotesEnhancedRSS.rss"),
        ("LEGACY", "RSS", "PatchnotesLegacyRSS.rss"),
        ("SHVDN", "RSS", None),
        ("CODEWALKER", "RSS", None)
    ]

    for name, prefix, path in sources:
        if name == "CODEWALKER":
            entries = fetch_codewalker_commits()
        elif name == "SHVDN":
            entries = fetch_shvdn_releases()
        else:
            entries = fetch_feed_entries(path)
        print(f"Updated section for {name} with {len(entries)} entries.")
        update_readme_section(prefix, name, entries)

if __name__ == "__main__":
    main()