from utils import get_all_categories_url, get_books_data, save_to_csv_file

def scrap_all_books():
    categories_urls = get_all_categories_url()
    for category_url in categories_urls:
        save_to_csv_file(get_books_data(category_url=category_url))