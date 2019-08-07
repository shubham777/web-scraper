import bs4
import pandas as pd
import time
import requests
from urllib.request import urlopen as uReq
from urllib.request import Request
from bs4 import BeautifulSoup


url1= 'https://www.indeed.co.in/jobs?q=receptionist+cum+office+assistant&l=Chandigarh%2C+Chandigarh'
url2= 'https://www.indeed.co.in/jobs?q=account+executive&l=Chandigarh'
url3= 'https://www.indeed.co.in/jobs?q=account+assistant&l=Chandigarh'
url4= 'https://www.indeed.co.in/jobs?q=front+office+executive&l=Chandigarh'
url5= 'https://www.indeed.co.in/jobs?q=front+office+associate&l=Chandigarh'
url6= 'https://www.indeed.co.in/jobs?q=computer+operator&l=Chandigarh'
url7= 'https://www.indeed.co.in/jobs?q=data+entry+operator&l=Chandigarh'
url8= 'https://www.indeed.co.in/jobs?q=accountant&l=Chandigarh'


li_of_url= [url1,url2,url3,url4,url5,url6,url7,url8]
# url1,url2,url3,url4,url5,url6,url7

job_title=[]
companies=[]
locations=[]
salaries=[]
summaries=[]
urls=[]
date=[]

max_results=20   
df=pd.DataFrame(columns=['Job Title','Company','Location','Salary','Summary','URL','Date Posted'])
    
for url in li_of_url:
    for start in range(0,max_results,10):

        URL = url+'&start='+str(start)

        time.sleep(1)
        #conducting a request of the stated URL above:
        req=Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
        uClient=uReq(req)

        #offloads the content into a variable
        page_html= uClient.read()
        uClient.close()

        #html parsing
        soup= BeautifulSoup(page_html,'lxml')

        for div in soup.find_all(name='div', attrs={'class':'title'}):
            for a in div.find_all(name='a', attrs={'data-tn-element':'jobTitle'}):
                job_title.append(a['title'])


        for div in soup.find_all(name='div', attrs={'class':'row'}):
            company = div.find_all(name='span', attrs={'class':'company'})
            if len(company) > 0:
                for b in company:
                    companies.append(b.text.strip())
            else:
                sec_try = div.find_all(name='span', attrs={'class':'result-link-source'})
                for span in sec_try:
                    companies.append(span.text.strip())

        for div in soup.find_all(name='div', attrs={'class':'row'}):
            c = div.find_all('span',attrs={'class':'location'})
            for span in c:
                locations.append(span.text)

        for div in soup.find_all(name='div', attrs={'class':'row'}): 
             d= div.find_all('div',attrs={'class':'location'})
             for div in d:
                 locations.append(div.text)

        for div in soup.find_all(name='div', attrs={'class':'row'}):
            try:
                salary = div.find('span', {'class':'no-wrap'}).text.strip()
                salaries.append(salary)
            except:
                salary = 'Nothing Found'
                salaries.append(salary)

        for div in soup.find_all(name='div', attrs={'class':'row'}):
            for d in div.find_all('div',attrs={'class':'title'}):
                for a in d.find_all('a'):
                    l=a.get('href')
                    link='https://www.indeed.co.in'+l
                    urls.append(link)


        for div in soup.find_all(name='div', attrs={'class':'row'}): 
            for span in div.find_all(name='span',attrs={'class':'date'}):
                tex=span.text
                date.append(tex)

        for div in soup.find_all(name='div', attrs={'class':'row'}):
            for span in div.find_all(name='span',attrs={'class':'sponsoredGray'}):
                tex=span.text
                date.append(tex)

for url in urls:
    
    my_url=url
    #opening up the connection, grabbing the url
    req=Request(my_url, headers={'User-Agent': 'Chrome/70.0.3538.77'})

    uClient=uReq(req)

    #offloads the content into a variable
    page_html= uClient.read()
    uClient.close()

    #html parsing
    page_soup= BeautifulSoup(page_html,"lxml")
    posting = page_soup.find(name='div', attrs={'class': "jobsearch-JobComponent"}).get_text()
    summaries.append(posting)

df['Job Title']=job_title
df['Company']=companies
df['Location']=locations
df['Salary']=salaries
df['Summary']=summaries
df['URL']=urls
df['Date Posted']=date

df=df.drop_duplicates()

df=df[df.Company!='2much Jobs']
df=df[df.Company!='GK Software Solutions pvt ltd']
df=df[df.Company!='Edulink Info Services']
df=df[df.Company!='Kapasa Jobs']
df=df[df.Company!='Bhatia Consultancy Services']
df=df[df.Company!='Nexgen Unisoft Industries pvt ltd']
df=df[df.Company!='LAKSHYA']
df=df[df.Company!='T & A Solutions']

df.to_csv(r'/home/user8/Desktop/job_list.csv',index=True)
