import requests
from bs4 import BeautifulSoup


def main():
    base_url = "https://it.wikipedia.org"

    response = requests.get(
        url="https://it.wikipedia.org/wiki/Comuni_d%27Italia_soppressi"
    )

    # soup = BeautifulSoup(response.content, 'html.parser')
    soup = BeautifulSoup(open("comunisoppressi.html"), "html.parser")

    li_list = soup.find_all('li')
    for li in li_list:
        links = li.findAll('a', href=True)
        source_town_pages = []
        target_town_pages = []
        i = 0
        while i < len(links) and not links[i]['title'].isnumeric():
            source_town_pages.append(base_url + links[i]['href'])
            i = i+1
        if i < len(links):
            year = links[i]['title']
            i = i+1
            while i < len(links) and not "cite_note" in links[i]['href'] and not links[i]['title'].isnumeric():
                target_town_pages.append(base_url + links[i]['href'])
                i = i+1
        print(links)


if __name__ == '__main__':
    main()
