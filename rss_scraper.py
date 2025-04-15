import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)

def parse_date(text):
    formats = ["%d %b %Y", "%B %d, %Y", "%d/%m/%y", "%d/%m/%Y"]
    for fmt in formats:
        try:
            return datetime.strptime(text.strip(), fmt)
        except ValueError:
            continue
    return None

def fetch_scripthookv():
    url = "http://www.dev-c.com/gtav/scripthookv/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    date_text = soup.find("td", string=lambda s: s and "Released" in s)
    version_text = soup.find("td", string=lambda s: s and "Version" in s)

    if not date_text:
        return []

    date_node = date_text.find_next_sibling("td")
    version_node = version_text.find_next_sibling("td") if version_text else None

    date = parse_date(date_node.text) if date_node else None
    version = version_node.text.strip() if version_node else "Unknown"

    if date:
        return [f"- [ScriptHookV {version} (Released {date.strftime('%d %b %Y')})](http://www.dev-c.com/gtav/scripthookv/)"]
    return []

def fetch_openrpf():
    url = "https://www.gta5-mods.com/tools/openrpf-openiv-asi-for-gta-v-enhanced"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    versions = []

    all_versions = soup.find("div", class_="download-list")
    if all_versions:
        for entry in all_versions.find_all("li")[:5]:
            date_tag = entry.find("span", class_="date")
            version_tag = entry.find("strong")
            if date_tag and version_tag:
                date = parse_date(date_tag.text)
                version = version_tag.text.strip()
                if date:
                    versions.append(f"- [OpenRPF {version} (Released {date.strftime('%d %b %Y')})]({url})")
    return versions

def update_readme_section(prefix, name, entries):
    start_marker = f"<!-- {prefix}-{name}-START -->"
    end_marker = f"<!-- {prefix}-{name}-END -->"

    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        raise ValueError(f"Markers not found: {start_marker} / {end_marker}")

    section = f"{start_marker}\n" + "\n".join(entries[:5]) + f"\n{end_marker}"
    updated = content[:start_idx] + section + content[end_idx + len(end_marker):]

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated)

def main():
    sections = [
        {"name": "SCRIPTHOOKV", "prefix": "RSS", "entries": fetch_scripthookv()},
        {"name": "OPENRPF", "prefix": "RSS", "entries": fetch_openrpf()},
    ]

    for section in sections:
        logging.info(f"{section['name']}: {len(section['entries'])} entries found")
        update_readme_section(section["prefix"], section["name"], section["entries"])

if __name__ == "__main__":
    main()