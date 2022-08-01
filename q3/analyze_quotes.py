from multiprocessing import connection
import sqlite3


def connect_to_db():
  connection = sqlite3.connect("quotes.db")
  print("Connected to Database")
  return connection

def total_quotes_in_website():
  connection = connect_to_db()
  cursor = connection.cursor()

  cursor.execute("SELECT COUNT(*) as tota_quotes FROM quotes")
  total_quotes = cursor.fetchall()
  print(f'Total Number of quotations on the website: {total_quotes[0][0]}')

def total_quotes_by_author(author_name):
  connection=connect_to_db()
  cursor = connection.cursor()

  author_name = author_name
  cursor.execute("""
      SELECT COUNT(*) 
      FROM quotes 
      WHERE author_id = (
        SELECT id
        FROM authors
        WHERE name = ?
      )
      """,[author_name])
  print(cursor.fetchall())
  connection.commit()
  connection.close()

def authors_with_maximum_no_of_quotes(number):
  connection = connect_to_db()
  cursor = connection.cursor()

  cursor.execute()

total_quotes_in_website()

total_quotes_by_author("Albert Einstein")