import bs4
import pandas as pd
import re

from urllib.request import urlopen as uReq
from urllib.request import Request
from bs4 import BeautifulSoup as soup


#saving the url in my_url
my_url='https://www.amazon.in/pcr/Best-Rated-Smartphones-Reviews/1805560031?ref_=fspcr_ebc_2_1389432031'

#opening up the connection, grabbing the url
req=Request(my_url, headers={'User-Agent': 'Mozilla/5.0'})
uClient=uReq(req)

#offloads the content into a variable
page_html= uClient.read()
uClient.close()

#html parsing
page_soup= soup(page_html,"lxml")

#extracting the links for each phone and saving them in a list
l1=[]
for A in page_soup.findAll('a',attrs={'class':'FS-PCR-pl-asin-title'}):
    link=A.get('href')
    l1.append(link)


#extracting the names for each phone and saving them in a list
l2 = []
for A in page_soup.findAll('a',attrs={'class':'FS-PCR-pl-asin-title'}):
    name=A.text.strip()
    name=re.sub(r'(\s+|\n)', ' ', name)
    l2.append(name)


#creating a dataframe for both names and link 
df=pd.DataFrame(columns=['name','links'])
df['name']=l2
df['links']=l1


#saving names one by one in a variable name
names=[x for x in df['name']]

#creating two final lists for the data frame
name_list=[]
review_list=[]
j=0
for links in df['links']:

    #saving individual links one by one from the list   
    my_url='https://www.amazon.in' + links

    #opening up the connection, grabbing the url
    req=Request(my_url, headers={'User-Agent': 'Chrome/70.0.3538.77'})

    uClient=uReq(req)

    #offloads the content into a variable
    page_html= uClient.read()
    uClient.close()

    #html parsing
    page_soup= soup(page_html,"lxml")

    #finding all div content which contains the reviews for that particular phone
    a= page_soup.findAll("div",{"data-hook":"review-collapsed"})
    
    #extracting review from text and appending them in a list
    for i, review in enumerate(a):
        name_list.append(names[j])
        review_list.append(review.text)
    j=j+1
    
#creating one data-frame and saving both the final name and review lists
new_df=pd.DataFrame(columns=['Phone Name','Review'])
new_df['Phone Name']=name_list
new_df['Review']=review_list

#saving the data in a csv
new_df.to_csv('Review-Top-Phones.csv',index=False)
