import os
import webbrowser
import sys
import subprocess
import voice

try:
	import requests
except:
	pass

def youtube(): # Запуск Ютуб
	webbrowser.open('https://www.youtube.com', new=2)


def yandex(): # Запуск Яндекс
	webbrowser.open('https://ya.ru/', new=2)


def vscode(): # Запуск VS Code
	try:
		subprocess.Popen('C:/Users/alexa/AppData/Local/Programs/Microsoft VS Code/Code.exe')
	except:
		voice.speaker('Путь к файлу не найден')


def weather(): # Получение погоды
	try:
		params = {'q': 'Красноярск', 'units': 'metric', 'lang': 'ru', 'appid': '3017071876ec86eaded0687918431d9a'}
		response = requests.get(f'https://api.openweathermap.org/data/2.5/weather', params=params)
		if not response:
			raise
		w = response.json()
		voice.speaker(f"в {w['name']}е сейчас на улице {w['weather'][0]['description']} {round(w['main']['temp'])} градусов")
		
	except:
		voice.speaker('Произошла ошибка')


def offBot(): # Отключение бота
	sys.exit()


def passive(): # Диалог с ботом
	pass

