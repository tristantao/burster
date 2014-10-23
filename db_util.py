import psycopg2
import sys
import csv


# void connect_db
# void load_university()
# {} get_university_from_db
#

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

def load_university():
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
    Returns unviersities in a dict format:
    name as key, and url as val.
    '''
    conn, cur = connect_db()
    query = "select name, url from university"
    university_dict = {}
    try:
        cur.execute(query)
        for row in cur:
            university_dict[row[0]] = row[1]
    except psycopg2.Error as pE:
        print str(pE)
        raise
    conn.close()
    cur.close()
    return university_dict

def iter_university():
    pass

if __name__ == "__main__":
    load_university()



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
   email varchar (25) UNIQUE NOT NULL,
   name varchar(25) default NULL,
   department varchar (25) default NULL,
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












