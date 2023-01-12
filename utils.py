import math
import re
from pathlib import Path
from pprint import pprint

import requests
from bs4 import BeautifulSoup

import constants


def get_all_categories_url():
    """Recupere les liens de toutes les categories"""
    soup = parse_html(constants.URL)
    all_categories_tags = soup.find("div",class_="side_categories").find("ul").find_all("li")[1:]
    return [f"{constants.URL}/{category_tag.find('a')['href']}" for category_tag in all_categories_tags]

def get_books_data(category_url):
    print(type(get_books_urls(category_url)))
    return [get_book_data(book_url) for book_url in get_books_urls(category_url)]

def parse_html(url):
    """Envoi de la requête pour récupérer le BeautifulSoup des pages"""
    response = requests.get(url)
    return BeautifulSoup(response.content, "html.parser")

def get_number_of_pages(category_url):
    """Retourne le nombre de pages présentes dans la catégorie"""
    content = parse_html(category_url)
    number_of_books_in_category = content.select("strong")[1].text
    if not number_of_books_in_category.isdigit():
        raise ValueError("Le nombre de livres dans la catégorie est invalide")
    return math.ceil(int(number_of_books_in_category) / 20)

def get_pages_urls(category_url):
    """Recuperer les urls de chaque catégorie"""
    pages_urls = []
    number_of_pages = get_number_of_pages(category_url)
    if number_of_pages == 1:
        pages_urls.append(category_url)
    else:
        for page_number in range(number_of_pages):
            pages_urls.append(category_url.replace("index.",f"page-{page_number + 1}"))
    return pages_urls
    #[category_url.replace("index.",f"page-{page_number + 1}") for page_number in range(number_of_pages)]

# Pour moi c'est là que ça se casse la gueule
def get_books_urls(pages_urls):
    """Recupere les URL des livres"""
    books_url = []
    content = parse_html(pages_urls)
    titles = content.find_all("h3")
    for title in titles:
        href = title.find("a")["href"]
        if "../../../" in href:
            url = href.replace("../../../", f"{constants.URL}catalogue/")
        else:
            url = constants.URL + href
        books_url.append(url)
    return books_url
    '''
    
    for page_url in pages_urls:
        print(page_url)
        content = parse_html(page_url)
        titles = content.find_all("h3")
        for title in titles:
            href = title.find("a")["href"]
            if "../../../" in href:
                url = href.replace("../../../", f"{constants.URL}catalogue/")
            else:
                url = constants.URL + href
            books_url.append(url)
    return books_url
    '''

def get_book_data(url):
    """Recupere les informations des livres de chaque page"""
    url = parse_html(url)
    html_tags = url.find(class_="product_main")
    data = {"title": html_tags.find("h1").get_text(strip=True),
            "category": url.find("ul", class_="breadcrumb").find_all("a")[2].get_text(strip=True),
            "price": html_tags.find(class_="price_color").get_text(strip=True).replace("Â", ""),
            "review_rating": " ".join(html_tags.find(class_="star-rating").get("class")).replace("star-rating", "").strip(),
            "image_url": url.find(class_="thumbnail").find("img").get("src").replace("../../../", f"{constants.URL}")}

    if description := url.find(id="product_description"):
        data["description"] = description.find_next_sibling("p").get_text(strip=True)
    else:
        data["description"] = ""

    additional_information = url.find(text="Product Information").find_next("table")
    for row in additional_information.find_all("tr"):
        header = row.find("th").get_text(strip=True)
        header = re.sub("[^a-zA-Z]+", "_", header)
        value = row.find("td").get_text(strip=True).replace("Â", "")
        data[header] = value
    return data

def convert_book_data_to_csv(books_data):
    lines = ["Titre;Categorie;Prix;Rating;Image URL;Description"]

    for book_data in books_data:
        lines.append(";".join([book_data["title"],
                              book_data["category"],
                              book_data["price"],
                              book_data["review_rating"],
                              book_data["image_url"],
                              book_data["description"]]))
        return "\n".join(lines)

def save_to_csv_file(book_data):
    """Enregistrer les informations des livres"""
    category_name = book_data[0]["category"]
    folder_path = Path("data") / category_name
    folder_path.mkdir(parents=True, exist_ok=True)

    file_path = folder_path / f"{category_name}.csv"
    with open(file_path, "a", encoding="utf8") as f:
        f.write(convert_book_data_to_csv(book_data))

    return True

    return True

def get_all_pages_url(category_url):
    """Recuperation des 50 pages du catalogue"""
    page = 1
    pages_url = []

    while True:
        page_url = category_url + f"catalogue/page-{page}.html"
        page += 1
        response = requests.get(page_url)
        if response.status_code == 200:
            pages_url.append(page_url)
        else:
            break
        return pages_url