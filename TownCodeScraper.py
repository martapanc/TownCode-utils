import requests
from bs4 import BeautifulSoup

def search_cadastral_code_in_pages(page_list):
    for url in page_list:
        if not "redlink" in url:
            resp = requests.get(url=url)
            page_soup = BeautifulSoup(resp.content, 'html.parser')
            tr_list = page_soup.find_all('tr')

            td = page_soup.select('th')
            for name, val in zip(td, td[1:]):
                a = name.find_next('a')
                if a.has_attr('title') and "catastale" in a['title']:
                    code = name.parent.find_next('td').text.replace('\n', '')
                    print(code)
                    break

def main():
    min_year = 1930
    base_url = "https://it.wikipedia.org"

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
            if int(year) >= min_year:
                i = i+1
                while i < len(links) and not "cite_note" in links[i]['href'] and not links[i]['title'].isnumeric():
                    target_town_pages.append(base_url + links[i]['href'])
                    i = i+1

                search_cadastral_code_in_pages(source_town_pages)
                search_cadastral_code_in_pages(target_town_pages)

                print(links)


if __name__ == '__main__':
    main()

