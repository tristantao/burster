import csv
import sys

if __name__ == "__main__":

    current_univ = ''
    university_hash = {}
    with open('professors_nov_10.csv', 'rbU') as f:
        reader = csv.reader(f, dialect="excel") #no header here
        for row in reader:
            name, email, university, good, contacted  = row[0], row[1], row[2], row[3], row[4]
            name_email_up = university_hash.get(university, [])
            name_email_up.append([name, email, good, contacted])
            university_hash[university] = name_email_up

    batch_index = 1
    keys = university_hash.keys()
    while True:
        current_keys = keys[:]
        for university in current_keys:
            prof_list = university_hash.get(university, [])
            if len(prof_list) == 0:
                keys.remove(university)
            with open('batch_%s.csv' % batch_index, 'a') as out_f:
                csv_out = csv.writer(out_f)
                if len(prof_list) != 0:
                    out_list = prof_list.pop()
                    out_list.insert(2, university)
                    csv_out.writerow(out_list)
        if len(keys) == 0:
            break
        batch_index += 1




