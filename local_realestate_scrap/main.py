from scrapping_nieruchomosci import scrap_real_estate_data
from trigger import trigger_dict, get_cities_to_scrap

folder_path = r"C:\Users\ADMIN\Desktop\Pliki\Data_Stuff\Python\API_real_estate\data"

cities_to_scrap = get_cities_to_scrap(folder_path)
for city in cities_to_scrap[-2:]:
    #print(cities_to_scrap)
    print(city)
    scrap_real_estate_data(trigger_dict[city][0], trigger_dict[city][1], trigger_dict[city][2])

