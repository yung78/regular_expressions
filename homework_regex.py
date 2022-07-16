from pprint import pprint
import re
import csv


def contact_book():
    contacts_list = []
    patern = r'(\+7|8)*\s*\(*(\d*)\)*\s*[s-]*(\d{3})\s*[s-]*(\d{2})\s*[s-]*(\d{2})\s*\(*([а-я]*\.*)\s*(\d*)\)*'
    with open("phonebook_raw.csv", encoding='utf8') as f:
        rows = csv.reader(f, delimiter=",")
        first_list = list(rows)
        for elem in first_list:
            res = re.sub(patern, r'+7(\2)\3-\4-\5 \6\7', elem[5])
            elem[5] = res
            contacts_list.append(elem)
    return contacts_list


def corrected():
    old_list = contact_book()
    correct_list = []
    for contact in old_list:
        if ' ' in contact[0]:
            cont = contact[0].split()
            id = 0
            for elem in cont:
                contact[id] = elem
                id += 1
        correct_list.append(contact)
    return correct_list


def del_double():
    c_list = corrected()
    end_list = corrected()
    counter = 1
    del_id = []
    for el1 in range(1, len(c_list)):
        counter += 1
        for el2 in range(counter, len(c_list)):
            if c_list[el1][0] == c_list[el2][0] and c_list[el1][1] == c_list[el2][1]:
                temp_list = []
                for doub_el1, doub_el2 in zip(c_list[el1], c_list[el2]):
                    if doub_el1 != '':
                        temp_list.append(doub_el1)
                    else:
                        temp_list.append(doub_el2)
                end_list[el1] = temp_list
                del_id.append(el2)
    end_list[:] = [x for i, x in enumerate(end_list) if i not in del_id]
    return end_list


def save_changes():
    with open("phonebook.csv", "w", encoding='utf8') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(del_double())


save_changes()
