from email.quoprimime import quote
from pydoc import text
import requests
from bs4 import BeautifulSoup
import time
import json





def creating_author_dict(author_born_deatils,author_page_link):
  author_details = {
    "name":author_name,
    "born":author_born_deatils,
    "reference":author_page_link
  }
  authors_dict[author_name]=author_details

def extracting_author_details(author_page,author_page_link):
  soup = BeautifulSoup(author_page.content,"html.parser")
  
  author_birth_date = soup.find("span",class_="author-born-date")
  author_birth_place = soup.find("span",class_="author-born-location")
  author_born_deatils = author_birth_date.text+" "+author_birth_place.text

  creating_author_dict(author_born_deatils,author_page_link)

def souping_author_page(each_quote):
  
  author_link = each_quote.find("a")
  author_page_link = f'http://quotes.toscrape.com{author_link["href"]}'
  author_page = requests.get(author_page_link)
  extracting_author_details(author_page,author_page_link)

def creating_quote_dict(quote,author,tags):

  global author_name
  author_name = author.text
  quote = str(quote.text.strip('“,”'))
  author = author.text
  quote_details = {
    "quote":quote,
    "author":author,
    "tags":tags
  }
  quotes_list.append(quote_details)
        
def extracting_the_each_quote_details(each_quote):

  quote = each_quote.find("span",class_="text")
  author = each_quote.find("small",class_="author")
  tags = []
  for each_tag in each_quote.find_all("a",class_="tag"):
    tags.append(each_tag.text)
  creating_quote_dict(quote,author,tags)

def souping_the_page(html_page):

  soup = BeautifulSoup(html_page,'html.parser')
  quotes_list = soup.find_all("div",class_="quote")
  for each_quote in quotes_list:
    extracting_the_each_quote_details(each_quote)
    souping_author_page(each_quote)
  
def get_html_page(url):
  html_page = requests.get(url)
  souping_the_page(html_page.content)
  
def generate_urls():
  for i in range(1,11):
    page_number = str(i)
    url = f'http://quotes.toscrape.com/page/{page_number}/'
    print(url)
    get_html_page(url)
    time.sleep(20)



author_name = ""
quotes_list = []
authors_dict = {}

def create_quotes_json_file():

  generate_urls()
  authors_final_list = []
  for i,k in authors_dict.items():
    authors_final_list.append(k)

  quotes_json = json.dumps({"quotes":quotes_list,"authors":authors_final_list})
  with open("quotes.json","w") as f:
    f.write(quotes_json)

create_quotes_json_file()




