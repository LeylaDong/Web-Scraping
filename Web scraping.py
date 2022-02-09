from time import sleep
import requests
from bs4 import BeautifulSoup

    BASE_URL = 'https://www.barnesandnoble.com'
    URL = 'https://www.barnesandnoble.com/b/books/_/N-1fZ29Z8q8?Nrpp=40&page=1'
    AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56'

    deliminator = '========================================='


def download_product_pages():
    headers = {
        'User-Agent': AGENT,
    }
    list_page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(list_page.content, 'html.parser')

    # Get the list of URLs of the top 40 books.
    book_urls = [BASE_URL + a.get('href') for a in soup.select('h3.product-info-title > a')]

    # Download each product page of the top 40 books.
    for i in range(len(book_urls)):
        filename = 'bn_top100_{:02d}.htm'.format(i + 1)
        page = requests.get(book_urls[i], headers=headers)
        with open(filename, 'wb') as f:
            f.write(page.content)
        sleep(5)

def print_over_views():
    for i in range(40):
        filename = 'bn_top100_{:02d}.htm'.format(i + 1)
        content = None
        with open(filename, 'r') as f:
            content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
        input = soup.select("div.header-content input[id=productName]")[0];
        title = input.get("value")
        overview = soup.select('.overview-cntnt')[0].text.strip()
        print(deliminator)
        print(title)
        print(overview[0:100])

if __name__ == '__main__':
    download_product_pages()
    print_over_views()
