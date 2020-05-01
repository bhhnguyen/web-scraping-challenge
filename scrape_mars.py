from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import os
import pandas as pd
import requests


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()
    scrape_dict = {}

    #Mars News
    try:
        url = "https://mars.nasa.gov/news/"
        browser.visit(url)
        html = browser.html
        soup = bs(html, "lxml")
        browser.is_element_present_by_tag('li', wait_time=30)
        item_list = soup.find("ul", class_="item_list")
        slides = item_list.find_all("li", class_="slide")
        content_title = slides[0].find("div", class_="content_title").text
        article_body = slides[0].find("div", class_="article_teaser_body").text
        scrape_dict['news_title'] = content_title
        scrape_dict['news_p'] = article_body
    except:
        print("Could not scrape news.")

    #JPL
    try:
        url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
        browser.visit(url)
        html = browser.html
        soup = bs(html, "lxml")
        browser.is_element_present_by_tag('section', wait_time=30)
        carousel = soup.find("section", class_="grid_gallery module grid_view")
        space_img = carousel.find("a", class_="fancybox")['data-fancybox-href']
        space_img = os.path.join("https://www.jpl.nasa.gov/", space_img[1:])
        scrape_dict['featured_image_url'] = space_img
    except:
        print("Could not scrape image.")

    #Twitter
    try:
        url = "https://twitter.com/marswxreport?lang=en"
        response = requests.get(url)
        # Scrape page into Soup
        soup = bs(response.text, "lxml")
        tweet_container = soup.find("div", class_="js-tweet-text-container")
        tweet_text = tweet_container.text
        scrape_dict['mars_weather'] = tweet_text.replace('\n', '')
    except:
        print("Could not scrape weather.")

    #Space Facts
    try:
        url = "https://space-facts.com/mars/"
        tables = pd.read_html(url)
        df = tables[0]
        scrape_dict['table_html'] = df.to_html(header=False,index=False).replace('\n', '')
    except:
        print("Could not scrape fact table.")

    #Hemispheres
    try:
        url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(url)
        time.sleep(10)
        hemis = []
        links = browser.find_by_css("a.product-item h3")
        for x in range(len(links)):
            hemi = {}
            browser.find_by_css("a.product-item h3")[x].click()
            time.sleep(5)
            img = browser.links.find_by_text("Sample").first
            hemi['title'] = browser.find_by_css("h2.title").text
            hemi['img_url'] = img['href']
            hemis.append(hemi)
            browser.back()
            time.sleep(5)
        scrape_dict['hemisphere_img_urls'] = hemis
    except:
        print("Could not scrape hemispheres.")


    # Quit the browser after scraping
    browser.quit()
    # Return results
    return scrape_dict

if __name__ == "__main__":
    data = scrape_info()
    print(data)