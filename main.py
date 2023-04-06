import csv
import re
import operator
import itertools
import os


def read_csv_to_dict(file_name):
    contacts_dict = []
    with open(file_name, encoding="utf8") as file:
        reader = csv.reader(file, delimiter=",")
        contacts_list = list(reader)

        keys = contacts_list[0]
        values = contacts_list[1:]
        for num, vals in enumerate(values):
            contacts_dict.append({})
            for key, val in zip(keys, vals):
                contacts_dict[num].update({key: val})

        return contacts_dict


def write_dicts_to_file(file_name, dicts):
    keys = list(dicts[0].keys())
    with open(file_name, "w", encoding="utf8") as file:
        datawriter = csv.writer(file, delimiter=",")
        datawriter.writerow(keys)
        for dict in dicts:
            datawriter.writerow(dict.values())


def fix_phones(in_file, out_file):
    with open(in_file, encoding="utf8") as file:
        text = file.read()

    pattern_phone = r"(\+7|8)?\s*\(?(\d{3})\)?[\s*-]?(\d{3})[\s*-]?(\d{2})[\s*-]?(\d{2})(\s*)\(?(доб\.?)?\s*(\d*)?\)?"
    fixed_phones = re.sub(pattern_phone, r"+7(\2)\3-\4-\5\6\7\8", text)
    with open(out_file, "w+", encoding="utf8") as file:
        text = file.write(fixed_phones)


def fix_names(in_file):
    contacts_dict = read_csv_to_dict(in_file)
    for v in contacts_dict:
        split = v["lastname"].split( )
        if len(split) > 1:
            v["lastname"] = split[0]
            v["firstname"] = split[1]
            if len(split) > 2:
                v["surname"] = split[2]

        split = v["firstname"].split( )
        if len(split) > 1:
            v["firstname"] = split[0]
            v["surname"] = split[1]

    return contacts_dict


def merge_names(contacts):
    group_list = ["firstname", "lastname"]
    group = operator.itemgetter(*group_list)
    contacts.sort(key=group)
    grouped = itertools.groupby(contacts, group)

    merge_data = []
    for (firstname, lastname), g in grouped:
        merge_data.append({"lastname": lastname, "firstname": firstname})
        for gr in g:
            d1 = merge_data[-1]
            for k, v in gr.items():
                if k not in d1 or d1[k] == "":
                    d1[k] = v

    return merge_data


fix_phones(in_file="phonebook_raw.csv", out_file="fixed_phones.csv")

fixed_names = fix_names(in_file="fixed_phones.csv")
os.remove("fixed_phones.csv")
merged_names = merge_names(fixed_names)

write_dicts_to_file("phonebook.csv", merged_names)
