# Dependencies
import os
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import pandas as pd
import time

def scrape():

    # Initialize Splinter for Windows Users
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    #--------NASA Mars News ---------
    # URL of page to be scraped
    NASA_News_url = 'https://mars.nasa.gov/news/'
    browser.visit(NASA_News_url)

    news_title = NASA_Mars_News_soup.find('div', class_ = 'content_title').text

    #This is not consistently running correct
    news_p = NASA_Mars_News_soup.find('div', class_ = 'article_teaser_body').text

    #---------JPL Mars Space Images - Featured Image----------
    # URL of page to visit
    JPL_Mars_Images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(JPL_Mars_Images_url)
    time.sleep(5)

    # Click on first button
    browser.click_link_by_id('full_image')
    time.sleep(5)

    # Click again
    browser.click_link_by_partial_text('more info')
    time.sleep(5)

    # Create Soup Object from the JPL Mars Space Images URL
    html = browser.html
    JPL_Mars_Images_soup = bs(html, 'html.parser')

    # find the relative image url
    relative_img_url = JPL_Mars_Images_soup.select_one('figure.lede a img')
    

    #I found that the execution of this code is unreliable unless I put in some delays.  Maybe I am wrong.
    time.sleep(10)

    figure = JPL_Mars_Images_soup.find('figure')
    relative_mars_image_url = figure.find('a')['href']
    mars_image_url = f'https://www.jpl.nasa.gov{relative_mars_image_url}'

    #-------------Mars Facts ---------------------
    #Read Mars Facts into dataframe --- returns a list of DataFrame objects
    Mars_Facts_df = pd.read_html('https://space-facts.com/mars/')[0]

    #Set Column Names and set index to description column
    Mars_Facts_df.columns=['description', 'value']
    Mars_Facts_df.set_index('description', inplace=True)

    Mars_Facts = Mars_Facts_df.to_html('Mars_Facts_table.html')
    
    #--------------- Mars Hemispheres ------------------------
    # URL of page to be scraped
    Mars_Hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(Mars_Hemisphere_url)
    # Create Soup Object from the Mars Hemisphere Web Page
    html=browser.html
    Mars_Hemisphere_soup= bs(html, 'html.parser')

    # Retreive all items that contain mars hemispheres information
    hemisphere_items = Mars_Hemisphere_soup.find_all('div', class_='item')
    # Create an empty list to store scraped hemisphere urls 
    hemisphere_image_urls = []
    # Variable for the main web site 
    hemispheres_main_url = 'https://astrogeology.usgs.gov'

    # Loop through the hemisphere items
    for i in hemisphere_items: 
        # Store hemisphere title
        hemisphere_title = i.find('h3').text
    
        # Store link that leads to full image website
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
    
        # Visit the complete image url 
        browser.visit(hemispheres_main_url + partial_img_url)
    
        # Create HTML Object of individual hemisphere image information 
        partial_img_html = browser.html
    
        # Create soup object using partial image url 
        partial_img_soup = bs( partial_img_html, 'html.parser')
    
        # Create complete image source url
        complete_img_url = hemispheres_main_url + partial_img_soup.find('img', class_='wide-image')['src']
    
        # Add title/image url dictionaries to hemisphere_image_urls list
        hemisphere_image_urls.append({"title" : hemisphere_title, "img_url" : complete_img_url})



    mars_information = {
        'news_title': news_title,
        'news_paragraph': news_p,
        'mars_image_url': mars_image_url,
        'mars_facts_html': Mars_Facts,
        'mars_hemispheres': hemisphere_image_urls
    }

    #print(scrape())

    return mars_information



