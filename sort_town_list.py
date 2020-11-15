import json


def read_json():
    with open('files/comuni_soppressi.json') as json_file:
        town_list = json.load(json_file)['towns']
        town_list.sort(key=lambda s: s['id'])

    return town_list
        # write_json(town_list)


def write_json(town_list, mode):
    with open('files/comuni_{}.json'.format(mode), 'w') as output:
        json.dump({"towns": town_list}, output, indent=4)


def remove_duplicates(town_list):
    unique = {each["id"]: each for each in town_list}.values()
    return [d for d in unique]


if __name__ == '__main__':
    # read_json()
    write_json(remove_duplicates(read_json()), "soppressi_sorted")
