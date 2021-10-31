# My-Captain-python-5-

import requests
from bs4 import BeautifulSoup
import pandas
import argparse
import connect

parser = argparse.ArgumentParser()
parser.add_argument("--page_num_Max", help="enter the number of page to parse", type= int)
parser.add_argument("--dbname", help="enter the name of db", type=str)
args = parser.parse_args()

oyo_url = "https://www.oyorooms.com/hotels-in-bangalore//?page="
page_num_Max = args.page_num_max
scraped_info_list = []
connect.connect(args.dbname)

for page_num in range(1,page_num_Max):
  url = oyo_url+str(page_num)
  print("get request for: "+url)
  req = request.get(url)
  content = req.content

  soup= BeautifulSoup(content, "html.parser")

  all_hotels = soup.find_all("div",{"class": "hotelcardListing"})

  for hotel in all_hotels:
    hotel_dict= {}
    hotel_dict["name"]= hotel_name=hotel.find("h3",{"class": "ListingHoteldescription_hotelName"}).text
    hotel_dict["address"]= hotel_address = hotel.find("span",{"itemprop": "streetAddress"}).text
    hotel_dict["price"]= hotel_price= hotel.find("span",{"class": "listingPrice__finalPrice"}).text
    #try__except
    try:
      hotel_dict["rating"]= hotel_rating= hotel.find("span",{"class": "hotelRating__ratingSummary"}).text
    except AttributeError:
      hotel_dict["rating"]= None
  
    parent_amenities_element =hotel.find("div",{"class": "amentyWrapper"})
  
    amenities_list=[]
    for amenity in parent_amenities_element.find_all("div",{"class": "amentyWrapper__amenity"}):
                                                   amenities_list.append(amenity.find("span", {"class": "d-body-sm"}).text.strip())
    hotel_dict["amenities"]= ', '.join(amenities_lis[:-1])
  
    scraped_info_list.append(hotel_dict)
    connect.insert_into_table(args.dbname, tuple(hotel_dict.values()))
  
    #print(hotel_name, hotel_address,hotel_price, hotel_rating ,amenities_list)
  
dataFrame = pandas.DataFrame(scraped_info_list)
print("creating csv file....")
dataFrame.to_csv("Oyo.csv")
connect.get_hotel_info(args.dbname)
 
