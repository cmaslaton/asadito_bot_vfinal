from bs4 import BeautifulSoup
from scrapers.carrefour import CarrefourScraper
from scrapers.constants import today
import requests


class DiaScraper(CarrefourScraper):
    def scrape_prices(self) -> None:
        # Agrega nombre del supermercado y fecha de la extracción de datos a products_with_prices
        self.products_and_prices['supermercado'] = 'dia'
        self.products_and_prices['fecha'] = today

        for product, product_url in self.products.items():
            # Intenta obtener el precio del artículo
            try:
                response = requests.get(f'https://diaonline.supermercadosdia.com.ar/{product_url}/p')
                price = BeautifulSoup(response.content, 'html.parser').find('span',
                                                                            class_='vtex-product-specifications-1-x-specificationValue vtex-product-specifications-1-x-specificationValue--first vtex-product-specifications-1-x-specificationValue--last')
                price = float(price.string)
                # Procesa el precio (lo modifica dependiendo si se trata de asado, lechuga o tomate)
                price = self.procesa_precio(product, price)
                print(f'Producto: {product} - ${price} (precio actualizado)')
                dato = f'{self.products_and_prices["fecha"]} - {self.products_and_prices["supermercado"]} - '
                dato += f'{product} - {price} - actualizado\n'
            # Si no puede, completa el precio del artículo con el precio inmediato anterior
            except:
                price = self.df_anterior.loc['dia'][product]
                print(f'Producto: {product} - ${price} (precio viejo)')
                dato = f'{self.products_and_prices["fecha"]} - {self.products_and_prices["supermercado"]} - '
                dato += f'{product} - {price} - ---------------\n'
            # Arma el diccionario -> articulo:precio
            self.products_and_prices[product] = price
            self.price_log(dato)
        self.total_price()

    def procesa_precio(self, product, price):
        if product == 'morcilla':
            return round(price / 400 * self.norm_products[product], 2)
        elif product == 'coca':
            return round(price * 2.25, 2)
        else:
            return round(price / 1000 * self.norm_products[product], 2)
