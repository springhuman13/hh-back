import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from app.crud import create_hackathon
from app.models import Hackathon


possible_location = [
    "Онлайн", "Офлайн", "Online", "Ofline", "г.",
    "Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Нижний Новгород",
    "Казань", "Челябинск", "Омск", "Самара", "Ростов-на-Дону", "Уфа", "Красноярск",
    "Пермь", "Воронеж", "Волгоград", "Краснодар", "Тюмень", "Иркутск", "Тула", "Барнаул"
]

def parse_description(description: str):
    place, dates, organizers, tech_focus = None, None, None, None

    parts = description.split("<strong>")

    for part in parts:
        part = part.strip()
        part = part.replace("<br>", "").replace("<br/>", "").replace("<strong>", "").replace("</strong>", "")

        if any(part.startswith(location) for location in possible_location):
            place = part
        elif "Хакатон:" in part:
            dates = part.replace("Хакатон:", "").strip()
        elif "Организаторы:" in part or "Организатор:" in part:
            organizers = part.replace("Организаторы:", "").replace("Организатор:", "").strip()
        elif "Технологический фокус:" in part:
            tech_focus = part.replace("Технологический фокус:", "").strip()

    return place, dates, organizers, tech_focus


def parse_hackathons(url: str, db: Session):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    hackathon_divs = soup.find_all("div", class_="t776__content")

    for hackathon_div in hackathon_divs:
        title = hackathon_div.find("div", class_="t776__title").text.strip()
        description = hackathon_div.find("div", class_="t776__descr").decode_contents().strip()
        link = hackathon_div.find("a", class_="js-product-link")["href"]
        img = hackathon_div.find("div", class_="t776__bgimg")["data-original"]

        place, dates, organizers, tech_focus = parse_description(description)

        if db.query(Hackathon).filter(Hackathon.link == link).first():
            continue

        create_hackathon(
            db,
            title=title,
            description=description,
            link=link,
            img=img,
            place=place,
            dates=dates,
            organizers=organizers,
            tech_focus=tech_focus,
        )
