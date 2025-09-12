import json
import urllib.request
from datetime import datetime
import sys
from bs4 import BeautifulSoup

SINGLESTORE_EOL_PAGE_LINK = "https://docs.singlestore.com/db/latest/support/singlestore-software-end-of-life-eol-policy/"
RC_VERSIONS_LINK = "https://release.memsql.com/rc/index/singlestoredbserver/latest.json"

def format_one_decimal(version):
    parts = version.split('.')
    if len(parts) >= 2:
        return f"{parts[0]}.{parts[1]}"
    return version


def get_page_html(link):
    page = urllib.request.urlopen(link)
    return page.read()


def get_table(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find("table", class_="table-component")

    data = []
    for row in table.find("tbody").find_all("tr"):
        cells = row.find_all("td")
        values = [str.strip(cell.get_text()) for cell in cells]
        data.append(values)

    return data

def get_rc_versions():
    try:
        with urllib.request.urlopen(RC_VERSIONS_LINK) as response:
            data = json.load(response)
            version = data.get("version")
            return [format_one_decimal(version)] if version else []
    except Exception:
        return []


def get_supported_versions(table):
    res = []
    for row in table:
        end_date_str = row[2]
        end_date = datetime.strptime(end_date_str, "%B %d, %Y")
        if end_date > datetime.today():
            res.append(row[0].split(" v", 1)[-1])

    return res


if __name__ == "__main__":
    include_rc = False
    if len(sys.argv) > 1:
        include_rc = sys.argv[1].lower() == "true"
    eol_page_html = get_page_html(SINGLESTORE_EOL_PAGE_LINK)
    eol_table = get_table(eol_page_html)
    supported_versions = get_supported_versions(eol_table)
    print(f"included rc: {include_rc}")
    if include_rc:
        rc_versions = get_rc_versions()
        # Add RC versions not already in supported_versions
        supported_versions += [v for v in rc_versions if v not in supported_versions]
    supported_versions += [str(include_rc)]
    print(f"::set-output name=versions::{json.dumps(supported_versions)}")
