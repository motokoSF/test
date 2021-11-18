from typing import Text
from bs4 import BeautifulSoup
import requests
import csv



def data_book(soup_all_cat_book):

    data = {}

    # Universal product code        
    data["universal_product_code"] = soup_all_cat_book.select("td")[0].text          
    #price_including_tax 
    data["price_including_tax"] = soup_all_cat_book.select("td")[2].text
    #price_excluding_tax
    data["price_excluding_tax"] = soup_all_cat_book.select("td")[3].text
    #number_available
    data["number_available"] = soup_all_cat_book.select("td")[5].text  
    #titres
    data["title"] = soup_all_cat_book.select("h1")[0].text
    #product_description
    data["product_description"] = soup_all_cat_book.select("p")[3].text
    #category
    data["category"] = soup_all_cat_book.select("a")[3].text
    #review_rating
    data["review_rating"] = soup_all_cat_book.find_all("p", class_="star-rating")[0].get("class")[1]
    #image_url
    image = soup_all_cat_book.find("div", class_="item active").img["src"]
    data["image_url"] = "http://books.toscrape.com/" + image.replace('../', '')

    return data

    




url="https://books.toscrape.com/index.html"



réponse = requests.get(url)
soup = BeautifulSoup(réponse.text, 'html.parser')

get_first_ul = soup.find("ul", class_="nav nav-list")
get_all_ul= get_first_ul.find("ul")
get_all_lis = get_all_ul.find_all("li")
for li in get_all_lis:
        categorie_url = url.replace("index.html",li.find('a')['href'].replace("index.html", "")) 
        categories_links = categorie_url + "index.html"
        print(categories_links)

        while True:

            demande = requests.get(categories_links)
            soup = BeautifulSoup(demande.text, 'html.parser')

    
            get_section = soup.find("section")
            get_all_article = get_section.find_all("article")
            for article in get_all_article:
                #avoir tous les liens sur une page 
                get_partial_links = article.find_all("a")[1]["href"]
                get_books_links = "https://books.toscrape.com/catalogue/" + get_partial_links.replace("../../../", "")   
                

                demande_cat_book = requests.get(get_books_links)
                soup_all_cat_book = BeautifulSoup(demande_cat_book.text, 'html.parser')
        
 
                #data/CSV pour tt les livres 
                data_cat_books = data_book(soup_all_cat_book)

                with open(r"C:\Users\Albin\Desktop\OpenClassrooms\P2_Albin_Capron\fichier-cat.csv","a",newline="", encoding="utf-8") as file:
            
                                Dictwriter = csv.DictWriter(file, fieldnames =  data_cat_books.keys())
                                Dictwriter.writeheader()
                                Dictwriter.writerow( data_cat_books)

            class_next = soup.find("li", class_ ="next")
            if class_next is None:
                break
            else:
                get_partial_links = class_next.find("a")["href"]

                categories_links = categorie_url + get_partial_links.replace("../../../", "")
                print(categories_links)
            