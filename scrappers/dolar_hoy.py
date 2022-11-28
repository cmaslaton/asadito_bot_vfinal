from bs4 import BeautifulSoup
import requests


class DolarHoyScraper:
    def __init__(self, cotizacion_anterior):
        self.url = 'https://dolarhoy.com/cotizacion-dolar-ccl'
        self.cotizacion_anterior = cotizacion_anterior

    def get_dollar_price(self):
        try:
            response = requests.get(self.url)
            dollar_soup = BeautifulSoup(response.content, 'html.parser').find_all('div', class_='value')
            return float(dollar_soup[1].text.replace('$', ''))
        except:
            return self.cotizacion_anterior
