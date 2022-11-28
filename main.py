from matplotlib import pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd
from scrapers.carrefour import CarrefourScraper
from scrapers.coto import CotoScraper
from scrapers.constants import CARREFOUR_ASADITO, COTO_ASADITO, DIA_ASADITO, DISCO_ASADITO, JUMBO_ASADITO, PATH
from scrapers.dia import DiaScraper
from scrapers.disco import DiscoScraper
from scrapers.dolar_hoy import DolarHoyScraper
from scrapers.jumbo import JumboScrapper
from scrapers.constants import today
import seaborn as sns
from twitter.bot import TwitterBot
from twitter.constants import API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


def data_to_csv(products_and_prices: dict) -> None:
    """Guarda los datos extraídos por los scrapers en el DataFrame 'asaditos.csv'

        Args:
            products_and_prices: Un diccionario con productos y sus precios. Se pasa el atributo que tiene el mismo
            nombre en las clases scrapers

        Returns:
                None
        """
    global df

    df_dictionary = pd.DataFrame([products_and_prices])  # Se pasa a dict a DF para poder utilizar pd.concat abajo
    df = pd.concat([df, df_dictionary], ignore_index=True)
    df.to_csv(f'{PATH}/asaditos.csv')


#################### EJECUCIÓN DEL CÓDIGO ####################

#### CARGA DE DFs ####

# Este es el df principal
df = pd.read_csv(f'{PATH}/asaditos.csv', index_col=0)
# df_anterior se carga para el caso en que no se pueda hacer el scraping de un precio.
df_anterior = pd.read_csv(f'{PATH}/asaditos.csv', index_col='supermercado').tail(5)
df_anterior.drop(columns='Unnamed: 0', inplace=True)
fecha_df_anterior = df_anterior.tail(1)['fecha'].values[0]
df_min_max_prom = pd.read_csv(f'{PATH}/min_max_prom.csv')
df_min_max_prom.drop(columns='Unnamed: 0', inplace=True)
cotizacion_anterior = df_min_max_prom.tail(1)['promedio_ccl'].values[0]

# #### EXTRACCIÓN Y GUARDADO DE PRECIOS ####

print('Iniciando con Carrefour...')
asado_carrefour = CarrefourScraper(products=CARREFOUR_ASADITO, df_anterior=df_anterior)
asado_carrefour.scrape_prices()
data_to_csv(asado_carrefour.products_and_prices)
print(f'{asado_carrefour.products_and_prices}\n')

print('Iniciando con Coto...')
asado_coto = CotoScraper(products=COTO_ASADITO, df_anterior=df_anterior)
asado_coto.scrape_prices()
data_to_csv(asado_coto.products_and_prices)
print(f'{asado_coto.products_and_prices}\n')

print('Iniciando con Día...')
asado_dia = DiaScraper(products=DIA_ASADITO, df_anterior=df_anterior)
asado_dia.scrape_prices()
data_to_csv(asado_dia.products_and_prices)
print(f'{asado_dia.products_and_prices}\n')

print('Iniciando con Disco...')
asado_disco = DiscoScraper(products=DISCO_ASADITO, df_anterior=df_anterior)
asado_disco.scrape_prices()
data_to_csv(asado_disco.products_and_prices)
print(f'{asado_disco.products_and_prices}\n')

print('Iniciando con Jumbo...')
asado_jumbo = JumboScrapper(products=JUMBO_ASADITO, df_anterior=df_anterior)
asado_jumbo.scrape_prices()
data_to_csv(asado_jumbo.products_and_prices)
print(f'{asado_jumbo.products_and_prices}\n')
asado_jumbo.price_log('---------------------------------------------------\n')

print('Iniciando con DolarHoy...')
scraper_dolar_hoy = DolarHoyScraper(cotizacion_anterior=cotizacion_anterior)
dolar_ccl = scraper_dolar_hoy.get_dollar_price()
print(f'Precio del Dolar CCL: {dolar_ccl}\n')

#### GUARDADO DE PRECIOS MÍNIMOS, MÁXIMOS Y PROMEDIO ####

# Se crea el df para extraer la información
df_today = df.tail(5).copy()

# Precio mínimo, máximo y promedio (anterior y actual)
precio_minimo = df_today.loc[df_today['precio_total'].idxmin()]['precio_total']
supermercado_min = df_today.loc[df_today['precio_total'].idxmin()]['supermercado']
precio_maximo = df_today.loc[df_today['precio_total'].idxmax()]['precio_total']
supermercado_max = df_today.loc[df_today['precio_total'].idxmax()]['supermercado']

precio_promedio_anterior = df_min_max_prom.iloc[-1]['promedio']
precio_promedio_actual = round(np.mean(df_today['precio_total']), 2)
precio_promedio_actual_ccl = round(precio_promedio_actual / dolar_ccl, 2)
var_precio_promedio = (precio_promedio_actual - precio_promedio_anterior) / precio_promedio_anterior * 100.0
var_precio_promedio = round(var_precio_promedio, 2)

# Guardado en df_min_max_prom y en archivo min_max_prom.csv
min_max_prom_dict = {'fecha': today, 'minimo': precio_minimo, 'super_minimo': supermercado_min,
                     'maximo': precio_maximo, 'super_maximo': supermercado_max,
                     'promedio': precio_promedio_actual, 'promedio_ccl': precio_promedio_actual_ccl}
df_dictionary_min_max_prom = pd.DataFrame([min_max_prom_dict])
df_min_max_prom = pd.concat([df_min_max_prom, df_dictionary_min_max_prom], ignore_index=True)
df_min_max_prom.to_csv(f'{PATH}/min_max_prom.csv')

primer_precio_promedio = df_min_max_prom.iloc[0]['promedio']  # Primer precio promedio
fecha_primer_precio_promedio = df_min_max_prom.iloc[0]['fecha']
var_promedio_primer_precio = round((precio_promedio_actual - primer_precio_promedio) / primer_precio_promedio * 100.0,
                                   2)
precio_promedio_4_semanas_atras = df_min_max_prom.iloc[-5]['promedio']  # 4 semanas atrás
fecha_precio_promedio_4_semanas_atras = df_min_max_prom.iloc[-5]['fecha']
var_promedio_4_semanas = round(
    (precio_promedio_actual - precio_promedio_4_semanas_atras) / precio_promedio_4_semanas_atras * 100.0, 2)

print(primer_precio_promedio, var_promedio_primer_precio, fecha_primer_precio_promedio)
print(precio_promedio_4_semanas_atras, var_promedio_4_semanas, fecha_precio_promedio_4_semanas_atras)

#### LINE PLOT ####

fig, ax = plt.subplots()
sns.set_theme(style='ticks')
fecha, precio_total, hue = df['fecha'], df['precio_total'], df['supermercado'].str.title()
lineplot = sns.lineplot(x=fecha, y=precio_total, hue=hue, linewidth=2.5, palette="Paired")
lineplot.set(ylabel='Precio del Asadito', xlabel='')
lineplot.yaxis.set_major_formatter('${x:1.0f}')
# my_locator = mtick.IndexLocator(base=2, offset=0)  # Para mostrar cada 2
# lineplot.xaxis.set_major_locator(my_locator)  # Para mostrar cada 2
plt.xticks(fontsize=6.5, rotation=45)
plt.title('Evolución del Precio del Asadito en el Tiempo', x=0.5, y=1.07)
plt.legend(ncol=6, bbox_to_anchor=(0, 1), loc='lower left', fontsize=7.7)
fig.set_size_inches(8, 5)  #
plt.savefig(f'{PATH}/lineplot_asaditos.png', dpi=400)

#### BAR PLOT ####

# Se crea el df para el barplot
df_barplot = df.tail(5).copy()
df_barplot.set_index('supermercado', inplace=True)
df_barplot.index = df_barplot.index.str.title()
df_barplot = df_barplot.sort_values('precio_total')
df_barplot.drop(columns=['fecha', 'precio_total'], inplace=True)
df_barplot.columns = df_barplot.columns.str.title()

# Bar plot vertical
sns.set(style='ticks')
ax_bar_plot = df_barplot.plot(kind='bar', stacked=True)
# Pone labels a las barras
for c in ax_bar_plot.containers:
    labels = [f'${int(v.get_height())}' if v.get_height() > 0 else '' for v in c]
    ax_bar_plot.bar_label(c, labels=labels, label_type='center', fontsize=6.5)
# Legends y salvado
ax_bar_plot.legend(ncol=6, bbox_to_anchor=(0, 1), loc='lower left', fontsize=7.7)
ax_bar_plot.yaxis.set_major_formatter('${x:1.0f}')
plt.xticks(fontsize=8, rotation=45)
plt.title('Composición del Precio de los Asaditos', x=0.5, y=1.07)
plt.savefig(f'{PATH}/barplot_asaditos.png', dpi=400)

##### LINE PLOT CON TWIN AXES #####

# Hace el plot
fig, ax = plt.subplots()
plt.title('Evolución del Precio Promedio del Asadito en Pesos y en Dólares (CCL)', x=0.5, y=1.05, fontsize=20)

# Agrega las líneas
g = sns.lineplot(ax=ax, x="fecha", y="promedio", data=df_min_max_prom, color='g', linewidth=2)
g.yaxis.set_major_formatter('${x:1.0f}')
plt.xticks(rotation=45)
g.set(ylabel='Precio Promedio en Pesos', xlabel='')
# my_locator = mtick.IndexLocator(base=2, offset=0)  # Para mostrar cada 2
# g.xaxis.set_major_locator(my_locator)  # Para mostrar cada 2
b = sns.lineplot(ax=g.axes.twinx(), x="fecha", y="promedio_ccl", data=df_min_max_prom, color='b', linewidth=2)
b.yaxis.set_major_formatter('US${x:.2f}')
b.set(ylabel='Precio Promedio en Dólares (CCL)')
sns.set(style='ticks')
g.legend(handles=[Line2D([], [], marker='_', color="g", label='Precio Promedio en Pesos'),
                  Line2D([], [], marker='_', color="b", label='Precio Promedio en Dólares (CCL)')],
         ncol=6, bbox_to_anchor=(0, 1), loc='lower left', fontsize=10)
fig.set_size_inches(12, 8)
plt.savefig(f'{PATH}/lineplot_asaditos_twin.png', dpi=200)

#### POSTEO EN TWITTER ####

print('Posteando en Twitter...')
twitter_bot = TwitterBot(API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
primer_tweet = twitter_bot.post_tweet(precio_promedio=precio_promedio_actual,
                                      variacion_promedio=var_precio_promedio,
                                      fecha_anterior=fecha_df_anterior)
segundo_tweet = twitter_bot.post_reply_1(super_min=supermercado_min, precio_min=precio_minimo,
                                         super_max=supermercado_max, precio_max=precio_maximo,
                                         reply_to=primer_tweet)
tercer_tweet = twitter_bot.post_reply_2(reply_to=segundo_tweet, var_precio_actual=var_precio_promedio,
                                        fecha_semana_pasada=fecha_df_anterior,
                                        var_precio_4_semanas=var_promedio_4_semanas,
                                        fecha_4_semanas=fecha_precio_promedio_4_semanas_atras,
                                        var_precio_inicial=var_promedio_primer_precio,
                                        fecha_inicial=fecha_primer_precio_promedio)
print('...Listo!')
