import os
from chardet import detect
from bs4 import BeautifulSoup
import csv
import re


# get file encoding type
def get_encoding_type(file):
    with open(file, "rb") as f:
        rawdata = f.read()
    return detect(rawdata)["encoding"]


# Получение названия паблика в формате <имя> <Ссылка>
def getName(s: str) -> str:
    match = re.search(r'<a href="(.*?)">(.*?)</a>', s)
    if match:
        return [f"{match.group(2)}", f"{match.group(1)}"]
    return []


# Создание таблицы
def GetCSV(rowList):
    with open("profile.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rowList)


FileName = "subscriptions1.html"
# Гении из вк используют не utf-8, а windows-1251. Спасибо им
# за 20 веселых минут непонимания, почему у меня не работает File.read()
from_codec = get_encoding_type(FileName)
File1 = open(FileName, encoding=from_codec)

a = File1.read()
soup = BeautifulSoup(a, "html.parser")
SoupResult = soup.find_all("a")

# Замена амперсанта реплейсом, чтобы таблица нормально обрабатывала значение
ResultForCSV = [
    getName(str(i).replace("&amp;", "&")) for i in SoupResult if getName(str(i))
]
GetCSV(ResultForCSV)
File1.close()
