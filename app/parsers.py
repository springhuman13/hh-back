import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from app.crud import create_hackathon

def parse_hackathon(url: str, db: Session):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    hackathon_div = soup.find("div", class_="t776__col")
    title = hackathon_div.find("div", class_="t776__title").text.strip()
    description = hackathon_div.find("div", class_="t776__descr").text.strip()
    link = hackathon_div.find("a", class_="js-product-link")["href"]

    focuses = []
    for strong in hackathon_div.find_all("strong"):
        if "Технологический фокус" in strong.text:
            focuses = strong.next_sibling.strip().split(", ")

    return create_hackathon(db, title, description, link, focuses)
