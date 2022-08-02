from asyncio.windows_events import NULL
import sqlite3
import json



def connect_to_db():
  connection = sqlite3.connect("quotes.db")
  print("Connected to Db")
  return connection

def get_quotes_file():
  with open("quotes.json","r") as f:
    quotes_file = f.read()
    quotes_file = json.loads(quotes_file)
  print("Quotes File Fetched")
  return quotes_file

def get_all_tags(quotes_file):
  tags_set = set()

  for each_quote in quotes_file["quotes"]:
    for each_tag in each_quote["tags"]:
      tags_set.add(each_tag)

  tags_list = sorted(list(tags_set))
  return tags_list

def get_author_id(author_name,author_table_list):
  for author in author_table_list:
    if author_name == author[1]:
      author_id = author[0]
      break
  return author_id

def get_quote_id(quote,quotes_list):
  for each_quote in quotes_list:
    if each_quote[1]==quote:
      quote_id = each_quote[0]
      break
  return quote_id

def get_tags_ids(tags,tags_table_list):
  tags_ids_list = []
  for each_tag in tags:
    for each_tag_tuple in tags_table_list:
      if each_tag == each_tag_tuple[1]:
        tags_ids_list.append(each_tag_tuple[0])
  return tags_ids_list

def create_authors_table():
  db_connection = connect_to_db()
  cursor = db_connection.cursor()

  cursor.execute("""
      CREATE TABLE Authors (
        id INTEGER NOT NULL PRIMARY KEY,
        name VARCHAR(250),
        born TEXT,
        reference TEXT

      )""")

  db_connection.commit()
  db_connection.close()
  print("Author Table Created")

def create_tags_table():
  connection = connect_to_db()
  cursor = connection.cursor()

  cursor.execute("""
    CREATE TABLE TAGS (
        id INTEGER NOT NULL PRIMARY KEY,
        tag TEXT)
  """)

  connection.commit()
  connection.close()
  print("Tags_table Created")

def create_quotes_table():
  connection = connect_to_db()
  cursor = connection.cursor()

  cursor.execute("""
        CREATE TABLE QUOTES(
          id INTEGER NOT NULL PRIMARY KEY,
          quote TEXT,
          no_of_tags INTEGER,
          author_id INTEGER,
          FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE
        )
  """)

  connection.commit()
  connection.close()
  print("quotes Table Created")

def create_quote_tag_table():
  connection = connect_to_db()
  cursor = connection.cursor()

  cursor.execute("""
  CREATE TABLE quote_tag(
    id INTEGER NOT NULL PRIMARY KEY,
    quote_id INTEGER,
    tag_id INTEGER,
    FOREIGN KEY (quote_id) REFERENCES quotes(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
  )
  """)

  connection.commit()
  connection.close()
  print("Quote_tag Table Created")

def insert_data_into_authors_table(quotes_file):
  db_connection = connect_to_db()
  cursor = db_connection.cursor()

  for author in quotes_file["authors"]:
    author_details = [author["name"],author["born"],author["reference"]]
    cursor.execute("INSERT INTO Authors('name','born','reference') VALUES(?,?,?)",author_details)
        

  db_connection.commit()
  db_connection.close()
  print("Data Inserted into Authors Table")

def insert_data_into_tags_tables(tags_list):
  db_connection = connect_to_db()
  cursor = db_connection.cursor()
  
  for each_tag in tags_list:
    cursor.execute("INSERT INTO TAGS('tag') VALUES(?)",[each_tag])

  db_connection.commit()
  db_connection.close()
  print("Data Inserted Into Tags Table")

def insert_data_into_quotes_table(quotes_file,author_table_list):
  connection = connect_to_db()
  cursor = connection.cursor()

  for each_quote in quotes_file["quotes"]:
    quote = each_quote["quote"]
    no_of_tags = len(each_quote["tags"])
    author_id = get_author_id(each_quote["author"],author_table_list)

    cursor.execute("""
    INSERT INTO 
    QUOTES('quote','no_of_tags','author_id')
    VALUES(?,?,?)"""
    ,[quote,no_of_tags,author_id])

  connection.commit()
  connection.close()
  print("Data Inserted into Quotes Table")

def insert_data_into_quote_tag_table(quotes_file,quotes_table_list,tags_table_list):
  connection = connect_to_db()
  cursor = connection.cursor()

  for each_quote in quotes_file:
    quote_id = get_quote_id(each_quote["quote"],quotes_table_list)
    tags_ids_list = get_tags_ids(each_quote["tags"],tags_table_list)

    if len(tags_ids_list) == 0:
      cursor.execute("INSERT INTO quote_tag('quote_id') VALUES(?)",[quote_id])
    else:
      for each_tag_id in tags_ids_list:
        cursor.execute("INSERT INTO quote_tag('quote_id','tag_id') VALUES(?,?)",[quote_id,each_tag_id])

  connection.commit()
  connection.close()
  print("Data Inserted Into Quote_Tag Table")
      
def get_author_table():
  db_connection = connect_to_db()
  cursor = db_connection.cursor()

  cursor.execute("""
     SELECT * FROM Authors  """)
  author_table_list = cursor.fetchall()

  for each_author in author_table_list:
    print(each_author)

  db_connection.commit()
  db_connection.close()
  print("Fetched Authors Table")
  return author_table_list

def get_tags_table():
  connection = connect_to_db()
  cursor = connection.cursor()

  cursor.execute("SELECT * FROM TAGS")
  tags_table = cursor.fetchall()

  for each_tag in tags_table:
    print(each_tag)
  connection.commit()
  connection.close()
  print("Fetched Tags Table")
  return tags_table
  
def get_quotes_table():
  connection = connect_to_db()
  cursor = connection.cursor()

  cursor.execute("SELECT * FROM quotes")
  quotes_table = cursor.fetchall()

  for each_quote in quotes_table:
    print(each_quote)

  connection.commit()
  connection.close()
  print("Fetched Quotes Table")
  return quotes_table

def get_quote_tag_table():
  connection = connect_to_db()
  cursor = connection.cursor()

  cursor.execute("SELECT * FROM quote_tag")
  quote_tag_table = cursor.fetchall()

  for each_quote_tag in quote_tag_table:
    print(each_quote_tag)

  connection.commit()
  connection.close()
  print("Fetched Quote_Tag Table")
  return quote_tag_table




quotes_file = get_quotes_file()
tags_list = get_all_tags(quotes_file)

create_tags_table()
insert_data_into_tags_tables(tags_list)
tags_table_list = get_tags_table()

create_authors_table()
insert_data_into_authors_table(quotes_file)
author_table_list = get_author_table()

create_quotes_table()
insert_data_into_quotes_table(quotes_file,author_table_list)
quotes_table_list = get_quotes_table()

create_quote_tag_table()
insert_data_into_quote_tag_table(quotes_file["quotes"],quotes_table_list,tags_table_list)
each_quote_list = get_quote_tag_table()


