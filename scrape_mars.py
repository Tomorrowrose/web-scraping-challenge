#!/usr/bin/env python
# coding: utf-8



from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd



def scrape_info(): 

    mars = {}
    browser = Browser("chrome")




    url = "https://mars.nasa.gov/news/"
    browser.visit(url)





    soup = BeautifulSoup(browser.html, "html.parser") 
    result = soup.find_all('div',class_="content_title")
    news_title = result[1].a.text
    news_title


    # In[5]:


    paragraph = soup.find('div',class_="article_teaser_body")
    news_p = paragraph.get_text()
    news_p





    mars["news_title"] = news_title
    mars["news_p"] = news_p
    mars





    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url) 
    time.sleep(2) 
    browser.find_by_id("full_image").click()
    time.sleep(2)
    browser.find_link_by_partial_text("more info").click()
    time.sleep(2)
    soup = BeautifulSoup(browser.html, "html.parser") 
    link = soup.find('figure',class_="lede")
    result_link = link.a.img["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + result_link
    featured_image_url



    mars["featured_image"] = featured_image_url





    url = "https://space-facts.com/mars/"
    table = pd.read_html(url) 
    df = table[0]
    df.columns = ["Attribute", "Values"]
    df





    html_table = df.to_html()
    html_table = html_table.replace('\n', " ")





    mars["facts"] = html_table
    mars





    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)





    hemisphere_image_urls = []
    links = browser.find_by_css("a.product-item h3")
    for i in range(len(links)):
        hemisphere = {}
        # We have to find the elements on each loop to avoid a stale element exception
        browser.find_by_css("a.product-item h3")[i].click()
        # Next, we find the Sample image anchor tag and extract the href
        sample_elem = browser.links.find_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']
        # Get Hemisphere title
        hemisphere['title'] = browser.find_by_css("h2.title").text
        # Append hemisphere object to list
        hemisphere_image_urls.append(hemisphere)
        # Finally, we navigate backwards
        browser.back()





    hemisphere_image_urls



    mars["hemisphere"] = hemisphere_image_urls

    return mars

if __name__ == "__main__":
    print(scrape_info())



