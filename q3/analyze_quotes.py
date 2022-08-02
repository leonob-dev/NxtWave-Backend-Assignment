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
  cursor.execute("""
    SELECT authors.name,count(quotes.id) AS total_quotes
    FROM quotes INNER JOIN authors on quotes.author_id = authors.id
    GROUP BY author_id 
    ORDER BY total_quotes DESC, authors.name ASC
    LIMIT ?
  """,[number])
  total_quotes_by_author = cursor.fetchall()
  for i in total_quotes_by_author:
    print(i)

  connection.commit()
  connection.close()


def max_min_avg_no_of_tags():
  connection = connect_to_db()
  cursor = connection.cursor()

  cursor.execute("""
    SELECT 
      MAX(no_of_tags),
      MIN(no_of_tags),
      AVG(no_of_tags)
    FROM quotes
  """)
  max_min_avg_of_quotes = cursor.fetchall()
  print(f'MAX No_of_Tags : {max_min_avg_of_quotes[0][0]}')
  print(f'MIN No_of_Tags : {max_min_avg_of_quotes[0][1]}')
  print(f'AVG No_of_Tags : {max_min_avg_of_quotes[0][2]}')

  connection.commit()
  connection.close()

total_quotes_in_website()

total_quotes_by_author("Albert Einstein")

authors_with_maximum_no_of_quotes(20)

max_min_avg_no_of_tags()