from src.fetch import Scraper
import sys
import os

scrape = Scraper()
scrape.lookup_links('photo')
def main_menu():
    Active = True
    while Active:
        print('PDFS'.center(50, '-'))
        for index, title in enumerate(scrape.titles, start=1):
            if os.path.exists(f'{scrape.PATH}/pdfs/{title}.pdf'):
                print('['+ str(index) +'] ' + title, "> [Downloaded] ".rjust(50,'-'))
            else:
                print('['+ str(index) +'] ' + title)
        try:
            user_input = int(input('\nEnter the option: '))
            scrape.download_pdfs(user_input)
        except EOFError:
            sys.exit()

main_menu()
