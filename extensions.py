import requests
import json
from config import keys

class ConvertionException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if base == quote:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты \'{base}\'.\nЕсли у вас возникли сложности, вызовите команду /help.')

        base_ticker, quote_ticker = keys[base], keys[quote]

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту \'{base}\'.\nЕсли у вас возникли сложности, вызовите команду /help.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту \'{quote}\'.\nЕсли у вас возникли сложности, вызовите команду /help.')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество \'{amount}\'.\nЕсли у вас возникли сложности, вызовите команду /help.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total_quote = json.loads(r.content)[keys[quote]]

        return total_quote