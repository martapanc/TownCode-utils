import json


def read_json():
    with open('files/comuni.json') as json_file:
        town_list = json.load(json_file)['towns']
        town_list.sort(key=lambda s: s['id'])

        write_json(town_list)


def write_json(town_list, mode):
    with open('files/comuni_{}.json'.format(mode), 'w') as output:
        json.dump({"towns": town_list}, output, indent=4)


def remove_duplicates(town_list):
    unique = {each["id"]: each for each in town_list}.values()
    print(unique)
    return unique


if __name__ == '__main__':
    # read_json()
    remove_duplicates([{"id": "ciao", "cc": 1}, {"id": "ciao", "cc": 2}])
