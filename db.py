#!/usr/bin/env python3

import mysql.connector
import json, sys, random
import requests, bs4
from mysql.connector import errorcode

authors = []
authors_row = []
publishers = []
publishers_row = []
book_data = []
books_row = []
wrote_data = []
max_authors = 10
max_publishers = 10

add_author = ("INSERT INTO authors "
              "(name) "
              "VALUES (%(name)s)")

add_publisher = ("INSERT INTO publishers "
              "(name) "
              "VALUES (%(name)s)")

add_book = ("INSERT INTO books "
            "(title, pub_id) "
            "VALUES (%(title)s, %(pub_id)s)")

add_wrote = ("INSERT INTO wrote "
           "(author_id, book_id) "
           "VALUES (%(author_id)s, %(book_id)s)")

def insert_wrote(cursor):
    index = 0
    for wrote in wrote_data:
        cursor.execute(add_wrote, wrote)

def insert_books(cursor):
    index = 0
    for book in book_data:
        print(book["title"] + " " + str(book["pub_id"]))
        cursor.execute(add_book, book)
        wrote_data[index]["book_id"] = cursor.lastrowid

def insert_publishers(cursor):
    for publisher in publishers:
        publisher_data = {'name' : publisher}
        cursor.execute(add_publisher, publisher_data)
        pub = {'name' : publisher, 'id' : int(cursor.lastrowid)}
        publishers_row.append(pub)

def insert_authors(cursor):
    for author in authors:
        author_data = {"name": author}
        cursor.execute(add_author, author_data)
        auth = {'name': author, 'author_id': int(cursor.lastrowid)}
        authors_row.append(auth)
    

def normalize_book(json_data):
    for book in json_data['editions']:
        book_title = book['title']
        #book_author = authors[random.randrange(0, max_authors, 1)]
        #book_publisher = publishers[random.randrange(0, max_publishers, 1)]
        book_author = random.randrange(0, max_authors, 1)
        book_publisher = random.randrange(0, max_publishers, 1)
        #Place holder, fixed later on
        book_id = len(book_data)
        book_data.append({'title': book_title,
                          'pub_id': publishers_row[book_publisher]["id"],
        })
        
        wrote_data.append({'author_id': authors_row[book_author]["author_id"],
                          'book_id': book_id,
        })
        
def populate_publishers(json_data):
    for book in json_data['editions']:
        publisher_name(book)
        if len(publishers) >= max_publishers:
            break

def publisher_name(book):
    publisher = book['publishers'][0]
    publishers.append(publisher)

def populate_authors(json_data):
    for book in json_data['editions']:
        author_name(book)
        if len(authors) >= max_authors:
            break

def author_name(book):
    try:
        author_url = book['authors'][0]['key']
        #print(author_url)
        author_data = requests.get('https://openlibrary.org' + author_url)
        html = bs4.BeautifulSoup(author_data.text, 'lxml')
        author = html.title.text.split('|')[0]
        #print(author)
        authors.append(author)
        #print(len(authors))
    except:
        #Ignore errors, just skip to next author
        return
    

try:
    cnx = mysql.connector.connect(
        user='mar64',
        password='password',
        host='127.0.0.1',
        database='zippy')
except mysql.connector.Error as err:
    print(err)
    exit()

#else:
    #cnx.close()

if len(sys.argv) == 1:
    print("Usage db.py file1.json file2.json ...")
    exit()


cursor = cnx.cursor(buffered=True)

for i in range(1, len(sys.argv)):
    
    jfile = open(sys.argv[i], 'r')
    jdata = jfile.read()
    jfile.close()
    book_json = json.loads(jdata)
    
    populate_authors(book_json)
    insert_authors(cursor)

    populate_publishers(book_json)
    insert_publishers(cursor)

    normalize_book(book_json)



print("Authors")
#insert_authors(cursor)
print("Publishers")
#insert_publishers(cursor)
cnx.commit()
print("Books")
insert_books(cursor)
cnx.commit()
print("Wrote")
insert_wrote(cursor)
cnx.commit()
cnx.close()
