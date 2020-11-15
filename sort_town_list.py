import json


def read_json():
    with open('files/comuni.json') as json_file:
        town_list = json.load(json_file)['towns']
        town_list.sort(key=lambda s: s['id'])

        with open('files/comuni_sorted.json', 'w') as output:
            json.dump({"towns": town_list}, output, indent=4)


if __name__ == '__main__':
    read_json()
