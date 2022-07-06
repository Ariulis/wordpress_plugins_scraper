from time import sleep
from random import uniform

from colorama import Fore

from source import URL, write_csv


class WordpressPluginParser:
    def __init__(self, sesssion) -> None:
        self.session = sesssion

    @staticmethod
    def refined_rating(string: str) -> str:
        rating = string.split()[0]
        return rating.replace(',', '')

    def get_html(self, url):
        r = self.session.get(url)
        if r.ok:
            return r.html
        return r.status_code

    def get_articles(self, html):
        articles = html.find('article')
        data_list = []

        for article in articles:
            title = article.find('.entry-title a', first=True).text
            link = article.find('.entry-title a', first=True).attrs['href']
            rating = article.find('.rating-count a', first=True).text
            src = article.find('.entry-thumbnail img', first=True).attrs['src']
            data = {
                'title': title,
                'link': link,
                'rating': self.refined_rating(rating),
                'src': src
            }
            data_list.append(data)

        return data_list

    def get_page_data(self, articles):
        write_csv(articles)


    def get_all_data(self):
        counter = 23
        while True:
            url = URL.format(counter)
            html = self.get_html(url)
            articles = self.get_articles(html)
            self.get_page_data(articles)
            print(f'{Fore.GREEN}- The page #{counter} is done...')
            check_next_page = html.find('.nav-links a')[-1].text

            if check_next_page == 'Next':
                counter += 1
                sleep(uniform(1, 3))

            else:
                print(f'{Fore.CYAN}Everything is done!')
                break
