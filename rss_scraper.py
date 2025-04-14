import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_scripthookv():
    url = "http://www.dev-c.com/gtav/scripthookv/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.find("div", class_="post-content")
    if not content:
        return None

    lines = [line.strip() for line in content.get_text(separator="\n").splitlines() if line.strip()]
    version = next((line for line in lines if "Version" in line), None)
    date = None
    for line in lines:
        try:
            date = datetime.strptime(line.strip(), "%B %d, %Y")
            break
        except ValueError:
            continue

    if version and date:
        return f"ScriptHookV update for {date.strftime('%d %B %Y')}"
    return None

def fetch_openrpf():
    url = "https://www.gta5-mods.com/tools/openrpf-openiv-asi-for-gta-v-enhanced"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    versions = []
    changelog_section = soup.find("div", class_="description")
    if changelog_section:
        lines = changelog_section.get_text(separator="\n").splitlines()
        for line in lines:
            line = line.strip()
            if line and any(month in line for month in ["January", "February", "March", "April", "May", "June",
                                                        "July", "August", "September", "October", "November", "December"]):
                try:
                    date = datetime.strptime(line, "%B %d, %Y")
                    versions.append(f"OpenRPF update for {date.strftime('%d %B %Y')}")
                    if len(versions) >= 5:
                        break
                except ValueError:
                    continue
    return versions

def main():
    updates = []
    shv = fetch_scripthookv()
    if shv:
        updates.append(shv)

    orpf = fetch_openrpf()
    if orpf:
        updates.extend(orpf)

    # Output or save to file here if needed
    for entry in updates:
        print(entry)

if __name__ == "__main__":
    main()
