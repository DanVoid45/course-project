from currency_converter import CurrencyConverter
import functions
def convertation(request):
    class CurrencyError(Exception):
        pass
    c = CurrencyConverter()
    money = None
    from_currency = None
    to_currency = None
    list_of_conv = request.split()
    if len(list_of_conv) > 4:
        list_of_conv = list_of_conv[1:]
    else:
        print()
    while money is None:
        try:
            money = list_of_conv[0]
        except ValueError:
            return ("Скажите, к примеру: 50 долларов в рубли")
            break
    while from_currency is None:
        try:
            list_of_conv[0] = int(list_of_conv[0])
        except ValueError:
            return ("Скажите, к примеру: 50 долларов в рубли")
        try:
            if "руб" in list_of_conv[1]:
                from_currency = "RUB"
            elif "дол" in list_of_conv[1]:
                from_currency = "USD"
            elif "евр" in list_of_conv[1]:
                from_currency = "EUR"
            if from_currency not in c.currencies:
                raise CurrencyError

        except (CurrencyError, IndexError):
            from_currency = None
            return("Скажите, например: 50 долларов в рубли")
            break

    while to_currency is None:
        try:
            list_of_conv[0] = int(list_of_conv[0])
        except ValueError:
            return None
        try:
            if "руб" in list_of_conv[3]:
                to_currency = "RUB"
            elif "дол" in list_of_conv[3]:
                to_currency = "USD"
            elif "евр" in list_of_conv[3]:
                to_currency = "EUR"
            if to_currency not in c.currencies:
                raise CurrencyError

        except (CurrencyError, IndexError):
            to_currency = None
            return("Скажите, например: 50 долларов в рубли")
            break
    while True:
        try:
            return (f"{money} {from_currency} в {to_currency} - "
                f"{round(c.convert(money, from_currency, to_currency), 2)}")
            break
        except ValueError:
            return("Скажите, например: 50 долларов в рубли")
            break