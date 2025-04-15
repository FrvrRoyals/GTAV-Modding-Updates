import requests
from bs4 import BeautifulSoup
from datetime import datetime

def parse_date_multiple_formats(line):
    formats = ["%B %d, %Y", "%d %b %Y", "%d %B %Y", "%d/%m/%Y", "%d/%m/%y", "%d %b %y", "%d %B %y"]
    for fmt in formats:
        try:
            return datetime.strptime(line, fmt)
        except ValueError:
            continue
    return None

def fetch_scripthookv():
    url = "http://www.dev-c.com/gtav/scripthookv/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.find("div", class_="post-content")
    if not content:
        print("Could not find content section on ScriptHookV page")
        return []

    lines = [line.strip() for line in content.get_text(separator="\n").splitlines() if line.strip()]
    version = next((line for line in lines if "Version" in line), None)
    date = None
    for line in lines:
        parsed_date = parse_date_multiple_formats(line)
        if parsed_date:
            date = parsed_date
            break

    if version and date:
        print(f"Found ScriptHookV version: {version}, date: {date.strftime('%d %B %Y')}")
        return [f"- ScriptHookV update for {date.strftime('%d %B %Y')}"]
    print("No valid version or date found for ScriptHookV")
    return []

def fetch_openrpf():
    url = "https://www.gta5-mods.com/tools/openrpf-openiv-asi-for-gta-v-enhanced"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    versions = []

    changelog_section = soup.find("div", class_="description")
    if not changelog_section:
        print("Could not find changelog section on OpenRPF page")
        return []

    lines = changelog_section.get_text(separator="\n").splitlines()
    for line in lines:
        line = line.strip()
        parsed_date = parse_date_multiple_formats(line)
        if parsed_date:
            versions.append(f"- OpenRPF update for {parsed_date.strftime('%d %B %Y')}")
            if len(versions) >= 5:
                break

    if versions:
        print(f"Found {len(versions)} OpenRPF updates.")
    else:
        print("No valid updates found for OpenRPF")
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

    new_section = f"{start_marker}\n" + "\n".join(entries[:5]) + f"\n{end_marker}"
    updated = content[:start_idx] + new_section + content[end_idx + len(end_marker):]

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated)
    print(f"Updated section for {name} with {len(entries[:5])} entries.")

def main():
    sections = [
        {
            "name": "SCRIPTHOOKV",
            "prefix": "RSS",
            "entries": fetch_scripthookv()
        },
        {
            "name": "OPENRPF",
            "prefix": "RSS",
            "entries": fetch_openrpf()
        }
    ]

    for section in sections:
        update_readme_section(section["prefix"], section["name"], section["entries"])

if __name__ == "__main__":
    main()