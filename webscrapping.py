


import requests 
from bs4 import BeautifulSoup

page = requests.get("https://www.bmw.co.cr/es/index.html")
soup = BeautifulSoup(page.content, 'html.parser')

# print(soup.prettify())
# print(soup.body)

#Links
print('============== Links ==============')
for link in soup.find_all('a'):
    print(link.get('href'))

#Textos
print('============== Textos ==============')
print(soup.get_text())

#Listas
print('============== Listas ==============')
print(soup.ul)

#Imagenes
print('============== Imagenes ==============')
# print(soup.img)
for image in soup.find_all('img'):
    print(image)
