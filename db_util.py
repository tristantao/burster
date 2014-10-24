import psycopg2
import sys
import csv
import professor
import university

## void connect_db
## void load_university()
## {} get_university_from_db


def connect_db():
    try:
        conn_string = "host='localhost' dbname='burster_data'"
        conn = psycopg2.connect(conn_string)
        conn.autocommit = True
    except:
        print "Cannot connect to db"
        raise
    cur = conn.cursor()
    return conn, cur

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

    cur.close()
    conn.close

def get_university_from_db():
    '''
    Returns unviersities in a list of University instances.
    '''
    conn, cur = connect_db()
    query = "select id, name, region, url from university"
    university_list = []
    try:
        cur.execute(query)
        for row in cur:
            university_list.append(university.University(row[0], row[1], row[2], row[3]))
    except psycopg2.Error as pE:
        print str(pE)
        raise
    conn.close()
    cur.close()
    return university_list

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
    return true


if __name__ == "__main__":
    load_university_csv()


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

ALTER TABLE professor
    add COLUMN last_contacted timestamp default NULL;

'''
#cur.execute('INSERT INTO %s (day, elapsed_time, net_time, length, average_speed, geometry)
						#VALUES (%s, %s, %s, %s, %s, %s)', (escaped_name, day, time_length, time_length_net,
																																										             #length_km, avg_speed, myLine_ppy))












