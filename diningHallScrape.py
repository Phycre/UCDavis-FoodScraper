import sys
import requests
from bs4 import BeautifulSoup
from plyer import notification 

specialFoods = ["BYO ", "Lasagna"]

# urls for each dining hall
urlS = "https://housing.ucdavis.edu/dining/menus/dining-commons/segundo/"
urlC = "https://housing.ucdavis.edu/dining/menus/dining-commons/cuarto/"
urlT = "https://housing.ucdavis.edu/dining/menus/dining-commons/tercero/"

urls = []

response = None
food_data = {}

def printAllFoods():
    for day, meals in food_data.items():
        print(f"\n{day}")
        for meal, foods in meals.items():
            print(f"  {meal}:")
            for food in foods:
                print(f"    - {food}")

def searchForFood():
    for day, meals in food_data.items():
        for meal, foods in meals.items():
            for food in foods:
                for specialFood in specialFoods:
                    if specialFood in food:
                        print(f"{day} {meal} {food}")
                        sendNotification(day, meal, food)

def sendNotification(day, meal, food):
    notification.notify(
        title=f"Special Food Found: {food}",
        message=f"On {day}, {meal}: {food}",
        timeout=10 
    )

def sortData(content):
    soup = BeautifulSoup(content, 'html.parser')
    days = soup.find_all('div', id=lambda x: x and x.startswith('tab'))
    for day in days:
        day_name = day.find('h3').text.strip()
        food_data[day_name] = {}
        current_meal = None
        for element in day.find_all(['h4', 'li']):
            if element.name == 'h4':  # breakfast/lunch/dinner
                current_meal = element.text.strip()
                food_data[day_name][current_meal] = []
            elif element.name == 'li' and current_meal:  # individual items
                span = element.find('span')
                if span:  # fix empty
                    food_item = span.text.strip()
                    food_data[day_name][current_meal].append(food_item)

def fetchData(urlLink):
    global response
    response = requests.get(urlLink)
    content = response.text
    sortData(content)

if len(sys.argv) < 2:
    print("Usage: python diningHallScrape.py [-P] to print whole menu, [-L] to search for special food, [-S] for Segundo, [-C] for Cuarto, [-T] for Tercero, [-A] for all halls")
else:
    if "-S" in sys.argv:
        urls.append(urlS)
    if "-C" in sys.argv:
        urls.append(urlC)
    if "-T" in sys.argv:
        urls.append(urlT)
    if "-A" in sys.argv:
        urls = [urlS, urlC, urlT]

    if "-P" in sys.argv:
        for url in urls:
            print(url[56:63])
            fetchData(url)
            printAllFoods()
    elif "-L" in sys.argv: 
        for url in urls:
            print(url[56:63])
            fetchData(url)
            searchForFood()
    else:
        print("Invalid argument. Usage: python diningHallScrape.py [-P] to print whole menu, [-L] to search for special food, [-S] for Segundo, [-C] for Cuarto, [-T] for Tercero, [-A] for all halls")

