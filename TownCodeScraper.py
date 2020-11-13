import requests
from bs4 import BeautifulSoup


def main():
    response = requests.get(
        url="https://it.wikipedia.org/wiki/Comuni_d%27Italia_soppressi"
    )

    # soup = BeautifulSoup(response.content, 'html.parser')
    soup = BeautifulSoup(open("comunisoppressi.html"), "html.parser")

    li_list = soup.find_all('li')
    print(li_list)
    # for li in li_list:
    #     if "toclevel" not in li['class']:
    #         print(li)


if __name__ == '__main__':
    main()
