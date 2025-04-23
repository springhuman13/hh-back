import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from app.service.hackathon_service import HackathonService
from app.models import Hackathon


class HackathonParser:
    def __init__(self, db: Session):
        self.db = db
        self.service = HackathonService(db)

    def parse(self):
        response = requests.get("https://www.xn--80aa3anexr8c.xn--p1ai/")
        soup = BeautifulSoup(response.text, "lxml")
        hackathon_divs = soup.find_all("div", class_="t776__col")

        for div in hackathon_divs:
            title = div.find("div", class_="t776__title").text.strip()
            print(title)
            description_html = div.find("div", class_="t776__descr").decode_contents().strip()
            print(description_html)
            link = div.find("a", class_="js-product-link")["href"]
            print(link)
            img = div.find("div", class_="t776__bgimg")["data-original"]
            print(img)

            # Пропускаем уже существующий хакатон
            if self.db.query(Hackathon).filter_by(website=link).first():
                continue

            place, dates, organizers, tech_focus, online = self._parse_description(description_html)

            self.service.process_hackathon(
                title=title,
                link=link,
                img=img,
                place=place,
                dates=dates,
                organizers=organizers,
                tech_focus=tech_focus,
                online=online
            )

    def _parse_description(self, description: str):
        possible_location = [
            "Онлайн", "Офлайн", "Online", "Ofline", "г.",
            "Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Нижний Новгород",
            "Казань", "Челябинск", "Омск", "Самара", "Ростов-на-Дону", "Уфа", "Красноярск",
            "Пермь", "Воронеж", "Волгоград", "Краснодар", "Тюмень", "Иркутск", "Тула", "Барнаул"
        ]

        place, dates, organizers, tech_focus, online = None, None, None, None, False
        parts = description.split("<strong>")

        for part in parts:
            part = part.strip().replace("<br>", "").replace("<br/>", "").replace("</strong>", "")

            if any(part.startswith(loc) for loc in possible_location):
                place = part
                if "Онлайн" in part or "Online" in part:
                    online = True
            elif "Хакатон:" in part:
                dates = part.replace("Хакатон:", "").strip()
            elif "Организаторы:" in part or "Организатор:" in part:
                organizers = part.replace("Организаторы:", "").replace("Организатор:", "").strip()
            elif "Технологический фокус:" in part:
                tech_focus = part.replace("Технологический фокус:", "").strip()

        return place, dates, organizers, tech_focus, online
