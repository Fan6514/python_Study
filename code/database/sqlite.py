import sqlite3

# connect to db
conn = sqlite3.connect('test.db')
# create a Cursor
cursor = conn.cursor()
# execute sql to create a user table
cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')
# execute sql to insert a data
cursor.execute('insert into user (id, name) values values (\'1\', \'Michael\')')
# get insert lines
print(cursor.rowcount)
# close Cursor
cursor.close()
# commit
conn.commit()
# close connection
conn.close()

# select table
conn = sqlite3.connect('test.db')
cursor = conn.cursor()
# select sql
cursor.execute('select * from user where id=?', ('1',))
# get select result
values = cursor.fetchall()
print(values)
# close Cursor
cursor.close()
# close connection
conn.close()
