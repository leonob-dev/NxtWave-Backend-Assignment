import json

with open("quotes.json","r") as f:
  quotes_file = f.read()



quotes_file = json.loads(quotes_file)

# for author in quotes_file["authors"]:
#   print(author["name"])
#   print(author["born"])

#   print("")


for quote in quotes_file["quotes"]:
  print(quote["quote"][:10])
  print(quote["author"])
  print(quote["tags"])

  print("")