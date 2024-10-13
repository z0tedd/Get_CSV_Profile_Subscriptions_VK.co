# Парсинг подписок профиля ВК

## Первое, что необходимо - запросить архив со своими данными

https://vk.com/faq18145

![image](https://github.com/user-attachments/assets/698a2dc0-c3dc-42d8-bbfa-4e8cf685d2fc)
![image](https://github.com/user-attachments/assets/282b4d7b-6986-4b1f-8d4c-a6e222fe4a64)


Спустя несколько дней вам придет сообщение о том, что архив подготовлен и его можно скачать
![image](https://github.com/user-attachments/assets/82bdf53f-cd86-4099-a369-f339939f9609)


Открываем архив, заходим в папку profile, видим html файлы с названием subscription0. Их мы и будем парсить.

![image](https://github.com/user-attachments/assets/544b62ba-b6ca-4c53-a1c4-2ba521dfe231)

![image](https://github.com/user-attachments/assets/985ba51d-0abd-4d5e-8c1a-5e788d2fd42f)


Код для обработки(кидаем его в папку profile, меняем название файла и запускаем):

```python
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

```

Получаем profile.csv, который читается экселем - Все готово!
![image](https://github.com/user-attachments/assets/b0dd57b7-f1d1-49ce-98e2-8cad966f69f6)
