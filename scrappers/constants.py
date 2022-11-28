from datetime import datetime as dt

##### LISTA DE PRODUCTOS DE LOS SUPERMERCADOS #####

CARREFOUR_ASADITO = {'asado': 'asado-de-novillito-x-kg-681248',
                     'chorizo': 'chorizo-parrillero-carrefour-envasado-al-vacio-x-kg',
                     'morcilla': 'morcilla-rosca-en-gancho-x-kg',
                     'lechuga': 'lechuga-capuchina-x-kg',
                     'tomate': 'tomate-x-kg',
                     'coca': 'gaseosa-coca-cola-sin-azucares-225-l'}

COTO_ASADITO = {'asado': '-asado-del-medio-estancias-coto-x-kg/_/A-00047979-00047979-200',
                'chorizo': '-chorizo-de-cerdo-ciudad-del-lago-x-kg/_/A-00036502-00036502-200',
                'morcilla': '-morcilla-rosca-ciudad-del-lago-x-kg/_/A-00036505-00036505-200',
                'lechuga': '-lechuga-capuchina-x-kg/_/A-00000648-00000648-200',
                'tomate': '-tomate-red-x-kg/_/A-00000684-00000684-200',
                'coca': '-gaseosa-coca-cola-sin-azucar-225-lt/_/A-00180416-00180416-200'}

DIA_ASADITO = {'asado': 'asado-de-novillito-envasado-al-vacio-x-1-kg-163188',
               'chorizo': 'chorizo-puro-cerdo-400-gr-1-un-262290',
               'morcilla': 'morcilla-comun-400-gr-262291',
               'lechuga': 'lechuga-capuchina-x-1-kg-90079',
               'tomate': 'tomate-redondo-x-1-kg-90127',
               'coca': 'gaseosa-coca-cola-sin-azucar-225-lt-121537'}

DISCO_ASADITO = {'asado': 'asado-del-centro-2',
                 'chorizo': 'chorizo-la-divisa',
                 'morcilla': 'morcilla-rosca-la-divisa',
                 'lechuga': 'lechuga-capuchina',
                 'tomate': 'tomate-redondo-grande-por-kg',
                 'coca': 'gaseosa-coca-cola-sin-azucar-2-25-lt'}

JUMBO_ASADITO = {'asado': 'asado-del-centro-2',
                 'chorizo': 'chorizo-la-divisa',
                 'morcilla': 'morcilla-rosca-la-divisa',
                 'lechuga': 'lechuga-capuchina',
                 'tomate': 'tomate-redondo-grande-por-kg',
                 'coca': 'gaseosa-coca-cola-sin-azucar-2-25-lt'}

PATH = r'C:/Users/Usuario/OneDrive/Escritorio/Pythoneta/asadito_bot/data'
# PATH = r'C:\Users\Carli\OneDrive\Escritorio\asadito_bot_vfinal\data'


#### FECHA DEL SCRAPING ####

today = dt.now().strftime('%d-%m-%Y')
