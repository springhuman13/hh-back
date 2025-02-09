import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from app.crud import create_hackathon
from app.models import Hackathon

def parse_hackathons(url: str, db: Session):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    hackathon_divs = soup.find_all("div", class_="t776__col")

    for hackathon_div in hackathon_divs:
        title = hackathon_div.find("div", class_="t776__title").text.strip()
        description = hackathon_div.find("div", class_="t776__descr").text.strip()
        link = hackathon_div.find("a", class_="js-product-link")["href"]

        existing_hackathon = db.query(Hackathon).filter(Hackathon.link == link).first()
        if existing_hackathon:
            # Пропускаем хакатон, если ссылка уже существует
            continue
        existing_hackathon = db.query(Hackathon).filter(Hackathon.description == description).first()
        if existing_hackathon:
            # Пропускаем хакатон, если ссылка уже существует
            continue
        existing_hackathon = db.query(Hackathon).filter(Hackathon.title == title).first()
        if existing_hackathon:
            # Пропускаем хакатон, если ссылка уже существует
            continue

        create_hackathon(db, title, description, link)
