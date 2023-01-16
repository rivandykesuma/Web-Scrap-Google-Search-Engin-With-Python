import requests
from bs4 import BeautifulSoup
import time
from mysql.connector import (connection)

# Create database before doing scrap web google search engine
con = connection.MySQLConnection(host='localhost', user='root', password='root')
cur = con.cursor()

cur.execute("""create database IF NOT EXISTS db_name""")

#Connect Database and create table for get data goole to SQL
con = connection.MySQLConnection(host='localhost', user='root', password='root',database = 'db_name')
cur = con.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS table_name(
    keyword varchar(100) DEFAULT NULL,
    title varchar(100) DEFAULT NULL,
    paragraph varchar(2000) DEFAULT NULL,
    link varchar(500) DEFAULT NULL UNIQUE
    )""")

# fill keyword for search data in google search engine.. can be unlimited keyword in list
keyword = [
'python', 'machine Learning'
]

#looping web scrapping google search engine 
for i in keyword:
    key = i.replace(" ","+")
    page = [x for x in range(10)]
    for c in page:
        print(i,c)
        url = 'https://www.google.com/search?q={}&start={}&sa=N'.format(key,(c*10))
        req = requests.get(url)
        time.sleep(5)
        sor = BeautifulSoup(req.text, "html.parser")
        list_article = sor.findAll("div", class_='Gx5Zad fP1Qef xpd EtOod pkphOe')
        
        for d in list_article:
            #print(i)
            title = d.find("div", class_='BNeawe vvjwJb AP7Wnd').text
            paragraph = d.find("div", class_='BNeawe s3v9rd AP7Wnd').text
            link = d.find('a')['href'].rsplit('&sa', 1)[0].replace('/url?q=','')
            try:
                cur.execute("""INSERT INTO table_name VALUES(%s,%s,%s,%s)""",(i,title, paragraph,link))
            
                con.commit()
            except:
                print('skip')
                pass
                

