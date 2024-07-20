import requests
import json
from flask import Flask


def get_valutes_list() -> list:
    """
    Загружает список котировок с сайта www.cbr-xml-daily.ru в формате JSON.
    :return: Список котировок в виде списка словарей.
    """
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    response = requests.get(url)
    data = json.loads(response.text)
    valutes = list(data['Valute'].values())
    return valutes


app = Flask(__name__)


def create_html(valutes) -> str:
    """
    Создает стилизованный вывод котировок в виде таблицы с заголовком.

    ВНИМАНИЕ:
    Для вывода заголовка таблицы использует названия ключей из первого элемента списка.
    Поэтому требуется, что бы все последущие элементы списка имели такие же ключи, как и в первом элементе.
    :param valutes: Котировки в виде списка словарей.
    :return: Возвращает HTML-страницу с таблицей котировок в виде строки.
    """
    text = '<h1>Курс валют</h1>'
    text += '''
    <style>
    * {
        padding: 0.75rem;
    }
    table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
    }
    th {
        background-color: #D6EEFF;
    }
    tr:nth-child(even) {
        background-color: #D6EEEE;
    }
    tr:nth-child(odd) {
        background-color: #D6FFFF;
    }
    </style>
    '''
    text += '<table>'

    # Выводим заголовок таблицы
    text += '<tr>'
    column_names = valutes[0].keys() if len(valutes) > 0 else list()
    for name in column_names:
        text += f'<th>{name}</th>'
    text += '</tr>'

    # Выводим тело таблицы
    for valute in valutes:
        text += '<tr>'
        for name in column_names:
            text += f'<td>{valute[name]}</td>' if name in valute else 'Нет значения'
        text += '</tr>'
    text += '</table>'

    # Возвращаем сформированную страницу
    return text


@app.route("/")
def index():
    valutes = get_valutes_list()
    html = create_html(valutes)
    return html


if __name__ == "__main__":
    app.run()
