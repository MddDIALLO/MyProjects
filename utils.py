import math

import requests
from bs4 import BeautifulSoup

import constants
'''Hello'''
def parse_html(url: str) -> BeautifulSoup:
    """Envoi de la requête pour récupérer la parser"""
    response = requests.get(url)
    return BeautifulSoup(response.content, 'html.parser')

def get_number_of_pages(category_url: str) -> int:
    """Retourne le nombre de pages présentes dans la catégorie"""
    content = parse_html(category_url)
    number_of_books_in_category = content.select("strong")[1].text
    if not number_of_books_in_category.isdigit():
        raise ValueError("Le nombre de livres dans la catégorie est invalide")
    return math.ceil(int(number_of_books_in_category) / 20)

def get_pages_urls(category_url: str) -> list:
    """Recuperation des urls de chaque catégorie"""
    pages_urls = []
    number_of_pages = get_number_of_pages(category_url)
    if number_of_pages == 1:
        pages_urls.append(category_url)
    else:
        for page_number in range(number_of_pages):
            pages_urls.append(category_url.replace("index.",f"page-{page_number + 1}"))
    return pages_urls
    #[category_url.replace("index.",f"page-{page_number + 1}") for page_number in range(number_of_pages)]

def get_books_from_category(category_url):
    pages_urls = get_pages_urls(category_url)
    return get_books_urls(pages_urls)

def get_books_urls(pages_urls: list) -> list:
    """Recuperer les URLs des livres"""
    books_url = []
    for page_url in pages_urls:
        content = parse_html(page_url)
        titles = content.find_all("h3")
        for title in titles:
            href = title.find('a')["href"]
            if "../../../" in href:
                url = href.replace("../../../", f"{constants.URL}catalogue/")
            else:
                url = constants.URL + href
            books_url.append(url)
    return books_url

if __name__ == '__main__':
    page_urls = get_pages_urls("https://books.toscrape.com/catalogue/category/books/travel_2/index.html")
    books_urls = get_books_urls(page_urls)
    print(books_urls)