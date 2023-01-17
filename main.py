from scraping_data import scrap_all_books
import constants

def main_menu():
    """Afficher le menu principal"""
    print(constants.MENU)

    choix = input("Votre choix: ")
    choix_disponible = ["1", "2"]

    while choix in choix_disponible:
        if choix == "1":
            scrap_all_books()
            exit()
        elif choix == "2":
            print("Au revoir")
            exit()

    print("Choix invalide")
    return main_menu()

main_menu()