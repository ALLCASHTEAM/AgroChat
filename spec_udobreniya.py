import requests
from bs4 import BeautifulSoup


def write_product_info():
    with open(f"spec_udobreniya.txt", "w+", encoding="utf-8") as file:

        pages = ["https://betaren.ru/catalog/spetsialnye-udobreniya/?PAGEN_1=1",
                 "https://betaren.ru/catalog/spetsialnye-udobreniya/?PAGEN_1=2"]
        for page in pages:
            req = requests.get(page)
            soup = BeautifulSoup(req.text, 'html.parser')  # catalog-items__tile catalog-el-for-loadmore
            for pr in soup.find_all('div', class_='catalog-items__tile catalog-el-for-loadmore'):
                name = pr.find('a', class_='h2-like').text.replace('-', ' ').replace('+', '')
                type = pr.find('p', class_='preview-text-p').text.replace('\n', ' ').replace(' ',' ').strip().strip().strip()
                file.write(f"{name} - {type}\n")


if __name__ == '__main__':
    write_product_info()

