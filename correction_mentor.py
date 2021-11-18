from bs4 import BeautifulSoup
import requests
import csv


url="https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"

while True:

    demande = requests.get(url)
    soup = BeautifulSoup(demande.text, 'html.parser')

    get_section = soup.find("section")
    get_all_article = get_section.find_all("article")
   
    list_of_book = []
    for url in get_all_article:
        info_of_book = get_info_book(url)
        list_of_book.append(info_of_book)
    
    write_book(list_of_book)

    def get_info_book(url):
        #avoir tous les liens sur une page 
        get_partial_links = url.find_all("a")[1]["href"]
        get_books_links = "https://books.toscrape.com/catalogue/" + get_partial_links.replace("../../../", "")
      
        

        demande_cat_book = requests.get(get_books_links)
        soup_all_cat_book = BeautifulSoup(demande_cat_book.text, 'html.parser')
        

        # Universal product code        
        get_all_upc = soup_all_cat_book.select("td")[0].text          
        #price_including_tax 
        get_all_price_including_tax  = soup_all_cat_book.select("td")[2].text
        #price_excluding_tax
        get_all_price_excluding_tax = soup_all_cat_book.select("td")[3].text
        #number_available
        get_all_stock = soup_all_cat_book.select("td")[5].text  
        #titres
        get_all_title = soup_all_cat_book.select("h1")[0].text
        #product_description
        get_all_description = soup_all_cat_book.select("p")[3].text
        #category
        get_all_categories = soup_all_cat_book.select("a")[3].text
        #review_rating
        get_all_rating = soup_all_cat_book.find_all("p", class_="star-rating")[0].get("class")[1]
        #image_url
        image = soup_all_cat_book.find("div", class_="item active").img["src"]
        get_all_image_url = "http://books.toscrape.com/" + image.replace('../', '')

        list_dict = []
        #data/CSV pour tt les livres d'une catégorie
        list_dict.append( {
                        "links": get_books_links,
                        "universal_ product_code": get_all_upc,
                        "title": get_all_title,
                        "price_including_tax": get_all_price_including_tax,
                        "price_excluding_tax": get_all_price_excluding_tax,
                        "number_available": get_all_stock,
                        "product_description": get_all_description,
                        "category": get_all_categories,
                        "review_rating": get_all_rating,
                        "image_url": get_all_image_url,
                        })
       
        def write_books_csv(list_books):
            for book in list_books:
                with open(r"C:\Users\Albin\Desktop\OpenClassrooms\P2_Albin_Capron\fichier-cat.csv","a",newline="", encoding="utf-8") as file:
            
                    Dictwriter = csv.DictWriter(file, fieldnames = book.keys())
                    Dictwriter.writeheader()
                    Dictwriter.writerow(book)

    class_next = soup.find("li", class_ ="next")
    if class_next is None:
        break
    else:
        get_partial_links = class_next.find("a")["href"]
        url = url.replace("index.html", "") + get_partial_links.replace("../../../", "")
       
    


    
    



            

    

