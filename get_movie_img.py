

import requests
import bs4
import requests, bs4
import csv

total_img_link = []
with open('yahoo_movie.csv', 'r', encoding='utf-8-sig') as f:
    result = f.readlines()

for i in range(1, len(result)):
    try:
        movie_url = result[i].split(',')[2]
        # print(movie_url)
        moviehtml = requests.get(movie_url)
        objSoup = bs4.BeautifulSoup(moviehtml.text, 'html')
        movie_img_link = objSoup.select("div.movie_intro_foto")[0].find("img").get("src")
        print(movie_img_link)
        total_img_link.append(movie_img_link)
    except:
        movie_img_link = 'https://www.portent.com/images/2020/07/404-Error-Image.jpg'
        total_img_link.append(movie_img_link)
        print('無圖片')


with open('img_link.csv','w',newline='') as f:
    writer=csv.writer(f)
    writer.writerow(['link'])
    for link in total_img_link:
        writer.writerow([link])
f.close()
