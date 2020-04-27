import sqlite3
import io
import requests
import lxml.etree
import shutil # Подключаем модуль
import os



con = sqlite3.connect("db/1.db")
cur = con.cursor()
museums = cur.execute("""SELECT * FROM Museums""").fetchall()
for museum in museums:
	i = museum[2]
	geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={i} &format=xml"
	response = requests.get(geocoder_request)
	root = lxml.etree.fromstring(response.content)
	pos1 = ','.join(root.findtext(".//{*}pos").split())
	maprec = f"https://static-maps.yandex.ru/1.x/?ll={pos1}8&spn=0.016457,0.00619&l=map&&pt={pos1},pm2ywl1"
	response = requests.get(maprec)

	map_file = museum[1] + ".png"
	with open(os.path.join('static', 'picture', map_file), "wb") as file:
	    file.write(response.content)
