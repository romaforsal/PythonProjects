import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://books.toscrape.com/"

response = requests.get(url)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'html.parser')

books = soup.find_all('article', class_='product_pod')

titles = []
prices = []
ratings = []
images = []

rating_map = {
    'One': 1,
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5
}

for book in books:
    title = book.h3.a['title']
    price_text = book.find('p', class_='price_color').text.strip()

    # Limpieza más robusta del precio
    price_clean = (
        price_text.replace('£', '')
        .replace('Â', '')   # Elimina caracteres mal codificados
        .strip()
    )

    price = float(price_clean)

    rating_class = book.p['class'][1]
    rating = rating_map.get(rating_class, None)
    image_url = url + book.img['src'].replace('../', '')

    titles.append(title)
    prices.append(price)
    ratings.append(rating)
    images.append(image_url)

df = pd.DataFrame({
    'Título': titles,
    'Precio (£)': prices,
    'Rating (1-5)': ratings,
    'Imagen': images
})

df.to_csv('books_data.csv', index=False, encoding='utf-8-sig')

print("✅ Scraping completado correctamente.")
print(df.head())