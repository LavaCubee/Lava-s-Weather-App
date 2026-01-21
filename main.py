import requests
import time
import threading
import sys
import os
from pystray import Icon, MenuItem, Menu
from PIL import Image

CITY = "City" # Your city,Ваш город.
UPDATE_INTERVAL = 600  # Timer of weather refresh (10 minutes),Таймер обновления погоды (10 минут).

def restart_app(icon, item):
    icon.stop()
    python = sys.executable
    os.execv(python, [python] + sys.argv)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_weather():
    try:
        r = requests.get(
            f"https://wttr.in/{CITY}?format=3",
            timeout=10
        )
        return r.text
    except:
        restart_app

def choose_icon(weather_text):
    text = weather_text.lower()

    if "☀" in weather_text or "clear" in text:
        return resource_path("icons/sun.png")
    if "🌧" in weather_text or "rain" in text:
        return resource_path("icons/rain.png")
    if "❄" in weather_text or "snow" in text:
        return resource_path("icons/snow.png")
    if "fog" in text or "mist" in text:
        return resource_path("icons/fog.png")

    return resource_path("icons/cloud.png")

def update(icon):
    while True:
        weather = get_weather()
        icon_path = choose_icon(weather)

        try:
            icon.icon = Image.open(icon_path)
        except:
            pass

        icon.title = weather
        time.sleep(UPDATE_INTERVAL)

def exit_app(icon, item):
    icon.stop()

icon = Icon(
    "weather",
    Image.open(resource_path("icons/cloud.png")),
    "Weather loading...,Загрузка погоды...",
    menu=Menu(
        MenuItem("Restart App,Перезапуск приложения", restart_app),
        MenuItem("Exit,Выход", exit_app)
    )
)

threading.Thread(target=update, args=(icon,), daemon=True).start()
icon.run()
