from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup, Tag, ResultSet, NavigableString

def parse_offer(offer: Tag) -> dict:
  return {
    "title": parse_title(offer)
  }

def parse_title(offer: Tag) -> str:
  title_tags: ResultSet = offer.find_all("h3")
  title_tag: NavigableString = title_tags[0]
  return title_tag.text.strip()

def main():
  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument("--headless")
  driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
  driver.get("https://nofluffjobs.com/pl/?lang=en")
  source = BeautifulSoup(driver.page_source, "html.parser")
  offers: ResultSet = source.find_all("a", class_="posting-list-item")
  for offer in offers:
    print(offer.prettify())
  
if __name__ == "__main__":
  main()