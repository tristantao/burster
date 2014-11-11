#from page import Page
from page import *
import pdb
import search_util
import keys
import db_util
import csv
import keys

#result_list, next_link = search_util.bing_search("Python Software Foundation", keys.bing_id,
#                                                  first_n=50)
#print result_list[0].url
#print result_list[0].title

#page = Page("https://www.stat.tamu.edu/people/", "texas")
#page.crawl_root(depth=1)

#print page.emails
#pdb.set_trace()

if __name__ == "__main__":
    csv_out = csv.writer(open("data/professors_nov_10.csv", "a"))
    csv_out.writerow(["FIRST NAME", "EMAIL", "UNIVERSITY"])


    with open('data/1000.csv', 'rb') as f:
        reader = csv.reader(f) #no header here
        for row in reader:
            university_id, university_name = row[0], row[1]
            print university_id
            print university_name
            target_professors = db_util.extract_unemailed_professors_from_university(university_name, 20)
            print len(target_professors)
            for professor in target_professors:
                if not professor.should_contact:
                    print "[INFO] Skipping Professor: %s" % professor.email
                    continue
                try:
                    professor_name = search_util.name_from_email(professor.email, university_name)
                    professor_name = search_util.simplify_name(professor_name, professor.email)
                    professor.name = professor_name
                    db_util.update_name(professor)
                    csv_out.writerow([professor_name, professor.email, university_name, professor.should_contact()])
                except Exception as e:
                    print str(e)
            db_util.add_email_transaction(target_professors, "1000.csv")

            #extract_unemailed_professors_from_university



