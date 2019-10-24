#!/usr/bin/env python
# coding: utf-8

# # Dependencies

# In[1]:



from bs4 import BeautifulSoup
import requests
import pymongo
import pandas as pd
from splinter import Browser
from selenium import webdriver


# In[2]:


executable_path = {"executable_path": "chromedriver.exe"}


# In[3]:


# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)


# In[ ]:





# # NEWS ARTICLE

# In[4]:





# In[68]:


def recentMarsNews():
    url ='https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser=Browser("chrome", **executable_path, headless=False)
    browser.visit(url)
    html=browser.html
    browser.quit()
    soup = BeautifulSoup(html, "html.parser")
    title=soup.find('div', class_="content_title").text
    text=soup.find('div', class_="rollover_description_inner").text
    return(title, text)


# In[70]:




# In[7]:





# # Full-size image

# In[9]:





# In[63]:

def findMarsPic():
    import time
    img_url_pg="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    img_browser=Browser("chrome", **executable_path, headless=False)
    img_browser.visit(img_url_pg)
    img_browser.click_link_by_partial_text('FULL')
    time.sleep(5)
    img_browser.click_link_by_partial_text('more info')
    img_html=img_browser.html
    img_soup=BeautifulSoup(img_html, "html.parser")
    img=img_soup.find('figure', class_="lede")
    img=img.a['href']
    
      
    featured_img="https://www.jpl.nasa.gov"+img
    img_browser.quit()

    return(featured_img)

# In[64]:




# # Mars Weather:

# In[53]:





# In[65]:


def currentMarsWeather():
    weather_url="https://twitter.com/marswxreport?lang=en"
    weather_browser=Browser("chrome", **executable_path, headless=False)
    weather_browser.visit(weather_url)
    weather_html=weather_browser.html
    weather_soup=BeautifulSoup(weather_html, 'html.parser')
    weather_browser.quit()
    print(weather_soup.find('div', class_="js-tweet-text-container").text)
    return (weather_soup.find('div', class_="js-tweet-text-container").text)


# In[66]:




# In[ ]:





# In[ ]:





# # Mars Facts:

# In[92]:


def getMarsFacts():
    fact_url="https://space-facts.com/mars/"
    fact_browser=Browser("chrome", **executable_path, headless=False)
    fact_browser.visit(fact_url)
    fact_table=(pd.read_html(fact_browser.html))
    fact_table=fact_table[1]
    fact_table.columns=['Mars', 'Data']
    fact_table=fact_table.to_html(classes='marsinformation')
    fact_table=fact_table.replace('\n', ' ')    
    fact_browser.quit()
   
    return (fact_table)

# In[93]:




# # Mars Hemispheres

# In[120]:


def getMarsHems():
    base="https://astrogeology.usgs.gov"
    hems_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    hems_browser=Browser("chrome", **executable_path, headless=False)
    hems_browser.visit(hems_url)
    hems_soup=BeautifulSoup(hems_browser.html, 'lxml')
    hems_browser.quit()
    list_img_url=[]
    for x in hems_soup.find_all('div', class_="item"):
        linkx=base+ x.find('a')["href"]
        list_img_url.append(linkx)
    print(getEnchancedMarsImg(list_img_url))
    return(getEnchancedMarsImg(list_img_url))


# In[140]:


def getEnchancedMarsImg(url_list):
    base="https://astrogeology.usgs.gov"
    browserx=Browser("chrome", **executable_path, headless=False)
    hemisphere_image_urls=[]
    for x in url_list:
        browserx.visit(x)
        xsoup=BeautifulSoup(browserx.html, 'lxml')
        title=xsoup.find('title').text
        title=title.split(" |")
        title=title[0]
        for u in xsoup.find_all('img', class_="wide-image"):
            img_link=base+u["src"]
        img_dic={"title":title, 
                "img_url":img_link}
        hemisphere_image_urls.append(img_dic)
        
    browserx.quit()
    return(hemisphere_image_urls)
        
       
       


# In[141]:





# In[ ]:

def scrape():
    results={"news": recentMarsNews(),
    "MarsPic": findMarsPic(), 
    "weather":currentMarsWeather(), 
    "facts_table":getMarsFacts(), 
    "MarsHems":getMarsHems()
    }
    return(results)


