from scraping_data import scrap_images, scrap_book_informations
import constants

def main_menu():
    """Affiche le menu principal"""
    print(constants.MENU)

    choix = input("Votre choix: ")
    choix_disponible = ["1", "2", "3"]

    while choix in choix_disponible:
        if choix == "1":
            scrap_book_informations(constants.URL)
        elif choix == "2":
            scrap_images(constants.URL)
        elif choix == "3":
            print("Au revoir")
            exit()

    print("Choix invalide")
    return main_menu()


main_menu()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
