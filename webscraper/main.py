from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup, Tag, ResultSet, NavigableString
from pandas import DataFrame
import time

def toInt(x: str) -> int | None:
  try:
    return int(x)
  except:
    return None

def parse_offer(offer: Tag) -> dict:
  pay_range: tuple[int, int, bool] = parse_pay_range(offer)
  return {
    "title": parse_title(offer),
    "category": parse_category(offer),
    "technologies": parse_technologies(offer),
	  "company": parse_company(offer),
	  "minimum_pay": pay_range[0],
	  "maximum_pay": pay_range[1],
    "check_salary_match": pay_range[2]
  }

def parse_title(offer: Tag) -> str:
  title_tag: NavigableString = offer.find("h3")
  return title_tag.text.strip()

def parse_category(offer: Tag) -> str:
  category_container: Tag = offer.find("div", class_="tiles-container")
  category_tag: NavigableString = category_container.find("span")
  return category_tag.text.strip()

def parse_technologies(offer: Tag) -> list[str]:
  technologies_container: Tag = offer.find("div", class_="tiles-container")
  technologies_tags: ResultSet = technologies_container.find_all("span")[1:]
  return [technology_tag.text.strip() for technology_tag in technologies_tags if technology_tag.text.strip() != "•"]

def parse_company(offer: Tag) -> str:
  company_container: Tag = offer.find("footer")
  company_tag: NavigableString = company_container.find("h4")
  return company_tag.text.strip()

def parse_pay_range(offer: Tag) -> tuple[int | None, int | None, bool]:
  pay_range_container: Tag = offer.find("aside", class_="posting-info")
  pay_range_tag: NavigableString = pay_range_container.find("span")
  pay_range: str = " ".join(pay_range_tag.text.strip().split())
  if pay_range == "Check Salary Match":
    return (None, None, True)
  pay_range_as_split = pay_range.split()
  return (toInt("".join(pay_range_as_split[:2])), toInt("".join(pay_range_as_split[3:5])), False)

def main():
  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument("--headless")
  driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
  driver.get("https://nofluffjobs.com/pl/?lang=en")

  #while True:
  for _ in range(0, 20):
    try:
      more_offers_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()=' See more offers ']")))
      driver.execute_script("arguments[0].click();", more_offers_button)
    except Exception as e:
      print(f"Exception: {e}")
      break

  source = BeautifulSoup(driver.page_source, "html.parser")
  offer_tags: ResultSet = source.find_all("a", class_="posting-list-item")
  offers_df: DataFrame = DataFrame([parse_offer(offer) for offer in offer_tags])
  print(offers_df)
  print(offers_df["category"].value_counts())

if __name__ == "__main__":
  main()