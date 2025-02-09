import requests
from bs4 import BeautifulSoup

# URL страницы с хакатонами
url = "https://www.xn--80aa3anexr8c.xn--p1ai/"

# Отправляем GET-запрос
response = requests.get(url)
response.raise_for_status()

# Разбираем HTML-код
soup = BeautifulSoup(response.text, "lxml")

# Ищем контейнер с данными о хакатоне
hackathon_div = soup.find("div", class_="t776__col")

# Получаем ссылку
link = hackathon_div.find("a", class_="js-product-link")["href"]

# Название хакатона
title = hackathon_div.find("div", class_="t776__title").text.strip()

# Описание
description = hackathon_div.find("div", class_="t776__descr").text.strip()

print(f"Название: {title}")
print(f"Ссылка: {link}")
print(f"Описание: {description}")