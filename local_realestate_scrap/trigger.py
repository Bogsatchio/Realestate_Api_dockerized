import os
from datetime import datetime

folder_path = r"C:\Users\ADMIN\Desktop\Pliki\Data_Stuff\Python\API_real_estate\data"


def get_cities_to_scrap(path):
    files = os.listdir(path)
    city_date_dict = {}
    for file in files:
        parts = file.split("_")
        date_str = parts[0][:10]
        date = datetime.strptime(date_str, "%Y-%m-%d")
        city = parts[1]
        try:
            if city_date_dict[city] < date:
                city_date_dict[city] = date
        except:
            city_date_dict[city] = date
        #print(date, city)
    cities_to_scrap = list(trigger_dict.keys())
    not_to_scrap = []
    for city, s_date in city_date_dict.items():
        difference = (datetime.now() - s_date).days
        if difference < 7:
            cities_to_scrap.remove(city)
    #print(cities_to_scrap)
    # cities_to_scrap = []
    # for city, s_date in city_date_dict.items():
    #     difference = (datetime.now() - s_date).days
    #     if difference >= 7:
    #         cities_to_scrap.append(city)
    return cities_to_scrap

trigger_dict = {
    "Plock": ["Plock", 30, 100],
    "Opole": ["Opole", 50, 65],
    "Warszawa-Wola": ["Warszawa-Wola", 50, 65],
    "Targowek": ["Targowek", 50, 70],
    "Torun": ["Torun", 50, 60],
    "Radom": ["Radom", 50, 65],
    "Wroclaw-Srodmiescie": ["Wroclaw-Srodmiescie", 50, 65],
    "Wroclaw-Gaj": ["Wroclaw-Gaj", 50, 70]
}

