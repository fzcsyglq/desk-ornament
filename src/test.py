#!/usr/bin/python3
import tkinter as tk
from PIL import Image, ImageTk
import requests
import json

# 创建主窗口
window = tk.Tk()
window.title("可控屏幕应用")
window.geometry("800x480")  # 设置屏幕分辨率

# 创建天气显示区域
weather_frame = tk.Frame(window, width=400, height=240)
weather_frame.pack(side=tk.LEFT)

# 创建相册显示区域
photo_frame = tk.Frame(window, width=400, height=240)
photo_frame.pack(side=tk.RIGHT)

# 获取天气数据
def get_weather():
    # 这里使用了一个示例的天气API，你可以根据实际情况替换成你自己的API
    url = "https://api.weatherapi.com/v1/current.json?key=YOUR_API_KEY&q=YOUR_LOCATION"
    response = requests.get(url)
    data = json.loads(response.text)
    weather = data["current"]["condition"]["text"]
    temperature = data["current"]["temp_c"]
    return f"天气: {weather}\n温度: {temperature}°C"

# 显示天气
def show_weather():
    weather_label = tk.Label(weather_frame, text=get_weather(), font=("Arial", 24))
    weather_label.pack()

# 显示相册
def show_photos():
    # 这里假设你的相册图片都存放在一个文件夹中，你可以根据实际情况进行修改
    photos = ["photos/photo1.jpeg", "photos/photo2.jpeg", "photos/photo3.jpeg"]
    current_photo = 0

    def next_photo():
        nonlocal current_photo
        current_photo = (current_photo + 1) % len(photos)        
        image = Image.open(photos[current_photo])
        image = image.resize((400, 240))
        photo = ImageTk.PhotoImage(image)
        photo_label.configure(image=photo)
        photo_label.image = photo

    image = Image.open(photos[current_photo])
    image = image.resize((400, 240))
    photo = ImageTk.PhotoImage(image)
    photo_label = tk.Label(photo_frame, image=photo)
    photo_label.pack()

    next_button = tk.Button(photo_frame, text="下一张", command=next_photo)
    next_button.pack()

# 切换功能
def switch_function(event):
    if event.delta > 0:
        show_weather()
    else:
        show_photos()

# 绑定滑动事件
window.bind("<MouseWheel>", switch_function)

# 默认显示天气
#show_weather()
show_photos()

# 运行主窗口
window.mainloop()


import os
import glob
import tkinter as tk
from PIL import Image, ImageTk

class ImageSlideshow(tk.Tk):
    def __init__(self, image_folder, slideshow_interval):
        tk.Tk.__init__(self)
        self.title("Image Slideshow")
        self.geometry("800x600")

        self.image_folder = image_folder
        self.slideshow_interval = slideshow_interval

        self.images = self.get_images()
        self.current_image_index = 0

        self.label = tk.Label(self)
        self.label.pack()

        self.bind("<Button-1>", self.next_image)
        self.after(0, self.show_image)

    def get_images(self):
        image_files = glob.glob(os.path.join(self.image_folder, "*.jpg"))  # 修改为你想要的图片格式
        images = []
        for image_file in image_files:
            image = Image.open(image_file)
            image = image.resize((800, 600))  # 修改为你想要的图片尺寸
            images.append(image)
        return images

    def show_image(self):
        image = self.images[self.current_image_index]
        photo = ImageTk.PhotoImage(image)
        self.label.config(image=photo)
        self.label.image = photo

        self.current_image_index = (self.current_image_index + 1) % len(self.images)
        self.after(self.slideshow_interval * 1000, self.show_image)

    def next_image(self, event):
        self.current_image_index = (self.current_image_index + 1) % len(self.images)

if __name__ == "__main__":
    image_folder = "path/to/your/folder"  # 修改为你的图片文件夹路径
    slideshow_interval = 5  # 修改为切换图片的时间间隔（单位：秒）

    app = ImageSlideshow(image_folder, slideshow_interval)
    app.mainloop()


import tkinter as tk

def close_window():
    root.destroy()

root = tk.Tk()
root.overrideredirect(True)
root.wm_attributes("-transparentcolor", "white")  # 将窗口的背景颜色设置为白色（可以根据实际情况修改）

# 自定义关闭按钮
close_button = tk.Button(root, text="×", font=("Arial", 12), bg="red", fg="white", bd=0, command=close_window)
close_button.pack(side="top", anchor="ne")

root.mainloop()



#!/usr/bin/python3

import tkinter as tk
import time
import turtle
import math
import requests
import json
import logging
import sys
import os
import getopt
from datetime import datetime, timedelta
from pynput.keyboard import Key
from pynput.keyboard import Controller as KController
from pynput.mouse import Button
from pynput.mouse import Controller as MController


class Frame(tk.Frame):

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.show_clock()

    def show_clock(self):
        self.keyboard = KController()
        self.mouse = MController()

        # move the mouse in the topleft corner - it look better than it would be "in front of"
        self.mouse.position = (0, 0)

        self.path = os.path.dirname(os.path.realpath(__file__))


        print("Starting WeatherClock...")
        try:
            self.options, self.remaining = getopt.getopt(sys.argv[1:], 'a:l:h', [
                "apikey=", "loglevel=", "latitude=", "longitude=" "help"])
            if self.remaining:
                print(f"Remaining arguments will not be used:{remaining}")
            if self.options:
                print(f"Options: {options}")
            self.api_key = False
            self.theme = "default"
            self.log_level = False
            self.latitude = False
            self.longitude = False
            self.units = False
            self.temperature_values = False 
            self.wind_values = False
            self.values_color = "gray"
            self.global_x_shift = 0
            self.global_y_shift = 0
            self.weather_text_description = -30
            self.weather_text_data = 30
            self.weather_text_vert_spacing = 40
            self.temperature_text_vert_spacing = -9
            self.temperature_text_horz_spacing = 11
            self.temperature_text_font_size = 11
            self.weather_text_description_font_size = 20
            self.weather_text_data_font_size = 19
            self.hourly_touch_size = 50
            self.radius = 265
            self.wn_title = "WeatherClock 0.0.0"
            self.divider_start = -125
            self.divider_end = 275
            self.hour_hand = 100
            self.hour_hand_color = "white"
            self.minute_hand = 170
            self.minute_hand_color = "yellow"
            self.second_hand = 75
            self.second_hand_color = "gray"
            self.wind_text_left_shift = 50
            self.wind_text_right_shift = 65
            self.wind_text_no_measure_text = False
            
            for opt, arg in options:
                if opt in ['-a', '--apikey']:
                    self.api_key = arg
                elif opt in ['-l', '--loglevel']:
                    self.log_level = arg
                elif opt in ['-n', '--latitude']:
                    self.latitude = arg
                elif opt in ['-s', '--longitude']:
                    self.longitude = arg
                elif opt in ['-u', '--units']:
                    if arg.lower() in ['metric', 'imperial']:
                        self.units = arg
                    else:
                        raise ValueError("[-u|--units] must be one of: metric, imperial")
                elif opt in ['-h', '--help']:
                    print('usage:\nweatherClock.py [-a|--apikey] <YourApiKey> [[-l|--loglevel] [Debug|Info|Warn|Error]|]')
                    exit(0)
                else:
                    print(f"Parameter unused: {opt}={arg}")
        except getopt.GetoptError:
            print('usage:\nweatherClock.py [-a|--apikey] <YourApiKey> [[-l|--loglevel] [Debug|Info|Warn|Error]|]')
            raise ValueError("Missing one or more parameters.")

        try:
            with open('settings.json', 'r') as settings_json:
                self.settings = json.loads(settings_json.read())
                if not api_key:
                    self.api_key_setting = settings.get('ApiKey')
                    self.api_key = api_key_setting if api_key_setting else False
                self.theme = settings.get('Theme')    
                if not log_level:
                    self.log_level = settings.get('LogLevel')
                if not latitude:
                    self.latitude = settings.get('Latitude')
                if not longitude:
                    self.longitude = settings.get('Longitude')
                if not units:
                    self.units = settings.get('Units')
                if not temperature_values:
                    self.temperature_values = settings.get('TemperatureValues').lower() in ['1', 'true']
                if not wind_values:
                    self.wind_values = settings.get('WindValues').lower() in ['1', 'true']
                self.values_color = settings.get('ValuesColor')
                self.global_x_shift = int(settings.get('GlobalXShift'))
                self.global_y_shift = int(settings.get('GlobalYShift'))
                self.weather_text_description = int(settings.get('WeatherTextDescription'))
                self.weather_text_data = int(settings.get('WeatherTextData'))
                self.weather_text_vert_spacing = int(settings.get('WeatherTextVertSpacing'))
                self.temperature_text_vert_spacing = int(settings.get('TemperatureTextVertSpacing'))
                self.temperature_text_horz_spacing = int(settings.get('TemperatureTextHorzSpacing'))
                self.temperature_text_font_size = int(settings.get('TemperatureTextFontSize'))
                self.weather_text_description_font_size = int(settings.get('WeatherTextDataFontSize'))
                self.weather_text_data_font_size = int(settings.get('WeatherTextDataFontSize'))
                # determines radius for user touch when going into hourly detail mode
                self.hourly_touch_size = int(settings.get('HourlyTouchSize'))
                # determines how big clock is
                self.radius = int(settings.get('Radius'))
                self.wn_title = settings.get('Title')
                self.divider_start = int(settings.get('DividerStart'))
                self.divider_end = int(settings.get('DividerEnd'))
                self.hour_hand = int(settings.get('HourHand'))
                self.hour_color = settings.get('HourColor')
                self.minute_hand = int(settings.get('MinuteHand'))
                self.minute_color = settings.get('MinuteColor')
                self.second_hand = int(settings.get('SecondHand'))
                self.second_color = settings.get('SecondColor')
                self.wind_text_left_shift = int(settings.get('WindTextLeftShift'))
                self.wind_text_right_shift = int(settings.get('WindTextRightShift'))
                self.wind_text_no_measure_text = settings.get('WindTextNoMeasureText').lower() in ['1', 'true']
                
        except FileNotFoundError:
            print("'settings.json' file not found. Using command line parameters.")

        if not api_key:
            raise ValueError("No ApiKey given. Use ApiKey in settings.json or use parameter: [-a|--apikey].")

        if log_level.lower() == 'debug':
            logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
        elif log_level.lower() == 'info' or log_level.lower() == 'information':
            logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
        elif log_level.lower() == 'warn' or log_level.lower() == 'warning':
            logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.WARNING)
        elif log_level.lower() == 'error':
            logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.ERROR)
        else:
            logging.error(f"Log Level set to invalid value: {log_level}")
            raise ValueError("LogLevel (--loglevel) must be one of: [Debug|Info|Information|Warn|Warning|Error]")


        self.url_params = f'lat={latitude}&lon={longitude}&exclude=current,minutely,daily,alerts,flags&appid={api_key}'
        if units:
            self.url_params += f"&units={units}"
        else:
            logging.info(f"Units not set. OpenWeatherMap.org defaults to 'standard'.")
        self.url = f'http://api.openweathermap.org/data/3.0/onecall?{url_params}'

        self.weatherUpdatePeriod = 5

        self.temp_array = [0] * 12
        self.temp_feel_array = [0] * 12
        self.wind_array = [0] * 12
        self.temp_array_was = [0] * 12
        self.temp_feel_array_was = [0] * 12
        self.wind_array_was = [0] * 12
        self.id_array = [0] * 12
        self.idImage_array = [""] * 12
        self.idImage_array_was = [""] * 12
        self.hour_cursor = int(time.strftime('%I'))

        print(url)
        self.res = requests.get(url)
        if res.ok:
            self.data = res.json()
        else:
            self.data = None
            res.raise_for_status()

        logging.debug(data)

        self.cursor_x = 0
        self.cursor_y = 0

        self.weatherText = turtle.Turtle()
        self.weatherText.hideturtle()

        self.weatherDividerPen = turtle.Turtle()
        self.weatherDividerPen.hideturtle()

        self.degree_sign = u"\N{DEGREE SIGN}"

        # 1 - hourly detail mode, 0 - analog clock face mode
        self.mode = 0

        self.hour_x = []
        self.hour_y = []

        for i in range(60, -300, -30):
            i_r = math.radians(i)
            hour_x.append((math.cos(i_r)*radius))
            hour_y.append((math.sin(i_r)*radius))

        def round_half_up(n, decimals=0):
            multiplier = 10 ** decimals
            return math.floor(n*multiplier + 0.5) / multiplier


        def touch_in_box(touch_x, touch_y, center_x, center_y, size_x, size_y):
            if center_x - size_x/2 < touch_x < center_x + size_x/2 and center_y + size_y/2 > touch_y > center_y - size_y/2:
                return True
            else:
                return False


        def get_mouse_click_coordinate(x, y):

            # when this event is triggered, it means someone pressed the screen, therefore we should check what state we are
            # going into (clock mode, or hourly detail mode)

            #global cursor_x
            #global cursor_y
            # 0 = clock, 1 = hourly detail
            #global mode
            #global hour_cursor

            self.cursor_x = x
            self.cursor_y = y
            logging.debug("cursor pressed: x, y")
            logging.debug(self.cursor_x, self.cursor_y)

            self.hour_cursor = int(time.strftime("%I"))
            self.current_meridiem = str(time.strftime('%p'))

            self.hour_touched = -1

            for i in range(0, 12):
                if touch_in_box(self.cursor_x, self.cursor_y, self.hour_x[i], self.hour_y[i], self.hourly_touch_size, self.hourly_touch_size):
                    self.hour_touched = i + 1
            self.tomorrow_date = None
            if self.hour_touched >= 0:
                logging.debug(f"hour {hour_touched} WAS TOUCHED !")

                if self.hour_touched < self.hour_cursor and not hour_cursor == 12:
                    hours_ahead = 12-hour_cursor+hour_touched
                    if current_meridiem == "PM":
                        tomorrow_date = datetime.today() + timedelta(days=1)
                        touched_meridiem = "AM"
                    else:
                        touched_meridiem = "PM"
                else:
                    if hour_cursor == 12:
                        hours_ahead = hour_touched
                    else:
                        hours_ahead = hour_touched - hour_cursor
                    touched_meridiem = current_meridiem
                if hours_ahead >= 0:
                    logging.info(f"Touched hour is {str(hours_ahead)} hours ahead")

            if mode == 0 and hour_touched != -1:
                # go to hourly detail mode
                mode = 1
                # ? to do?: add the button touches for different hours

                # remove the clock hands from showing
                pen.clear()

                # without this there is some weird line
                weatherText.penup()

                weatherText.goto(weather_text_description + global_x_shift, weather_text_vert_spacing * 3 + global_y_shift)
                weatherText.color("white")
                # day of the week
                weatherText.write("Day", align="right", font=("Verdana", weather_text_description_font_size, "bold"))

                weatherText.goto(weather_text_data + global_x_shift, weather_text_vert_spacing * 3 + global_y_shift)
                if not tomorrow_date:
                    weatherText.write(datetime.today().strftime('%A'),
                                      align="left", font=("Verdana", weather_text_data_font_size, "bold"))
                else:
                    weatherText.write(tomorrow_date.strftime('%A'),
                                      align="left", font=("Verdana", weather_text_data_font_size, "bold"))

                # hour of the day
                weatherText.goto(weather_text_description + global_x_shift, weather_text_vert_spacing * 2 + global_y_shift)
                weatherText.write("hour", align="right", font=("Verdana", weather_text_description_font_size, "bold"))

                weatherText.goto(weather_text_data + global_x_shift, weather_text_vert_spacing * 2 + global_y_shift)
                weatherText.write(str(hour_touched) + " " + touched_meridiem,
                                  align="left", font=("Verdana", weather_text_data_font_size, "bold"))

                # temperature
                weatherText.goto(weather_text_description + global_x_shift, weather_text_vert_spacing + global_y_shift)
                weatherText.write("temp", align="right", font=("Verdana", weather_text_description_font_size, "bold"))

                weatherText.goto(weather_text_data + global_x_shift, weather_text_vert_spacing + global_y_shift)
                weatherText.write(str(round_half_up(data["hourly"][hours_ahead]["temp"], 1)) + degree_sign,
                                  align="left", font=("Verdana", weather_text_data_font_size, "bold"))

                # Feels like
                weatherText.goto(weather_text_description + global_x_shift, global_y_shift)
                weatherText.write("Feels like", align="right",
                                  font=("Verdana", weather_text_description_font_size, "bold"))

                weatherText.goto(weather_text_data + global_x_shift, global_y_shift)
                weatherText.write(str(round_half_up(data["hourly"][hours_ahead]["feels_like"], 1)) + degree_sign,
                                  align="left", font=("Verdana", weather_text_data_font_size, "bold"))

                # POP
                weatherText.goto(weather_text_description + global_x_shift, -weather_text_vert_spacing + global_y_shift)
                weatherText.write("POP", align="right", font=("Verdana", weather_text_description_font_size, "bold"))

                weatherText.goto(weather_text_data + global_x_shift, -weather_text_vert_spacing + global_y_shift)
                weatherText.write(str(int(data["hourly"][hours_ahead]["pop"]*100)) + " %",
                                  align="left", font=("Verdana", weather_text_data_font_size, "bold"))

                # Rain
                weatherText.goto(weather_text_description + global_x_shift, -weather_text_vert_spacing * 2 + global_y_shift)
                weatherText.write("Rain", align="right", font=("Verdana", weather_text_description_font_size, "bold"))

                weatherText.goto(weather_text_data + global_x_shift, -weather_text_vert_spacing * 2 + global_y_shift)
                if 'rain' not in data["hourly"][hours_ahead]:
                    weatherText.write("--", align="left", font=("Verdana", weather_text_data_font_size, "bold"))
                else:
                    weatherText.write(str(data["hourly"][hours_ahead]["rain"]["1h"]) + " mm",
                                      align="left", font=("Verdana", weather_text_data_font_size, "bold"))

                # Wind
                weatherText.goto(weather_text_description + global_x_shift, -weather_text_vert_spacing * 3 + global_y_shift)
                weatherText.write("Wind", align="right", font=("Verdana", weather_text_description_font_size, "bold"))

                weatherText.goto(weather_text_data + global_x_shift, -weather_text_vert_spacing * 3 + global_y_shift)
                weatherText.write(str(data["hourly"][hours_ahead]["wind_speed"]) + " km/h",
                                  align="left", font=("Verdana", weather_text_data_font_size, "bold"))

                weatherText.hideturtle()

                weatherDividerPen.pensize(3)

                weatherDividerPen.penup()
                weatherDividerPen.goto(global_x_shift, divider_start + global_y_shift)
                weatherDividerPen.color("white")
                weatherDividerPen.setheading(90)
                weatherDividerPen.pendown()
                weatherDividerPen.fd(divider_end)
                weatherDividerPen.hideturtle()

            elif mode == 1 and touch_in_box(cursor_x, cursor_y, 0, 0, 200, 200):
                mode = 0  # go back to clock mode
                weatherText.clear()  # remove hourly details from screen
                weatherDividerPen.clear()

            cursor_x = -1
            cursor_y = -1


        def update_forecast():

            global hour_cursor

            # weather ID breakdown https://openweathermap.org/weather-conditions
            # use https://ezgif.com/maker for gif conversion

            logging.debug("---- update_forecast() ----")

            hour_cursor = int(time.strftime("%I"))
            meridiem = time.strftime('%p')

            logging.debug("hour_cursor: " + str(hour_cursor))

            for num in range(12):
                # current hour
                logging.debug("current hour: " + str(hour_cursor) + " " + meridiem)
                # forecast hour
                logging.debug("forecast hour: " + str(int(hour_cursor)+num))
                logging.debug("temperature: " + str(data["hourly"][num]["temp"]))
                logging.debug("feels like: " + str(data["hourly"][num]["feels_like"]))
                logging.debug("wind speed: " + str(data["hourly"][num]["wind_speed"]))
                logging.debug(data["hourly"][num]["weather"][0]["description"])
                logging.debug("weather ID: " + str(data["hourly"][num]["weather"][0]["id"]))
                logging.debug("POP: " + str(data["hourly"][num]["pop"]))

                if 'rain' not in data["hourly"][num]:
                    logging.debug("no rain data")
                else:
                    logging.debug("rain: " + str(data["hourly"][num]["rain"]))

                temp_array[num] = data["hourly"][num]["temp"]
                temp_feel_array[num] = data["hourly"][num]["feels_like"]
                wind_array[num] = data["hourly"][num]["wind_speed"]      
                id_array[num] = data["hourly"][num]["weather"][0]["id"]

                path_theme = os.path.join(path, theme)

                if 232 >= id_array[num] >= 200:
                    idImage_array[num] = os.path.join(path_theme, "11d@2x.gif")
                elif 321 >= id_array[num] >= 300:
                    idImage_array[num] = os.path.join(path_theme, "09d@2x.gif")
                elif 504 >= id_array[num] >= 500:
                    idImage_array[num] = os.path.join(path_theme, "10d@2x.gif")
                elif id_array[num] == 511:
                    idImage_array[num] = os.path.join(path_theme, "13d@2x.gif")
                elif 531 >= id_array[num] >= 520:
                    idImage_array[num] = os.path.join(path_theme, "09d@2x.gif")
                elif 622 >= id_array[num] >= 600:
                    idImage_array[num] = os.path.join(path_theme, "13d@2x.gif")
                elif 781 >= id_array[num] >= 701:
                    idImage_array[num] = os.path.join(path_theme, "50d@2x.gif")
                elif id_array[num] == 800:
                    idImage_array[num] = os.path.join(path_theme, "01d@2x.gif")
                elif id_array[num] == 801:
                    idImage_array[num] = os.path.join(path_theme, "02d@2x.gif")
                elif id_array[num] == 802:
                    idImage_array[num] = os.path.join(path_theme, "03d@2x.gif")
                elif id_array[num] == 803 or id_array[num] == 804:
                    idImage_array[num] = os.path.join(path_theme, "04d@2x.gif")
                else:
                    logging.error("Invalid weather ID")

            logging.debug(temp_array)
            logging.debug(id_array)
            logging.debug(idImage_array)

            for image in idImage_array:
                wn.addshape(image)


        wn = turtle.Screen()
        canvas = wn.getcanvas()
        canvas.pack(in_ = self)
        wn.bgcolor("black")
        wn.screensize()
        #wn.setup(width=600, height=600)
        # Make full screen
        wn.setup(width=1.0, height=1.0)
        wn.title(wn_title)
        # turns off the animation, so you can't see anything when it is drawing
        wn.tracer(0)

        # create our drawing pen
        pen = turtle.Turtle()
        pen.hideturtle()
        # 0 is fastest it can go
        pen.speed(0)
        pen.pensize(3)

        bg_hour = []
        bg_hourtext = []
        bg_windtext = []

        for i in range(0, 12):
            bg_hour_i = turtle.Turtle()
            bg_hour_i.goto(hour_x[i] + global_x_shift, hour_y[i] + global_y_shift)
            bg_hour.append(bg_hour_i)

            bg_hourtext_i = turtle.Turtle()
            bg_hourtext_i.color(values_color)
            bg_hourtext_i.hideturtle()
            bg_hourtext.append(bg_hourtext_i)

            bg_windtext_i = turtle.Turtle()
            bg_windtext_i.color(values_color)
            bg_windtext_i.hideturtle()
            bg_windtext.append(bg_windtext_i)

        s = 0
        # time.sleep(10)


        # draw a clock using the pen i created
        def draw_clock(hour, minute, second, pen):
            pen.hideturtle()

            # Draw the hour hand
            pen.penup()
            pen.goto(global_x_shift, global_y_shift)
            pen.color(hour_color)
            pen.pensize(6)
            pen.setheading(90)
            angle = (hour / 12) * 360 + (minute/60) * 30
            pen.rt(angle)
            pen.pendown()
            pen.fd(hour_hand)

            # Draw the minute hand
            pen.penup()
            pen.goto(global_x_shift, global_y_shift)
            pen.color(minute_color)
            pen.setheading(90)
            angle = (minute / 60.0) * 360  # optional + (s/60) * 6
            pen.rt(angle)
            pen.pendown()
            pen.fd(minute_hand)

            # Draw the second hand
            pen.penup()
            pen.goto(global_x_shift, global_y_shift)
            pen.color(second_color)
            pen.setheading(90)
            angle = (second / 60) * 360
            pen.rt(angle)
            pen.pendown()
            pen.fd(second_hand)

        # makes the program fullscreen when you launch it
        keyboard.press(Key.alt)
        keyboard.press(Key.f11)
        time.sleep(0.05)
        keyboard.release(Key.f11)
        keyboard.release(Key.alt)
        time.sleep(1)   

        canvas = wn.getcanvas()
        top_window = canvas.winfo_toplevel()
        running = True
        # wn.onkeypress(fun=exit(), key='q')


        def on_close():
            global running
            running = False


        top_window.protocol("WM_DELETE_WINDOW", on_close)
        top_window.overrideredirect(True)
        wn.listen()

        needUpdate1 = True    

        while running:
            try:
                logging.debug("\n... Main Loop Start ...\n")

                h = int(time.strftime("%I"))
                m = int(time.strftime("%M"))
                s = int(time.strftime("%S"))

                logging.debug(f"{str(h)}:{str(m)}:{str(s)}")

                needUpdate = False
                if (needUpdate1):
                    needUpdate = True
                    needUpdate1 = False
                
                # every x minutes, fetch new weather data
                if m % weatherUpdatePeriod == 0 and s == 0:
                    res = requests.get(url)
                    data = res.json()
                    logging.debug("** FETCHED NEW DATA **")
                    needUpdate = True

                if mode == 0:
                    draw_clock(h, m, s, pen)
                    update_forecast()

                    logging.debug(f"hour_cursor: {str(hour_cursor)}")
                    
                    for i in range(1, 13):
                        if (i - hour_cursor < 0):
                            j = 12 - abs(i - hour_cursor)
                        else:
                            j = i - hour_cursor
                        if(idImage_array[j] != idImage_array_was[j]):
                            bg_hour[i-1].shape(idImage_array[j])
                            idImage_array_was[j] = idImage_array[j]
                            
                        if ((needUpdate) or (temp_array[j] != temp_array_was[j]) or (temp_feel_array[j] != temp_feel_array_was[j]) or
                                (wind_array[j] != wind_array_was[j])):
                            if (temperature_values):
                                bg_hourtext[i-1].clear()
                                bg_hourtext[i-1].penup()
                                x_shift = 0
                                y_shift = 0
                                if (("04d@2x.gif" in idImage_array[j]) or ("02d@2x.gif" in idImage_array[j])):
                                    x_shift = -7
                                    y_shift = -8
                                if ("11d@2x.gif" in idImage_array[j]):
                                    x_shift = -9
                                    y_shift = 3
                                if (("09d@2x.gif" in idImage_array[j]) or  ("10d@2x.gif" in idImage_array[j])):
                                    x_shift = -6
                                    y_shift = 3
                                if ("03d@2x.gif" in idImage_array[j]):
                                    x_shift = -3
                                    y_shift = -5
                                if (temp_array[j] < 10):
                                    x_shift = x_shift + 4
                                bg_hourtext[i-1].goto(hour_x[i-1] + temperature_text_horz_spacing + x_shift - 20 + global_x_shift, hour_y[i-1] + temperature_text_vert_spacing + y_shift + global_y_shift)
                                v = int(round(temp_array[j]))
                                v2 = int(round(temp_feel_array[j]))
                                bg_hourtext[i-1].write(str(round(temp_array[j])), align="left", font=("Verdana", temperature_text_font_size, "bold"))
                            if  (wind_values):   
                                if (i in range(1,6)):
                                    bg_windtext[i-1].clear()
                                    bg_windtext[i-1].penup()
                                    kmh = " km/h"
                                    if (wind_text_no_measure_text):
                                        kmh = ""
                                    bg_windtext[i-1].goto(hour_x[i-1] + temperature_text_horz_spacing +  x_shift + wind_text_right_shift + global_x_shift, hour_y[i-1] + temperature_text_vert_spacing + y_shift + global_y_shift)
                                    bg_windtext[i-1].write(str(wind_array[j]) + kmh, align="left", font=("Verdana", temperature_text_font_size, ""))
                                if (i in range(7,12)):
                                    bg_windtext[i-1].clear()
                                    bg_windtext[i-1].penup()
                                    bg_windtext[i-1].goto(hour_x[i-1] + temperature_text_horz_spacing +  x_shift - wind_text_left_shift + global_x_shift, hour_y[i-1] + temperature_text_vert_spacing + y_shift + global_y_shift)
                                    bg_windtext[i-1].write(str(wind_array[j]), align="right", font=("Verdana", temperature_text_font_size, ""))
                        temp_array_was[j] = temp_array[j]
                        temp_feel_array_was[j] = temp_feel_array[j]
                        wind_array_was[j] = wind_array[j]                    

                wn.update()

                # cursor / touch logic
                # this returns the coordinate of the press !
                turtle.onscreenclick(get_mouse_click_coordinate)
                logging.debug("MODE:" + str(mode))
                logging.debug("cursor_x: " + str(cursor_x) + "; cursor_y: " + str(cursor_y))

                if cursor_x != -1 and cursor_y != -1:
                    logging.debug("screen was touched")

                time.sleep(1)

                pen.clear()

            except KeyboardInterrupt:
                print("Exiting WeatherClock.")
                exit(0)
