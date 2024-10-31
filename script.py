import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import matplotlib.pyplot as plt

def questao_1():
    # URL do subreddit
    url = 'https://www.reddit.com/r/programming/'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        posts = soup.find_all('div', class_='_1oQyIsiPHYt6nx7VOmd1sz', limit=3)

        data = []
        for post in posts:
            title = post.find('h3').text
            upvotes = post.find('div', class_='_1rZYMD_4xY3gRcSS3p8ODO').text
            link = post.find('a', class_='SQnoC3ObvgnGjWt90zD9Z')['href']
            data.append([title, upvotes, link])

        df = pd.DataFrame(data, columns=['Title', 'Upvotes', 'Link'])
        df.to_excel('reddit_posts.xlsx', index=False)
    else:
        print('Erro ao acessar o site')

    print('Web scraping concluído!')

def questao_2():
    with open('api_response.json', 'r') as file:
        data = json.load(file)

    offers = []
    for item in data['results']:
        offer_link = item['offer_link']
        image_link = item['image_link']
        price = item['price']
        title = item['title']
        offers.append([offer_link, image_link, price, title])

    df = pd.DataFrame(offers, columns=['Offer Link', 'Image Link', 'Price', 'Title'])
    df.to_csv('offers.csv', index=False)

    print('Ofertas extraídas e salvas em offers.csv!')

def questao_3():
    url = 'https://www.magazineluiza.com.br/aparador-pelos-philips-one-blade-qp1424-10-philips-novo/p/237634500/pf/papp/'

    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find('h1', class_='header-product__title').text.strip()
    stock_availability = 'Disponível' if soup.find('div', class_='available') else 'Indisponível'
    price = soup.find('span', class_='price-template__text').text.strip()

    product_info = {
        'title': title,
        'stock_availability': stock_availability,
        'price': price
    }

    with open('product_info.json', 'w') as file:
        json.dump(product_info, file, indent=4)

    print('Informações do produto capturadas e salvas em product_info.json!')

def questao_4():
    df = pd.read_json('dados_compra.json')

    print(df.head())
    print(df.isnull().sum())

    total_compras = df.shape[0]
    media_gasto = df['valor_venda'].mean()
    min_gasto = df['valor_venda'].min()
    max_gasto = df['valor_venda'].max()
    produto_mais_caro = df.loc[df['valor_venda'].idxmax()]
    produto_mais_barato = df.loc[df['valor_venda'].idxmin()]

    distribuicao_genero = df['genero'].value_counts()
    total_gasto_por_genero = df.groupby('genero')['valor_venda'].sum()

    distribuicao_genero.plot(kind='bar', title='Distribuição de Gênero')
    plt.xlabel('Gênero')
    plt.ylabel('Contagem')
    plt.show()

    total_gasto_por_genero.plot(kind='bar', title='Total Gasto por Gênero')
    plt.xlabel('Gênero')
    plt.ylabel('Total Gasto')
    plt.show()

    print(f'Total de Compras: {total_compras}')
    print(f'Média de Gasto por Compra: {media_gasto}')
    print(f'Gasto Mínimo: {min_gasto}')
    print(f'Gasto Máximo: {max_gasto}')
    print(f'Produto Mais Caro: {produto_mais_caro}')
    print(f'Produto Mais Barato: {produto_mais_barato}')

if __name__ == "__main__":
    questao_1()
    questao_2()
    questao_3()
    questao_4()
