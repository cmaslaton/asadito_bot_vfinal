from bs4 import BeautifulSoup
from scrapers.carrefour import CarrefourScraper
from scrapers.constants import today
import re
import requests


class CotoScraper(CarrefourScraper):
    def scrape_prices(self) -> None:
        coto_url = 'https://www.cotodigital3.com.ar/sitios/cdigi/producto'
        # Agrega nombre del supermercado y fecha de la extracción de datos a products_with_prices
        self.products_and_prices['supermercado'] = 'coto'
        self.products_and_prices['fecha'] = today

        for product, product_url in self.products.items():
            # Intenta obtener el precio del artículo
            try:
                response = requests.get(f'{coto_url}/{product_url}')
                coto_soup = BeautifulSoup(response.content, 'html.parser').find(class_='atg_store_newPrice').text
                price = float(
                    re.findall("\$[0-9.,]*", coto_soup)[0].replace('$', '').replace('.', '').replace(',', '.'))
                # Procesa el precio (lo modifica dependiendo si se trata de asado, lechuga o tomate)
                price = self.procesa_precio(product, price)
                print(f'Producto: {product} - ${price} (precio actualizado)')
                dato = f'{self.products_and_prices["fecha"]} - {self.products_and_prices["supermercado"]} - '
                dato += f'{product} - {price} - actualizado\n'
            # Si no puede, completa el precio del artículo con el precio inmediato anterior
            except:
                price = self.df_anterior.loc['coto'][product]
                print(f'Producto: {product} - ${price} (precio viejo)')
                dato = f'{self.products_and_prices["fecha"]} - {self.products_and_prices["supermercado"]} - '
                dato += f'{product} - {price} - ---------------\n'
            # Arma el diccionario -> articulo:precio
            self.products_and_prices[product] = price
            self.price_log(dato)
        self.total_price()
