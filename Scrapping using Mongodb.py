import requests
from bs4 import BeautifulSoup
import pandas as pd
import pymongo

dbConn = pymongo.MongoClient("mongodb://localhost:27017/")  # opening a connection to Mongo
db = dbConn['Flipkart']   #  Flipkart1,2,and 3 are the  databases
db1=dbConn["Flipkart1"]
db2=dbConn["Flipkart2"]
db3=dbConn["Flipkart3"]
data=pd.read_csv("Flipkart.csv")
print(data.head())
print(data.shape)
items=[]
items_link=[]

for _ in range(0,453):
    items.append(data.iloc[_,2])
    items_link.append(data.iloc[_,3])




for i in range(len(items)):

    reviews = db[items[i]].find({})
    reviews_1 = db1[items[i]].find({})
    reviews_2 = db2[items[i]].find({})
    if reviews.count()>0 or reviews_1.count()>0 or reviews_2.count()>0:
        print("Data is already there")


    else:
        for j in range(1,8):
            url = (items_link[i]+"&page={}".format(j))
            print(url)
            html_page = requests.get(url)
            html = BeautifulSoup(html_page.text, "html.parser")
            try:

                page = (html.find_all('div', {'class': '_3O0U0u'}))
                for k in page:
                    Main={}
                    try:
                        Name = k.find('div', class_="_3wU53n").text
                        price = k.find('div', class_='_1vC4OE _2rQ-NK').text
                        link = k.find('a', class_='_31qSD5')["href"]
                        product_link = "https://www.flipkart.com" + link

                        product_page = requests.get(product_link)
                        product_html = BeautifulSoup(product_page.content, "html.parser")
                        # print(product_html)
                        mydict = {"Name": Name, "Price": price}
                        try:
                            a = product_html.find_all('div', {'class': '_1HmYoV _35HD7C'})[0].find_all("div",{"class": "MocXoX"})[0]
                            b = a.find_all("div", {'class': "_2lzn0o"})
                            for l in range(len(b)):
                                if b[l].text == "Dimensions":
                                    x = l
                            # print(b)
                            c = a.find_all("div", {'class': "_2RngUh"})[x].findAll("tr")
                            # print(c)
                            my_product_dict = {}
                            for m in range(len(c)):
                                my_product_dict[c[m].find("td").text] = c[m].find('li').text
                            mydict.update(my_product_dict)
                        except:
                            pass

                        table=db3[items[i]]
                        x=table.insert_one(mydict)

                    except:
                        row=[]
                        for s in range(0, 4):
                            try:
                                Name = k.find_all("a", class_="_2cLu-l")[s]["title"]
                                price = k.find_all("div", class_="_1vC4OE")[s].text
                                link = k.find_all("a", class_="_2cLu-l")[s]["href"]

                                product_link = "https://www.flipkart.com" + link

                                product_page = requests.get(product_link)
                                product_html = BeautifulSoup(product_page.content, "html.parser")
                                # print(product_html)
                                mydict = {"Name": Name, "Price": price}
                                #print(mydict)
                            except:
                                Name = k.find_all("a", class_="_2mylT6")[s]["title"]
                                price = k.find_all("div", class_="_1vC4OE")[s].text
                                link = k.find_all("a", class_="_2mylT6")[s]["href"]

                                product_link = "https://www.flipkart.com" + link

                                product_page = requests.get(product_link)
                                product_html = BeautifulSoup(product_page.content, "html.parser")
                                # print(product_html)
                                mydict = {"Name": Name, "Price": price}

                            try:
                                a = product_html.find_all('div', {'class': '_1HmYoV _35HD7C'})[0].find_all("div", {"class": "MocXoX"})[0]
                                b = a.find_all("div", {'class': "_2lzn0o"})
                                for n in range(len(b)):
                                    if b[n].text == "Dimensions":
                                        x = n
                                # print(b)
                                c = a.find_all("div", {'class': "_2RngUh"})[x].findAll("tr")
                                # print(c)
                                my_product_dict = {}
                                for m in range(len(c)):
                                    my_product_dict[c[m].find("td").text] = c[m].find('li').text
                                mydict.update(my_product_dict)

                            except:
                                v = ["Height", "Weight", "Width", "Depth"]
                                try:

                                    #print(v)
                                    o = product_html.find_all('div', {'class': '_2RngUh'})[0]
                                    #print(o)
                                    d = o.find_all("td", class_="_3-wDH3 col col-3-12")
                                    c = []
                                    for a in range(len(d)):
                                        if d[a].text in v:
                                            c.append(a)

                                    #print(c)
                                    g = [d[b].text for b in c]
                                    r = product_html.find_all('div', {'class': '_2RngUh'})[0].find_all("li")
                                    rr = [r[i].text for i in c]
                                    #print(rr)
                                    my_product_dict = {}
                                    for p in range(len(c)):
                                        my_product_dict[g[p]] = rr[p]
                                    mydict.update(my_product_dict)
                                    #print(mydict)

                                except:
                                    o = product_html.find_all('div', {'class': '_2GNeiG'})[0]
                                    d = o.find_all("div", class_="col col-3-12 _1kyh2f")
                                    c = []
                                    for a in range(len(d)):
                                        if d[a].text in v:
                                            c.append(a)
                                    g = [d[b].text for b in c]
                                    r = o.find_all("div", class_="col col-9-12 _1BMpvA")
                                    rr = [r[i].text for i in c]
                                    my_product_dict = {}
                                    for p in range(len(c)):
                                        my_product_dict[g[p]] = rr[p]
                                    mydict.update(my_product_dict)
                                    # print(mydict)

                            row.append(mydict)

                        print(row)
                        table=db3[items[i]]
                        for t in row:
                            x = table.insert_one(t)
            except:
                pass












