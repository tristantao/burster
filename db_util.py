import sys
import csv
from professor import *
import university
import psycopg2
import psycopg2.extras

## void connect_db
## void load_university()
## {} get_university_from_db

##################
#### Utility #####
##################

def connect_db():
    try:
        conn_string = "host='localhost' dbname='burster_data'"
        conn = psycopg2.connect(conn_string)
        conn.autocommit = True
        print "[INFO] Connected to DB."
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        print "[INFO] Cursor Created."
    except:
        print "Cannot connect to db"
        raise
    return conn, cur

def close_db(conn, cur):
    cur.close()
    conn.close()
    print "[INFO] Disconnected db."

##################
### University ###
##################

def load_university_csv():
    conn, cur = connect_db()
    with open('universities.csv', 'rb') as f:
        reader = csv.reader(f)
        header = reader.next()
        print header
        for row in reader:
            university_name, university_url = row
            query = "INSERT INTO %s (name, region, date_added, url) VALUES (%%s, %%s, %%s, %%s)" % "university"
            args_tuple = (university_name, None, "now()", university_url)
            try:
                cur.execute(query, args_tuple)
                conn.commit()
            except psycopg2.IntegrityError as pIE:
                print "Duplicate: " + str(pIE)
                continue
            except psycopg2.DataError as pDE:
                print "Error: " + str(pIE)
                continue
    close_db(conn, cur)

def get_university_from_db():
    '''
    Returns unviersities in a list of University instances.
    Ordered in last scraped date.
    '''
    conn, cur = connect_db()
    query = "SELECT id, name, region, url FROM university ORDER BY last_scraped DESC"
    university_list = []
    try:
        cur.execute(query)
        for row in cur:
            university_list.append(university.University(row[0], row[1], row[2], row[3]))
    except psycopg2.Error as pE:
        print str(pE)
        raise
    close_db(conn, cur)
    return university_list

def update_university_last_scraped(university_id):
    '''
    update the university.last_scraped as now() for university_id
    '''
    conn, cur = connect_db()
    query = "UPDATE %s SET last_scraped = now() WHERE id = '%%s' " % "university"
    arg_id = [university_id]
    try:
        cur.execute(query, arg_id)
        conn.commit()
    except Exception as e:
        print str(e)
    close_db(conn, cur)

##################
### Professors ###
##################

def insert_professors(professor_list):
    '''
    Insert a professor.
    @input list of professors
    '''
    conn, cur = connect_db()
    for professor in professor_list:
        university_id = professor.university_id
        professor_name = professor.name
        professor_email = professor.email
        professor_department = professor.department
        args_tuple = (str(professor_email), professor_name, professor_department, university_id, "now()", None)

        query = """INSERT INTO %s (email, name, department, university_id, date_added, last_contacted) VALUES (%%s, %%s, %%s, %%s, %%s, %%s)""" % "professor"
        try:
            cur.execute(query, args_tuple)
            conn.commit()
        except psycopg2.IntegrityError as pIE:
            print "Duplicate: " + str(pIE)
            continue
    close_db(conn, cur)
    return True

def extract_unemailed_professors_from_university(university_name, n):
    '''
    Returns n professors from a specific university. Only grabs professors we haven't emailed before (for now).
    Tries to return a list of length 0 ~ n depending on professsor count.
    Updates email_transaction assuming that we email the professors.
    '''

    conn, cur = connect_db()
    conn2, cur2 = connect_db()
    try:
        cur.execute(""" SELECT id FROM university WHERE name = '%s' """ % university_name)
        university_id = cur.fetchone()[0]
    except TypeError as tE:
            print str(tE)
            raise

    try:
        query = """ WITH emailed_professors AS (SELECT DISTINCT professor_id FROM %s)
            SELECT * from %s WHERE university_id = %%s AND id NOT in (SELECT professor_id FROM emailed_professors)""" \
            % ("email_transaction", "professor")
        args_tuple = (university_id,)
        cur2.execute(query, args_tuple)

        potential_professors = []
        for professor in cur2: #name, email, university_id, department):9
            print professor
            potential_professors.append(Professor(professor['name'], professor['email'],
                                                  professor['university_id'], professor['department']))
        print len(potential_professors)
        print potential_professors[0].name
        print potential_professors[1].name
    except psycopg2.Error as pE:
            print str(pE)
            raise

    close_db(conn, cur)
    close_db(conn2, cur2)
    return potential_professors


def fix_emails(table_name, email_col_name):
    '''
    Fix emails to email-able form.
    Removes "mailto" or [at] etc.
    '''
    conn, cur = connect_db()
    conn2, cur2 = connect_db()
    conn3, cur3 = connect_db()
    query = """ SELECT * FROM %s """
    cur.execute(query % table_name)
    for row in cur:
        try:
            print row
            professor_id = row['id']
            professor_email = row['email']
            updated = False
            if "/" in professor_email or "'" in professor_email or "mailto" in professor_email:
                professor_email = professor_email.replace("/", "").replace("mailto", "").replace("'", "")
                updated = True
            if "=" in professor_email:
                professor_email = professor_email.split("=")[-1]
                updated = True
            if " at " in professor_email:
                professor_email = professor_email.replace(" at ", "@")
                updated = True
            if updated:
                 cur2.execute("""UPDATE %s SET %s = '%s' WHERE id = %s """ % (table_name, email_col_name, professor_email, professor_id))
        except psycopg2.IntegrityError as pIE:
            print str(pIE)
            cur3.execute("""DELETE FROM %s WHERE id = %s """ % (table_name, professor_id))
            continue
        except psycopg2.Error as pE:
            print str(pE)
            raise
    close_db(conn, cur)
    close_db(conn2, cur2)
    close_db(conn3, cur3)


##################
##### Emails #####
##################
def add_email_transaction(professor_list, email_type, time = None):
    '''
    Updates the email transaction db, assuming we sent emails to the given professors witht the custom email_type
    '''
    conn, cur = connect_db()
    conn2, cur2 = connect_db()
    #id | date | professor_id | email_type
    if (time == None):
        time = "now()"
    query = """INSERT INTO %s (date, professor_id, email_type) VALUES (%%s, %%s, %%s) """ % "email_transaction"

    for professor in professor_list:
        try:
            cur2.execute(""" SELECT id from professor where email = '%s' """ % professor.email)
            professor_id = cur2.fetchone()[0]
            args_tuple = (time, professor_id, email_type)
            cur.execute(query, args_tuple)
        except TypeError as tE:
            print str(tE)
            continue
        except psycopg2.Error as pE:
            print str(pE)
            raise
    close_db(conn, cur)
    close_db(conn2, cur2)

if __name__ == "__main__":
    add_email_transaction([Professor('a', 'cade.white@jmc.acu.edu', 'a', 'a'),
        Professor('b', 'hlfoster@uaa.alaska.edu', 'b', 'b')], "test_email")
    extract_unemailed_professors_from_university("American Business & Technology University",100)
    pass
    #fix_emails('professor', 'email')
    #load_university_csv()


#some notes:
'''
CREATE TABLE IF NOT EXISTS university (
   id serial NOT NULL primary key,
   name varchar(50) UNIQUE NOT NULL,
   region varchar(20) NOT NULL,
   date_added timestamp default NULL
);

insert into university (name, region, date_added) VALUES
('test', 'over the rainbow', now())
;

INSERT INTO films (code, title, did, date_prod, kind) VALUES
    ('B6717', 'Tampopo', 110, '1985-02-10', 'Comedy'),
    ('HG120', 'The Dinner Game', 140, DEFAULT, 'Comedy');


CREATE TABLE IF NOT EXISTS professor (
   id serial NOT NULL primary key,
   email varchar (100) UNIQUE NOT NULL,
   name varchar(100) default NULL,
   department varchar (100) default NULL,
   university_id int NOT NULL,
   FOREIGN KEY(university_id) REFERENCES university(id),
   date_added timestamp default NULL
);


CREATE TABLE IF NOT EXISTS email_transaction (
    id seriaL NOT NULL primary key,
    date timestamp NOT NULL,
    professor_id int NOT NULL,
    FOREIGN KEY(professor_id) REFERENCES professor(id),
    email_type varchar(20) NOT NULL
);



ALTER TABLE professor
    add COLUMN last_contacted timestamp default NULL;

'''
#cur.execute('INSERT INTO %s (day, elapsed_time, net_time, length, average_speed, geometry)
						#VALUES (%s, %s, %s, %s, %s, %s)', (escaped_name, day, time_length, time_length_net,
																																										             #length_km, avg_speed, myLine_ppy))












