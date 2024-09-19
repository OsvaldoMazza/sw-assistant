# Importing necessary libraries
import requests
from bs4 import BeautifulSoup

def get_weather(city, days=None):
    url = "https://www.google.com/search?q=" + "weather" + city
    if days != None:
        url += f" in {days} days"

    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')

    # Extracting the temperature
    temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text

    # Extracting the time and sky description
    str_ = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
    data = str_.split('\n')
    sky = data[1]

    # Getting all div tags with the specific class name
    listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})

    # Extracting other required data
    strd = listdiv[5].text
    pos = strd.find('Wind')
    other_data = strd[pos:]

    if days == None:
        phrase = f"La temperatura en {city} es {temp}, y el cielo está {sky}."
    else:
         phrase = f"La temperatura en {city} será {temp} en {days}, y el cielo estará {sky}."

    if len(other_data) > 5:
        phrase += other_data

    print(f"Google weather: {phrase}")

    return phrase
