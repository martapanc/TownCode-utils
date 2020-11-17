import json
import re
from urllib.parse import urlparse, parse_qs

import requests
from bs4 import BeautifulSoup

from sort_town_list import write_json

town_without_page_list = []


def search_cadastral_code_in_pages(page_list):
    output_list = []
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
                    cadastral = name.parent.find_next('td').text.replace('\n', '')
                    province_node = name.parent.find_next('tr').find('td')
                    province = province_node.text.replace('\n', '') if province_node is not None else "-"
                    province = province if len(province) == 2 else "-"
                    print(town_name, cadastral, province)

                    output_list.append({
                        "cc": cadastral,
                        "id": town_name,
                        "p": province
                    })
                    break

    return output_list


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
    output_list = []
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

                output_list = output_list + search_cadastral_code_in_pages(source_town_pages) + search_cadastral_code_in_pages(target_town_pages)

    write_json(output_list, "soppressi")


def lombardia_scraper():
    output_list = []
    soup = BeautifulSoup(open("lombardia.html"), "html.parser")
    li_list = soup.find_all('li')
    for li in li_list:
        links = li.findAll('a', href=True)
        output_list.append(links[0]['title'])
    return output_list


def lombardia_xxi_scraper():
    output_list = []
    soup = BeautifulSoup(open("lombardia_xxi.html"), "html.parser")
    td_list = soup.find_all('td')
    for td in td_list:
        links = td.findAll('a', href=True)
        if len(links) == 0 or links[0] is None:
            continue
        town_title = links[0]['title'].split(" (")[0]
        output_list.append(town_title) if not town_title.isnumeric() else None
    return output_list


def print_to_json(output_list):
    with open('files/lombardia_soppressi.json', 'w') as output:
        json.dump(output_list, output)


def scrape_wikipedia():
    wikipedia_scraper()
    print(town_without_page_list)
    result_list = []
    for town in town_without_page_list:
        cadastral, province = search_cadastral_code_of_town(town)
        result_list.append({
            "cc": cadastral,
            "id": town,
            "p": province
        })
    print_to_json(result_list)


def main():
    result_list = []
    town_list = set(lombardia_scraper() + lombardia_xxi_scraper())
    for town in town_list:
        town = town.replace("Ca'", "Ca")
        cadastral, province = search_cadastral_code_of_town(town)
        print(cadastral)
        result_list.append({
            "cc": cadastral,
            "id": town,
            "p": province
        })
    print_to_json(result_list)


if __name__ == '__main__':
    main()
