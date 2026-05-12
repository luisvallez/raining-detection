from requests import get
from os import getenv
from dotenv import load_dotenv
from json import load, dump
from pandas import DataFrame

load_dotenv()

# Colocar API de https://openweathermap.org/api/forecast5
API: str = getenv("APIKEY")

# Puedes encontrar tus coordenadas deseadas en https://www.coordenadas-gps.com/
lat: str = "32.6245314"
lon: str = "-115.452604"

df: dict = {}
lista: list[int] = []


def leer_datos():
    with open("datos.json", "r") as file:
        data: dict = load(file)
        return DataFrame(data["list"])


try:
    df = leer_datos()
except FileNotFoundError:
    with get(
        url=f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API}"
    ) as response:
        data: dict = response.json()
        with open("datos.json", "w") as file:
            dump(data, file, indent=2)
    df = leer_datos()
finally:
    for x in leer_datos()["weather"]:
        lista.append(x[0]["id"])


try:
    indice_lluvia = lista.index(500)
except ValueError:
    print("No va a llover pronto")
else:
    if indice_lluvia in [0, 1, 2, 3]:
        print(f"it will rain in the next {(indice_lluvia+1)*3} hours")
    else:
        print("puede que llueva mañana")
