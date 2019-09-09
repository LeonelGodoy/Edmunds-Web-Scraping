import pandas as pd
import numpy as np

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import urllib

# list creation
Price = []
Price_integer = []
Mileage = []
Mileage_integer = []
Distance = []
Model = []
VIN = []

def carfax_data(dataframe):
    for n,i in enumerate(df['VIN']):
        link = "https://www.carfax.com/VehicleHistory/p/Report.cfx?partner=EMS_0&vin=" + i
        req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, "html.parser")
        iterate = 0
        for i in soup.find_all('span', class_="wrappingDesc"):
            df.loc[n,str(iterate)] = i.text
            if "Last reported odometer" in i.text:
                break
            iterate += 1

def edmunds_webscraping(link) :
    req = Request(link,headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, "html.parser")
    for i in soup.find_all('h3', class_="mb-0 text-gray-darker"):
        Price.append(i.text)
    for i in soup.find_all('h3', class_="mb-0 text-gray-darker"):
        result = ''.join(i for i in i.text[1:] if i.isdigit())
        Price_integer.append(int(result))
    for i in soup.find_all('span', class_="text-gray-darker ml-0_25"):
        Mileage.append(i.text)
    for i in soup.find_all('span', class_="text-gray-darker ml-0_25"):
        result = ''.join(i for i in i.text[:-6] if i.isdigit())
        Mileage_integer.append(int(result))
    for i in soup.find_all('div', class_="disclaimer text-gray-dark"):
        Distance.append(i.text)
    for i in soup.find_all('a', class_="d-block h5 mb-0"):
        Model.append(i.text)
        VIN.append(i.get('href')[-18:-1])

# iterates through the pages and applys the function above
for num in range(0,19):
    url = ('https://www.edmunds.com/inventory/srp.html?deliverytype=local&price=15000-*&make=lexus&mileage=15000-*&model=gs-350&sort=distance%3Aasc&year=2015-2015&radius=500'+
           '&pagenumber='+
           str(num))
    edmunds_webscraping(url)

df = pd.DataFrame({"Model" : Model, "VIN" : VIN, "Price":Price, "y":Price_integer,
                   "Mileage":Mileage, "X":Mileage_integer,
                   "Distance":Distance})

carfax_data(df)

df['# of Owners'] = df.fillna("NA").apply(lambda row: row['0'] if ("owners" in row['0']) or ("1-Owner" in row['0']) else
                            row['1'] if ("owners" in row['1']) or ("1-Owner" in row['1']) else
                            row['2'] if ("owners" in row['2']) or ("1-Owner" in row['2']) else
                            row['3'] if ("owners" in row['3']) or ("1-Owner" in row['3']) else
                            row['4'] if ("owners" in row['4']) or ("1-Owner" in row['4']) else
                            row['5'] if ("owners" in row['5']) or ("1-Owner" in row['5']) else "NA", axis=1)

df['Accidents'] = df.fillna("NA").apply(lambda row: row['0'] if ("accidents" in row['0']) or ("Accident" in row['0']) else
                            row['1'] if ("accidents" in row['1']) or ("Accident" in row['1']) else
                            row['2'] if ("accidents" in row['2']) or ("Accident" in row['2']) else
                            row['3'] if ("accidents" in row['3']) or ("Accident" in row['3']) else
                            row['4'] if ("accidents" in row['4']) or ("Accident" in row['4']) else
                            row['5'] if ("accidents" in row['5']) or ("Accident" in row['5']) else "NA", axis=1)

df['Damage'] = df.fillna("NA").apply(lambda row: row['0'] if ("damage" in row['0']) or ("Damage" in row['0']) else
                            row['1'] if ("damage" in row['1']) or ("Damage" in row['1']) else
                            row['2'] if ("damage" in row['2']) or ("Damage" in row['2']) else
                            row['3'] if ("damage" in row['3']) or ("Damage" in row['3']) else
                            row['4'] if ("damage" in row['4']) or ("Damage" in row['4']) else
                            row['5'] if ("damage" in row['5']) or ("Damage" in row['5']) else "NA", axis=1)

df['Service'] = df.fillna("NA").apply(lambda row: row['0'] if ("Service" in row['0']) else
                            row['1'] if ("Service" in row['1'])  else
                            row['2'] if ("Service" in row['2'])  else
                            row['3'] if ("Service" in row['3'])  else
                            row['4'] if ("Service" in row['4'])  else
                            row['5'] if ("Service" in row['5'])  else "NA", axis=1)

df['L/CERTIFIED'] = df.fillna("NA").apply(lambda row: row['0'] if ("L/CERTIFIED" in row['0']) else
                            row['1'] if ("L/CERTIFIED" in row['1'])  else
                            row['2'] if ("L/CERTIFIED" in row['2'])  else
                            row['3'] if ("L/CERTIFIED" in row['3'])  else
                            row['4'] if ("L/CERTIFIED" in row['4'])  else
                            row['5'] if ("L/CERTIFIED" in row['5'])  else "NA", axis=1)

df.to_csv("Edmunds_output.csv")
