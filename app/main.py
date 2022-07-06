from requests_html import HTMLSession
from colorama import Fore

from source import time_counter, read_csv
from scrape import WordpressPluginParser
from image import ImageParser
from db import db, WordpressPluginDB


s = HTMLSession()


@time_counter()
def write_to_db():
    data = read_csv()
    db.connect()
    db.create_tables([WordpressPluginDB])

    with db.atomic():
        for index in range(0, len(data), 10):
            WordpressPluginDB.insert_many(data[index:index + 10]).execute()


@time_counter()
def write_image():
    data = read_csv()
    for item in data:
        title = item['title']
        src = item['src']
        image = ImageParser(s, title, src)
        image.save_image()


@time_counter()
def get_data_write_csv():
    parser = WordpressPluginParser(s)
    parser.get_all_data()


def main():
    while True:
        print(f"""{Fore.YELLOW}
        What do you want to do?
        1 - get data from site and write it down to csv file
        2 - fetch data from csv file and write it down to database
        3 - download images   
        4 - exit
        """)
        question = input()
        if question == '1':
            get_data_write_csv()
        elif question == '2':
            write_to_db()
        elif question == '3':
            write_image()
        elif question == '4':
            print(f'{Fore.LIGHTCYAN_EX}Good bye!')
            break
        else:
            print(f'{Fore.RED}Do the correct choice!')


if __name__ == '__main__':
    main()
