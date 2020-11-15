import json
import re
from urllib.parse import urlparse, parse_qs

import requests
from bs4 import BeautifulSoup

town_without_page_list = []


def search_cadastral_code_in_pages(page_list):
    for url in page_list:
        if "redlink" in url:
            params = parse_qs(urlparse(url).query)
            if "title" in params:
                town_title = params['title'][0].replace("_", " ").replace("%27", "'")
                town_without_page_list.append(town_title)
        else:
            resp = requests.get(url=url)
            soup = BeautifulSoup(resp.content, 'html.parser')

            td = soup.select('th')
            town_name = td[0].contents[0]

            for name, val in zip(td, td[1:]):
                a = name.find_next('a')
                if a.has_attr('title') and "catastale" in a['title']:
                    code = name.parent.find_next('td').text.replace('\n', '')
                    province_node = name.parent.find_next('tr').find('td')
                    province = province_node.text.replace('\n', '') if province_node is not None else "-"
                    province = province if len(province) == 2 else "-"
                    print(town_name, code, province)
                    break


def search_cadastral_code_of_town(town_name):
    response = requests.get("https://calcolocf.com/codice-catastale.html?comune={}".format(town_name))
    soup = BeautifulSoup(response.content, 'html.parser')
    cadastral_code = soup.find("div", {"class": "codice_catastale"})
    town_code = soup.find("a", href=re.compile("comune="))
    if cadastral_code is not None:
        return cadastral_code.text, \
               town_code.text.replace(town_name, "").replace(" ", "").replace("(", "").replace(")", "")
    return "", ""


def wikipedia_scraper():
    min_year = 1930
    base_url = "https://it.wikipedia.org"
    soup = BeautifulSoup(open("comunisoppressi.html"), "html.parser")
    li_list = soup.find_all('li')
    for li in li_list:
        links = li.findAll('a', href=True)
        source_town_pages = []
        target_town_pages = []
        i = 0

        while i < len(links) and not links[i]['title'].isnumeric():
            source_town_pages.append(base_url + links[i]['href'])
            i = i + 1

        if i < len(links):
            year = links[i]['title']
            if int(year) >= min_year:
                i = i + 1
                while i < len(links) and "cite_note" not in links[i]['href'] and not links[i]['title'].isnumeric():
                    target_town_pages.append(base_url + links[i]['href'])
                    i = i + 1

                search_cadastral_code_in_pages(source_town_pages)
                search_cadastral_code_in_pages(target_town_pages)

                print(links)
    print(town_without_page_list)


def print_to_json(output_list):
    with open('data.json', 'w') as output:
        json.dump(output_list, output)


def main():
    wikipedia_scraper()
    print(town_without_page_list)

    result_list = []
    for town in town_without_page_list:
        cadastral, code = search_cadastral_code_of_town(town)
        result_list.append({
            "cc": cadastral,
            "id": town,
            "p": code
        })
    print_to_json(result_list)


if __name__ == '__main__':
    main()
