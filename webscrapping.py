from datetime import date
from distutils.log import info
from urllib import request
import requests
from bs4 import BeautifulSoup


def get_database():
    from pymongo import MongoClient
    import pymongo

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://webscrapping-user:KbL7bDtumnkWyjCa@cluster0.lwh3p.mongodb.net/?retryWrites=true&w=majority"
    # "mongodb+srv://<username>:<password>@cluster0.lwh3p.mongodb.net/?retryWrites=true&w=majority"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    from pymongo import MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['webscrapping']


# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":

    # Get the database
    webscrapping = get_database()

    page = requests.get("https://books.toscrape.com/index.html")
    soup = BeautifulSoup(page.content, 'html.parser')

    li = soup.select("ol > li")
    url = 'https://books.toscrape.com/'

    # auditoria
    auditoría = {
        "fecha": str(date.today()),
        "pagina_web": "https://books.toscrape.com/index.html",
        "numero_registros": len(li),
        "estado": "finalizado",
        "errores": "none"
    }
    # inserta en la db
    webscrapping.auditoria.insert_one(auditoría)

    # print(len(li))
    for link in li:
        page = requests.get(url + link.find('a').get('href'))
        sopa = BeautifulSoup(page.content, 'html.parser')
        titulo = sopa.find('h1').get_text()
        BOOK = {'titulo': titulo}
        tabla = sopa.find("table")
        tr = tabla.find_all('tr')
        for t in tr:
            prod_info = {
                **BOOK, t.find('th').get_text(): t.find('td').get_text()}
            BOOK = {**prod_info}
        # print(BOOK)

        # insertar en la db
        webscrapping.registros.insert_one(BOOK)
