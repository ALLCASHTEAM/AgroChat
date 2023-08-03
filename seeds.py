import requests
from bs4 import BeautifulSoup

def write_product_info():
    with open(f"seeds.txt", "w+", encoding="utf-8") as file:
        pages = ["https://betaren.ru/catalog/semena/drazhirovannye-semena-sakharnoy-svekly/?PAGEN_1=1",
                     "https://betaren.ru/catalog/semena/drazhirovannye-semena-sakharnoy-svekly/?PAGEN_1=2",
                     "https://betaren.ru/catalog/semena/semena-ozimoy-pshenitsy/",
                     "https://betaren.ru/catalog/semena/semena-yarovoy-pshenitsy/",
                     "https://betaren.ru/catalog/semena/semena-soi/",
                     "https://betaren.ru/catalog/semena/semena-zernobobovykh-kultur/",
                     "https://betaren.ru/catalog/semena/semena-podsolnechnika/",
                     "https://betaren.ru/catalog/semena/semena-kukuruzy/",
                     "https://betaren.ru/catalog/semena/semena-rapsa/"]
        for page in pages:
            req = requests.get(page)
            soup = BeautifulSoup(req.text, 'html.parser')
            for pr in soup.find_all('div', class_='catalog-items__tile catalog-el-for-loadmore'):
                pre_type = pr.find('span', class_='active-i-text').text.replace('\n', ' ').replace('-', ' ').strip()
                name = pr.find('div', class_='product-name').text.replace('-', ' ').replace('+', '').strip()
                try:
                    type = pr.find('div', class_='preview-text').text.replace('-', ' ').replace('\n', ' ').strip()
                except:
                    type = 'МИМО'.strip()

                file.write(f"{pre_type} - {name} - {type}\n")


if __name__ == '__main__':
    write_product_info()