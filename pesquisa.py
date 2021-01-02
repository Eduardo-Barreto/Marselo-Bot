import imgkit
import pyshorteners


def get_link(search):
    search = search.replace(' ', '+')

    url = f'https://www.google.com/search?&q={search}&ie=UTF-8&oe=UTF-8'

    shorted = pyshorteners.Shortener()
    url = shorted.tinyurl.short(url)

    return url


def get_screenshot(url):
    config = imgkit.config(
        wkhtmltoimage='C:/Program Files/wkhtmltopdf/bin/wkhtmltoimage.exe'
        # rasp '/usr/bin/wkhtmltoimage'
    )

    options = {
        'format': 'jpg',
        'crop-h': '1230',
        'crop-w': '1440',
        'crop-x': '0',
        'crop-y': '0',
        'encoding': "UTF-8",
        'quiet': '',
    }

    imgkit.from_url(url, 'screenshot.jpg', config=config, options=options)
