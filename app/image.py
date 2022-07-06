import os
from string import punctuation


class ImageParser:
    def __init__(self, session, title, src) -> None:
        self.session = session
        self.title = title
        self.src = src

    def get_image_obj(self):
        response = self.session.get(self.src, stream=True)
        if response.ok:
            return response
        return response.status_code

    def refine_title(self):
        symbols = f'{punctuation}–'
        title = self.title.replace(' ', '')
        title_words_list = [
            letter for letter in title if letter not in symbols]
        return ''.join(title_words_list)

    def get_extension(self):
        return self.src.split('/')[-1].split('?')[0].split('.')[-1]

    def get_path(self):
        title = self.refine_title()
        extension = self.get_extension()

        file_name = f'{title}.{extension}'

        if not os.path.exists('images'):
            os.mkdir('images')

        return os.path.abspath(f'images/{file_name}')

    def save_image(self):
        img_obj = self.get_image_obj()
        path = self.get_path()

        with open(path, 'wb') as f:
            for chunk in img_obj.iter_content(8192):
                f.write(chunk)
