# importer les librairies pour le scraping des données 
from bs4 import BeautifulSoup
import requests
import csv


url="https://books.toscrape.com/catalogue/dune-dune-1_151/index.html"
demande = requests.get(url)
soup = BeautifulSoup(demande.text, 'html.parser')


# product_page_url
# il me faut l'url du site into url categorie into url du livre  

get_section = soup.find_all("section") 

#universal_ product_code (upc)
upc = soup.select("td")[0].text
#title
titre = soup.select("h1")[0].text
#price_including_tax 
prix_avec_taxe = soup.select("td")[2].text
#price_excluding_tax
prix_sans_taxe = soup.select("td")[3].text
#number_available
stock = soup.select("td")[5].text
#product_description
description = soup.select("p")[3].text
#category
categorie = soup.select("a")[3]
#review_rating
note = soup.find_all("p", class_="star-rating")[0].get("class")[1]
#image_url
image = soup.find("div", class_="item active").img["src"]
image = "http://books.toscrape.com/" + image.replace('../', '')


#data/CSV pour un livre
data_pour_un_livre = {
                      "universal_ product_code": upc,
                      "title": titre,
                      "price_including_tax": prix_avec_taxe,
                      "price_excluding_tax": prix_sans_taxe,
                      "number_available": stock,
                      "product_description": description,
                      "category": categorie,
                      "review_rating": note,
                      "image_url": image,
                      }


with open(r"C:\Users\Albin\Desktop\OpenClassrooms\P2_Albin_Capron\fichier.csv","w",newline="", encoding="utf-8") as file:
  

    writer = csv.DictWriter(file, fieldnames = data_pour_un_livre.keys())
    writer.writeheader()
    writer.writerow(data_pour_un_livre)


print(data_pour_un_livre)