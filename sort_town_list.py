import json


def read_json():
    with open('files/comuni_soppressi.json') as json_file:
        town_list = json.load(json_file)['towns']
        town_list.sort(key=lambda s: s['id'])

    return town_list


def write_json(town_list, mode):
    with open('files/comuni_{}.json'.format(mode), 'w') as output:
        json.dump({"towns": town_list}, output, indent=4)


def remove_duplicates(town_list):
    unique = {each["id"]: each for each in town_list}.values()
    return [d for d in unique]


def add_suppressed_towns_and_sort():
    with open('files/lombardia_soppressi.json') as suppressed_sorted:
        suppressed_sorted_list = json.load(suppressed_sorted)
        with open('files/comuni_nuovi_e_soppressi.json') as sorted:
            sorted_list = json.load(sorted)['towns']

            merge_list = remove_duplicates(suppressed_sorted_list + sorted_list)
            merge_list.sort(key=lambda s: s['id'])
            write_json(merge_list, "nuovi_e_soppressi_con_lombardia")


if __name__ == '__main__':
    # read_json()
    add_suppressed_towns_and_sort()
