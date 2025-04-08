import urllib.request
from datetime import datetime

from bs4 import BeautifulSoup

SINGLESTORE_EOL_PAGE_LINK = "https://docs.singlestore.com/db/latest/support/singlestore-software-end-of-life-eol-policy/"


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


def get_supported_versions(table):
    res = []
    for row in table:
        end_date_str = row[2]
        end_date = datetime.strptime(end_date_str, "%B %d, %Y")
        if end_date > datetime.today():
            res.append(row[0].split(" v", 1)[-1])

    return res


if __name__ == "__main__":
    eol_page_html = get_page_html(SINGLESTORE_EOL_PAGE_LINK)
    eol_table = get_table(eol_page_html)
    print(get_supported_versions(eol_table))
