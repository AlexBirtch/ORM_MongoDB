import csv
import re
from pymongo import MongoClient
import datetime as dt
from pprint import pprint
import os


def read_data(csv_file, db):
    """
    Загрузить данные в бд из CSV-файла
    """
    with open(csv_file, encoding='utf8') as csvfile:
        # прочитать файл с данными и записать в коллекцию
        csv_reader = csv.DictReader(csvfile)
        artists_list = list(csv_reader)
        uniq_id = 0
        list_for_db = []
        for artist in artists_list:
            uniq_id += 1
            artist_info = {'_id': uniq_id,
                           'Исполнитель': artist['Исполнитель'],
                           'Цена': int(artist['Цена']),
                           'Место': artist['Место'],
                           'Дата': dt.datetime.strptime('2020 ' + artist['Дата'], '%Y %d.%m')}

            list_for_db.append(artist_info)

        db.insert_many(list_for_db)


def find_cheapest(db):
    """
    Отсортировать билеты из базы по возрастанию цены
    Документация: https://docs.mongodb.com/manual/reference/method/cursor.sort/
    """
    tikets = list(db.find().sort('Цена', 1))
    print('Отсортированные билеты из базы по возрастанию цены')
    for ticket in tikets:
        pprint(ticket)



def find_by_name(name, db):
    """
    Найти билеты по имени исполнителя (в том числе – по подстроке, например "Seconds to"),
    и вернуть их по возрастанию цены
    """
    arts = re.compile(name, re.IGNORECASE)
    result = list(db.find({'Исполнитель': arts}).sort('Цена', 1))
    print(f'Отсортированный поиск по имени исполнителя:')
    for line in result:
        pprint(line)


def find_by_date(db):
    """
    Реализовать сортировку по дате мероприятия.
    Найти билеты по дате (мероприятия с 1 по 30 июля.  $gte >=, $lte <=).
    Также отсортировал по дате
    """
    day_start = dt.datetime(2020, 7, 1)
    day_end = dt.datetime(2020, 7, 30)
    result = list(db.find({'Дата': {'$gte': day_start, '$lte': day_end}}).sort('Дата', 1))
    print(f'Сортировка по дате мероприятия с 1 по 30 июля:')

    for line in result:

        print(line)

if __name__ == '__main__':
    client = MongoClient()
    db = client['netology_test0_0_2']
    art_coll = db['artists']
    read_data('artists.csv', art_coll)
    find_cheapest(art_coll)
    find_by_name('Lil Jon', art_coll)
    find_by_date(art_coll)