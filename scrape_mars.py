#Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://redplanetscience.com/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    find_element = soup.select_one("section.image_and_description_container div.container div.col-md-12 div.row div.col-md-8 div.list_text")
    find_element.find("div", class_="content_title")

    #News title
    title = find_element.find("div", class_="content_title").get_text()
    print(title)

    #News paragraph
    paragraph = find_element.find("div", class_="article_teaser_body").get_text()
    print(paragraph)

    #Quit Browser
    browser.quit()

    #Visit other site
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://spaceimages-mars.com/"
    browser.visit(url)

    #Find image url
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    find_element = soup.select_one("div.header img.headerimage")
    image_url = find_element['src']
    featured_image_url = f"https://spaceimages-mars.com/{image_url}"
    print(featured_image_url)

    #Quit Browser
    browser.quit()

    #Scrape table
    mars_facts = pd.read_html("https://galaxyfacts-mars.com")[1]
    print(mars_facts)
    mars_facts.reset_index(inplace=True)
    mars_facts.columns=["Id","Properties", "Values"]
    mars_facts.drop(["Id"], axis=1, inplace=True)
    mars_facts = mars_facts.to_html()

    #Visit other site
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://marshemispheres.com/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image_urls = []

    #Loop through hemispheres
    links = browser.find_by_css("a.itemLink.product-item")
    for link in links:
        hemisphere = {}
        
        #Link
        hemisphere["img_url"] = link['href']
        
        #Title
        hemisphere["title"] = link.text
        
        #Append Hemisphere Object to List
        image_urls.append(hemisphere)
    image_urls

    #Clean
    image_urls.pop(0)
    image_urls.pop(1)
    image_urls.pop(2)
    image_urls.pop(3)
    image_urls.pop(4)
    image_urls

    #Quit Browser
    browser.quit()

    #Put into Dictionary
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    data = {
        "title": title,
        "paragraph": paragraph,
        "featured_image": image_url,
        "facts": mars_facts,
        "hemispheres": image_urls,
    }
    browser.quit()
    return data 

if __name__ == "__main__":
    print(scrape())