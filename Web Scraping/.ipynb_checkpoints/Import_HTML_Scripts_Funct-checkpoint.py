import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

def scroll(url):
    # For URLs with infinite scroll feature or permissions
    driver = webdriver.Chrome()
    driver.get(url)

    screen_height = driver.execute_script("return window.screen.height;")  # Browser window height
    i = 1
    while True:
        # Scroll down
        driver.execute_script(f"window.scrollTo(0, {screen_height * i});")
        i += 1
        time.sleep(1)
    
        # Check if reaching the end of the page
        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        if screen_height * i > scroll_height:
            break
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    return soup

def request(url):
    # For URLs with no permissions
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup

def mult_page(url, func, num):
    # att should be the attribute = "..." ex. id = "next"
    soups = [] # will return a list of HTML scripts
    soup = func(url)
    for i in range(num):
        soups.append(soup)
        next = soup.find("link", rel="next").get("href") # adjust the tag and attributes for the rights ones
        soup = func(str(next))
    return soups 