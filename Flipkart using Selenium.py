from selenium import webdriver
import os
from bs4 import BeautifulSoup
import time
import csv
import requests
from selenium.webdriver.common.keys import Keys

class Flipkart():

    def __init__(self):
        self.current_path=os.getcwd()
        self.url='https://www.flipkart.com'
        self.driver_path= "geckodriver.exe"
        self.driver=webdriver.Firefox(executable_path=self.driver_path)

    def page_load(self):
        self.driver.get(self.url)
        try:
            login_pop=self.driver.find_element_by_class_name("_29YdH8")
            login_pop.click()
            print('pop-up closed')
        except:
            pass
        search_field=self.driver.find_element_by_class_name("LM6RPg")
        search_field.send_keys("smartphone"+'\n')
        time.sleep(2)
        search=self.driver.find_element_by_class_name("vh79eN")
        search.click()
        page_url=self.driver.current_url
        page_html=requests.get(page_url)
        #print(page_url)
        self.soup=BeautifulSoup(page_html.text,"html.parser")
        #print(self.soup)


    def create_csv_file(self):
        rowHeaders = ["Name", "Storage_details", "Screen_size", "Camera_details", "Battery_details", "Processor",
                      "Warranty", "Price in Rupees"]
        self.file_csv=open("Flipkart.csv","w",newline='',encoding='utf-8')
        self.mycsv=csv.DictWriter(self.file_csv,fieldnames=rowHeaders)
        self.mycsv.writeheader()

    def data_scrap(self):
        first_page=(self.soup.find_all('div',{'class':'_3O0U0u'}))
        for i in first_page:
            Name = i.find('div', class_="_3wU53n").text
            price = i.find('div', class_='_1vC4OE _2rQ-NK').text
            details = i.find_all('li')
            storage = details[0].text
            camera_details = details[2].text
            screen_size = details[1].text
            battery_details = details[3].text
            processor = details[4].text
            try:
                warranty_details=[j.text for j in details if j.text[:14]=="Brand Warranty"][0]
            except:
                warranty_details="No warranty"


            my_dict={"Name":Name,"Storage_details":storage,"Screen_size":screen_size,"Camera_details":camera_details,"Battery_details": battery_details,"Processor": processor, "Warranty": warranty_details, "Price in Rupees": price}
            print(my_dict)
            self.mycsv.writerow(my_dict)


    def tearDown(self):
        self.driver.quit()
        self.file_csv.close()


if __name__=="__main__":
    Flipkart=Flipkart()
    Flipkart.page_load()
    Flipkart.create_csv_file()
    Flipkart.data_scrap()
    Flipkart.tearDown()
    print("Task Completed")




