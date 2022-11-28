from bs4 import BeautifulSoup
from scrapers.constants import today, PATH
import requests


class CarrefourScraper:
    def __init__(self, products, df_anterior):
        self.products = products
        self.products_and_prices = dict()
        self.norm_products = {'asado': 2000, 'chorizo': 800, 'morcilla': 1000, 'lechuga': 350, 'tomate': 500}
        self.df_anterior = df_anterior

    def scrape_prices(self) -> None:
        """Extrae los precios de los artículos que se pasan en el atributo 'products' y arma el diccionario
           del atributo 'products_with_prices'

        Args:
            No necesita argumentos

        Returns:
            float, int o string: El precio de artículo (float o int) o N/A (str) si no pudo encontrarlo
        """
        # Agrega nombre del supermercado y fecha de la extracción de datos a products_with_prices
        self.products_and_prices['supermercado'] = 'carrefour'
        self.products_and_prices['fecha'] = today
        for product, product_url in self.products.items():
            # Intenta obtener el precio del artículo
            try:
                response = requests.get(f'https://www.carrefour.com.ar/{product_url}/p')
                carrefour_soup = BeautifulSoup(response.content, 'html.parser').find('span',
                                                                                     class_='lyracons-carrefourarg-product-price-1-x-currencyInteger')
                price = float(carrefour_soup.string)
                # Procesa el precio (lo modifica dependiendo si se trata de asado, lechuga o tomate)
                price = self.procesa_precio(product, price)
                print(f'Producto: {product} - ${price} (precio actualizado)')
                dato = f'{self.products_and_prices["fecha"]} - {self.products_and_prices["supermercado"]} - '
                dato += f'{product} - {price} - actualizado\n'
            # Si no puede, completa el precio del artículo con el precio inmediato anterior
            except:
                price = self.df_anterior.loc['carrefour'][product]
                print(f'Producto: {product} - ${price} (precio viejo)')
                dato = f'{self.products_and_prices["fecha"]} - {self.products_and_prices["supermercado"]} - '
                dato += f'{product} - {price} - ---------------\n'
            self.products_and_prices[product] = price
            self.price_log(dato)
        self.total_price()

    def price_log(self, dato):
        with open(f'{PATH}/price_log.txt', 'a') as f:
            f.write(dato)

    def procesa_precio(self, product, price):
        """ Modifica el precio según el tipo de artículo que se ingrese

        Args:
            No necesita argumentos

        Returns
            int o float: el precio del artículo
        """
        if product != 'coca':
            return round(price / 1000 * self.norm_products[product], 2)
        return price

    def total_price(self) -> None:
        """Agrega el precio total del asadito al atributo products_with_prices

        Args:
            No necesita argumentos

        Returns
            None
        """
        # Inicializa el contador
        total_price_counter = 0
        # Si el precio es un float o un int, lo suma al contador
        for price in self.products_and_prices.values():
            if isinstance(price, float) or isinstance(price, int):
                total_price_counter += price
        self.products_and_prices['precio_total'] = round(total_price_counter, 2)
