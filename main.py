from bs4 import BeautifulSoup
import requests
import os
import re

# 파일 내부에 접근하여 id, index값을 가져오는 함수
def		get_music_data(lines):
	music_data = {}
	for line in lines:
		if line.find("\"index\":") != -1:
			music_index = re.sub("( |\"|index|:|,|\n)", "", line)
		if line.find("\"id\":") != -1:
			music_id = re.sub("( |\"id\"|\"|:|,|\n)", "", line)
		if line.find("}") != -1:
			music_data[music_index] = music_id
	return music_data

# songlst/* 에 해당하는 파일에 접근하는 함수
def		find_file(path_dir):
	file_list = os.listdir(path_dir)
	music_data = {}
	for file in file_list:
		try:
			fw = open(f"{path_dir}{file}", "r")
		except:
			print(f"{file} 열기에 실패하였습니다.")
			return 1
		lines = fw.readlines()
		# if lines != "[]\n":
		# 	print(lines)
		music_data.update(get_music_data(lines))
		fw.close()
	return music_data

def		get_last_page(url):
	global count
	result = requests.get(url)
	soup = BeautifulSoup(result.text, "html.parser")
	# print(soup.prettify())
	x = soup.find("div", class_="watch-main-col")
	if x:
		return 0
	else:
		return 1

# promo-title style-scope ytd-background-promo-renderer
# https://www.youtube.com/watch?v={id}
# 유튜브링크가 제대로 동작하는지 확인하는 함수
def		ytlink(music_datas):
	total, live, dead = 0, 0, 0
	dead_indexs = []
	for index, id in music_datas.items():
		url = f"https://www.youtube.com/watch?v={id}"
		total += 1
		if get_last_page(url) == 0:
			# print(f"휴우 살았다 {index}")
			# print(url)
			live += 1
		else:
			# print(f"죽었어!!!! 🪦")
			# print(f"https://jst.chichoon.com/play/{index}")
			# print(url)
			dead += 1
			dead_indexs.append(index)
	print(f"{live}/{total}\ndead 🪦  : {dead}")
	print("\n죽은 url_list")
	for dead_index in dead_indexs:
		print(f"https://jst.chichoon.com/play/{dead_index}")

def		main():
	path_dir = "public/songlist/"
	music_datas = find_file(path_dir)
	ytlink(music_datas)

main()