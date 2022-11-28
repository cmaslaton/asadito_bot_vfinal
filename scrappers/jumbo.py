from bs4 import BeautifulSoup
from scrapers.carrefour import CarrefourScraper
from scrapers.constants import today
import requests


class JumboScrapper(CarrefourScraper):
    def scrape_prices(self) -> None:
        # Agrega nombre del supermercado y fecha de la extracción de datos a products_with_prices
        self.products_and_prices['supermercado'] = 'jumbo'
        self.products_and_prices['fecha'] = today

        for product, product_url in self.products.items():
            # Intenta obtener el precio del artículo
            try:
                response = requests.get(f'https://www.jumbo.com.ar/{product_url}/p')
                jumbo_soup = BeautifulSoup(response.content, 'html.parser').find('strong', class_='skuBestPrice')
                price = float(jumbo_soup.string.replace('$ ', '').replace('.', '').replace(',', '.'))
                # Procesa el precio (lo modifica dependiendo si se trata de asado, lechuga o tomate)
                price = self.procesa_precio(product, price)
                print(f'Producto: {product} - ${price} (precio actualizado)')
                dato = f'{self.products_and_prices["fecha"]} - {self.products_and_prices["supermercado"]} - '
                dato += f'{product} - {price} - actualizado\n'
            # Si no puede, completa el precio del artículo con el precio inmediato anterior
            except:
                price = self.df_anterior.loc['jumbo'][product]
                print(f'Producto: {product} - ${price} (precio viejo)')
                dato = f'{self.products_and_prices["fecha"]} - {self.products_and_prices["supermercado"]} - '
                dato += f'{product} - {price} - ---------------\n'
            # Arma el diccionario -> articulo:precio
            self.products_and_prices[product] = price
            self.price_log(dato)
        self.total_price()
