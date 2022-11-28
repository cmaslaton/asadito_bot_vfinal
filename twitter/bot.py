import tweepy
from scrapers.constants import PATH


class TwitterBot:
    def __init__(self, api_key: str, api_key_secret: str, consumer_key: str, consumer_key_secret: str):
        self.api_key = api_key
        self.api_key_secret = api_key_secret
        self.consumer_key = consumer_key
        self.consumer_key_secret = consumer_key_secret

    def post_tweet(self, precio_promedio, variacion_promedio, fecha_anterior):
        """Postea el primer tweet

        Args:
            No lleva

        Returns
            El posteo del primer tweet
        """
        auth = tweepy.OAuthHandler(self.api_key, self.api_key_secret)
        auth.set_access_token(self.consumer_key, self.consumer_key_secret)
        api = tweepy.API(auth)
        first_tweet = 'Este finde, hacer un asadito para 4 personas con 2 kg de asado, 4 chorizos, morcilla rosca,'
        first_tweet += ' 500 gr de tomate, 350 gr de lechuga y una coca de 2.25 lts te sale, en promedio,'
        first_tweet += f' ${float(precio_promedio):g}.'
        if variacion_promedio > 0:
            first_tweet += f' Esto representa un aumento del {variacion_promedio}% respecto de la medición anterior'
        elif variacion_promedio < 0:
            first_tweet += f' Esto representa una caída del {abs(variacion_promedio)}% respecto de la medición anterior'
        else:
            first_tweet += f' Esto indica que no hubo variaciones respecto de la medición anterior'
        first_tweet += f' ({fecha_anterior}).'
        # print(first_tweet)
        return api.update_status(status=first_tweet)

    def post_reply_1(self, reply_to, precio_min, super_min, precio_max, super_max):
        """Postea las respuestas tweet

        Args:
            reply_to: El tweet al que responde

        Returns
            El posteo del primer tweet
        """
        auth = tweepy.OAuthHandler(self.api_key, self.api_key_secret)
        auth.set_access_token(self.consumer_key, self.consumer_key_secret)
        api = tweepy.API(auth)
        tweet_text = f'El precio mínimo de un asadito para 4 personas se registró en el supermercado '
        tweet_text += f'{super_min.title()} (${float(precio_min):g}) y el máximo en el supermercado '
        tweet_text += f'{super_max.title()} (${float(precio_max):g}).'
        # print(tweet_text)
        return api.update_status(status=tweet_text, in_reply_to_status_id=reply_to.id)

    def post_reply_2(self, reply_to, var_precio_actual, fecha_semana_pasada, var_precio_4_semanas, fecha_4_semanas,
                     var_precio_inicial, fecha_inicial):
        """Postea las respuestas tweet

        Args:
            reply_to: El tweet al que responde

        Returns
            El posteo del primer tweet
        """
        auth = tweepy.OAuthHandler(self.api_key, self.api_key_secret)
        auth.set_access_token(self.consumer_key, self.consumer_key_secret)
        api = tweepy.API(auth)
        tweet_text = f'A la fecha, la variación del precio promedio de un asadito (el #AsaditoIndex) es de: '
        # VARIACIÓN CONTRA SEMANA PASADA
        if var_precio_actual > 0:
            tweet_text += f'+{var_precio_actual}% respecto de la medición de la semana pasada ({fecha_semana_pasada}), '
        elif var_precio_actual < 0:
            tweet_text += f'{var_precio_actual}% respecto de la medición de la semana pasada ({fecha_semana_pasada}), '
        else:
            tweet_text += f'0% (sin variaciones respecto de la medición de la semana pasada), '
        # VARIACIÓN CONTRA 4 SEMANAS
        if var_precio_4_semanas > 0:
            tweet_text += f'+{var_precio_4_semanas}% respecto de la medición de hace 4 semanas ({fecha_4_semanas}) y '
        elif var_precio_4_semanas < 0:
            tweet_text += f'{var_precio_4_semanas}% respecto de la medición de hace 4 semanas ({fecha_4_semanas}) y '
        else:
            tweet_text += f'0% (sin variaciones respecto de la medición de hace 4 semanas) y '
        # VARIACIÓN CONTRA PRIMERA MEDICIÓN
        if var_precio_inicial > 0:
            tweet_text += f'+{var_precio_inicial}% respecto de la primera medición ({fecha_inicial}).'
        elif var_precio_4_semanas < 0:
            tweet_text += f'{var_precio_inicial}% respecto de la primera medición ({fecha_inicial}).'
        else:
            tweet_text += f'0% (sin variaciones respecto de la primera medición).'
        # Agrega los archivos
        filenames = [f'{PATH}/barplot_asaditos.png',
                     f'{PATH}/lineplot_asaditos.png',
                     f'{PATH}/lineplot_asaditos_twin.png']
        media_ids = []
        for filename in filenames:
            res = api.media_upload(filename)
            media_ids.append(res.media_id)
        # Publica el tweet
        # print(tweet_text)
        return api.update_status(media_ids=media_ids, status=tweet_text, in_reply_to_status_id=reply_to.id)
