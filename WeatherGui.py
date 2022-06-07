#! /usr/bin/env python3
from contextlib import nullcontext
from tkinter import *
from pyowm.owm import OWM
import schedule
from time import time, sleep
import os
import requests
import json
import datetime, pytz
from dotenv import load_dotenv
from PIL import ImageTk, Image
from pandas import DataFrame

load_dotenv()

api_key = os.environ.get("WEATHER_SECRET")
owm = OWM(api_key)

mgr = owm.weather_manager()
my_city_id = 4950191
weather = mgr.weather_at_id(my_city_id).weather 
print("WEATHER", weather)

root = Tk()
root.title("Weather App")
root.geometry("450x850+3441+100")
root['background'] = "white"
  
# Image
# new = ImageTk.PhotoImage(Image.open('IT2.JPG'))
# panel = Label(root, image=new)
# panel.place(x=75, y=520)
  
  
# Dates
dt = datetime.datetime.now()
date = Label(root, text=dt.strftime('%A--'), bg='white', font=("bold", 15))
date.place(x=5, y=130)
month = Label(root, text=dt.strftime('%d %B'), bg='white', font=("bold", 15))
month.place(x=100, y=130)
  
# Time
hour = Label(root, text=dt.strftime('%I : %M %p'),
             bg='white', font=("bold", 15))
hour.place(x=10, y=160)
  
# Theme for the respective time the application is used
if int((dt.strftime('%I'))) >= 8 & int((dt.strftime('%I'))) <= 5:
    img = ImageTk.PhotoImage(Image.open('C:/Users/sampa/OneDrive/Desktop/Python Projects/WeatherGUI/moon.png'))
    panel = Label(root, image=img)
    panel.place(x=210, y=200)
else:
    img = ImageTk.PhotoImage(Image.open('C:/Users/sampa/OneDrive/Desktop/Python Projects/WeatherGUI/sun.png'))
    panel = Label(root, image=img)
    panel.place(x=210, y=200)
  
  
# City Search
# city_name = StringVar()
# city_entry = Entry(root, textvariable=city_name, width=45)
# city_entry.grid(row=1, column=0, ipady=10, stick=W+E+N+S)
# Forecast
    dates = []
    weather_desc = []
    low = []
    high = []
    icons = []
    alerts = []
  
  
def city_name():
    # API Call
    api_request = requests.get("https://api.openweathermap.org/data/2.5/weather?id=4950191" + "&units=imperial&appid="+api_key)
    api_onecall_request = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=41.757721&lon=-70.500137" + "&units=imperial&appid="+api_key)
  
    api = json.loads(api_request.content)
    api_onecall = json.loads(api_onecall_request.content)
    print("sadasda",api_onecall["current"])
    
    
    for index in range( 1, 4):
        local_time = datetime.datetime.fromtimestamp( api_onecall['daily'][index]['dt'], tz=pytz.timezone('US/Eastern'))
        str_time = local_time.strftime('%m/%d - %a')
        print(f"Day [+{index}] {str_time} = low:{api_onecall['daily'][index]['temp']['min']} high: {api_onecall['daily'][index]['temp']['max']}  = {api_onecall['daily'][index]['weather'][0]['description']} ")
        dates.append(str_time)
        weather_desc.append(api_onecall['daily'][index]['weather'][0]['description'])
        icons.append(api_onecall['daily'][index]['weather'][0]['icon'])
        # alerts.append(api_onecall['alerts'][0]['event']) if alerts.append(api_onecall['alerts'][index]['event']) else None
        low.append(api_onecall['daily'][index]['temp']['min'])
        high.append(api_onecall['daily'][index]['temp']['max'])

    
    
    
    # Temperatures
    y = api['main']
    wd = api['weather'][0]
    wm = wd['main']
    description = wd['description']
    current_temprature = y['temp']
    humidity = y['humidity']
    tempmin = y['temp_min']
    tempmax = y['temp_max']
  
    # Coordinates
    x = api['coord']
    longtitude = x['lon']
    latitude = x['lat']
  
    # Country
    z = api['sys']
    country = z['country']
    citi = api['name']
  
    # Adding the received info into the screen
    label_temp.configure(text=current_temprature)
    label_humidity.configure(text=humidity)
    max_temp.configure(text=tempmax)
    min_temp.configure(text=tempmin)
    label_lon.configure(text=longtitude)
    label_lat.configure(text=latitude)
    label_country.configure(text=country)
    label_citi.configure(text=citi)
    label_weather.configure(text=wm)
    label_weather2.configure(text=description)
    day1Min.configure(text=low[0])
  
# # Search Bar and Button
# city_nameButton = Button(root, text="Search", command=city_name)
# city_nameButton.grid(row=1, column=1, padx=5, stick=W+E+N+S)
  
  
# Country  Names and Coordinates

label_citi = Label(root, text="...", width=0, 
                   bg='white', font=("bold", 15))
label_citi.place(x=10, y=63)
  
label_country = Label(root, text="...", width=0, 
                      bg='white', font=("bold", 15))
label_country.place(x=135, y=63)
  
label_lon = Label(root, text="...", width=0,
                  bg='white', font=("Helvetica", 15))
label_lon.place(x=25, y=95)
label_lat = Label(root, text="...", width=0,
                  bg='white', font=("Helvetica", 15))
label_lat.place(x=195, y=95)
  
# Current Temperature
  
label_temp = Label(root, text="...", width=0, bg='white',
                   font=("Helvetica", 50), fg='black')
label_temp.place(x=18, y=220)

label_weather = Label(root, text="...", width=0, bg='white', font=("Helvetica",20), fg='black')
label_weather.place(x=18, y=300)

label_weather2 = Label(root, text="...", width=0, bg='white', font=("Helvetica", 20), fg='black')
label_weather2.place(x=18, y=330)
  
# Other temperature details
  
humi = Label(root, text="Humidity: ", width=0, 
             bg='white', font=("bold", 15))
humi.place(x=3, y=400)
  
label_humidity = Label(root, text="...", width=0,
                       bg='white', font=("bold", 15))
label_humidity.place(x=107, y=400)
  
  
maxi = Label(root, text="Max. Temp.: ", width=0, 
             bg='white', font=("bold", 15))
maxi.place(x=3, y=430)
  
max_temp = Label(root, text="...", width=0, 
                 bg='white', font=("bold", 15))
max_temp.place(x=128, y=430)
  
  
mini = Label(root, text="Min. Temp.: ", width=0, 
             bg='white', font=("bold", 15))
mini.place(x=3, y=460)
  
min_temp = Label(root, text="...", width=0, 
                 bg='white', font=("bold", 15))
min_temp.place(x=128, y=460)

#Forecast
day1Min = Label(root, text='{}'.format(dates[0]), width=0, 
                 bg='white', font=("bold", 15))
day1Min.place(x=10, y=480)
day2Min = Label(root, text="...", width=0, 
                 bg='white', font=("bold", 15))
day3Min = Label(root, text="...", width=0, 
                 bg='white', font=("bold", 15))
day1Max = Label(root, text="...", width=0, 
                 bg='white', font=("bold", 15))
day2Max = Label(root, text="...", width=0, 
                 bg='white', font=("bold", 15))
day3Max = Label(root, text="...", width=0, 
                 bg='white', font=("bold", 15))
day1Icon = Label(root, text="...", width=0, 
                 bg='white', font=("bold", 15))
day2Icon = Label(root, text="...", width=0, 
                 bg='white', font=("bold", 15))
day3Icon = Label(root, text="...", width=0, 
                 bg='white', font=("bold", 15))
day1Description = Label(root, text="...", width=0, 
                 bg='white', font=("bold", 15))
day2Description = Label(root, text="...", width=0, 
                 bg='white', font=("bold", 15))
day3Description = Label(root, text="...", width=0, 
                 bg='white', font=("bold", 15))
day1Date = Label(root, text="...", width=0, 
                 bg='white', font=("bold", 15))
day2Date = Label(root, text="...", width=0, 
                 bg='white', font=("bold", 15))
day3Date = Label(root, text="...", width=0, 
                 bg='white', font=("bold", 15))
  
# Note
# s = sched.scheduler(time.time, time.sleep)
# s.enter(1, 1, city_name())
# s.run()
# city_name()
city_name()


root.mainloop()