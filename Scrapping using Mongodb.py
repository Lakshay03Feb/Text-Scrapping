
import requests
from bs4 import BeautifulSoup

import pymongo

items=input("Enter list of items").split(",")
print(items)



dbConn = pymongo.MongoClient("mongodb://localhost:27017/")  # opening a connection to Mongo
db = dbConn['Flipkart']
for i in items:
    reviews = db[i].find({})
    if reviews.count() >0:
        print("Data is already there")

    else:
        for j in range(1,2):
            url = ("https://www.flipkart.com/search?q={}&otracker=search&otracker{}=search&marketplace=FLIPKART&as-show=on&as=off".format(i,j))
            print(url)
            html_page = requests.get(url)
            html = BeautifulSoup(html_page.text, "html.parser")
            page = (html.find_all('div', {'class': '_3O0U0u'}))
            for p in page:
                Name = p.find('div', class_="_3wU53n").text
                price = p.find('div', class_='_1vC4OE _2rQ-NK').text
                link = p.find('a', class_='_31qSD5')["href"]
                product_link = "https://www.flipkart.com" + link

                product_page = requests.get(product_link)
                product_html = BeautifulSoup(product_page.content, "html.parser")
                # print(product_html)
                a = product_html.find_all('div', {'class': '_1HmYoV _35HD7C'})[0].find_all("div", {"class": "MocXoX"})[
                    0]
                b = a.find_all("div", {'class': "_2lzn0o"})
                for k in range(len(b)):
                    if b[k].text == "Dimensions":
                        x = k
                c = a.find_all("div", {'class': "_2RngUh"})[x].findAll("tr")
                # print(c)
                my_product_dict = {}
                for m in range(len(c)):
                    my_product_dict[c[m].find("td").text] = c[m].find('li').text

                mydict = {"Name": Name, "Price": price}
                mydict.update(my_product_dict)
                table = db[i]
                x = table.insert_one(mydict)










