import pandas as pd
import requests
import math

from dataclasses import dataclass
from operator import le
from typing import List, Dict, Any
from functools import lru_cache


# Здесь хранится обработанный dataframe из файла MO_dataset.csv
FEATURES = None # признаки
TARGET = None   # отклики

# Базовый url API
GEOAPI_BASE_URL = 'https://nominatim.openstreetmap.org/search'
# API требует уникальный User-Agent
USER_AGENT = 'RentometrFull/1.0 (rentometr_full@itmo.ru)'
CNT = 0
# Город
CITY = 'Санкт-Петербург'


@dataclass
class Coordinates:
    lat: float
    lon: float

    def get_radian(self):
        return RadCoordinates(
            math.radians(self.lat),
            math.radians(self.lon)
        )

@dataclass
class RadCoordinates:
    lat: float
    lon: float

@lru_cache()
def coordinates_from_address(
        address: str
) -> Coordinates | None:
    # Параметры запроса
    params = {'q': address, 'format': 'json', 'limit': 1, 'countrycodes': 'RU'}
    headers = {'User-Agent': USER_AGENT}

    # Выполнение запроса и проверка на наличие ошибки
    try:
        response = requests.get(GEOAPI_BASE_URL, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data:
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            return Coordinates(lat, lon)

        else:
            print('Адрес не найден')
            return None

    except requests.RequestException as e:
        print(f'Ошибка запроса: {e}')
        return None


def gowers_distance(
    c1: Coordinates,
    c2: Coordinates
) -> float:

    c1r, c2r = c1.get_radian(), c2.get_radian()

    dlat = c2r.lat - c1r.lat
    dlon = c2r.lon - c1r.lon

    # Формула гаверсинусов
    a = math.sin(dlat/2)**2 + math.cos(c1r.lat) * math.cos(c2r.lat) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Радиус Земли
    R = 6371

    distance = R * c

    return distance


'''
Данная функция рассчитывает расстояние от дома
до метро в км при помощи открытого API
'''
def distance_from_address(
        street: str,
        house_number: str,
        metro_station: str
) -> float:

    # Форматирование адресов
    flat_address = f'{CITY}, {street}, {house_number}'
    metro_address = f'{CITY}, станция метро {metro_station}'

    # Получение координат и проверка на ошибку
    try:
        flat_coords = coordinates_from_address(flat_address)
        metro_coords = coordinates_from_address(metro_address)

        if (flat_coords and metro_coords):
            distance = gowers_distance(flat_coords, metro_coords)
            return distance

        else:
            return None

    except Exception as e:
        print(f'Ошибка при расчёте: {e}')


'''
Строим адрес и считаем расстояние
'''
def compute_distance(row):
    return distance_from_address(
        row['street'],
        row['house_number'],
        row['underground']
    )


# Обработка количества комнат
def process_rooms_count(val):
    return 'студия' if val == -1 else str(val)


'''
Данная функция загружает .csv датафрейм и возвращает
вектор признаков и вектор откликов
'''
def load_dataframe(file_path):
    # Загрузка данных
    df = pd.read_csv(file_path, sep=';') # 'MO_dataset.csv'

    # Удалим столбец "author"
    df = df.drop(columns=['author'])

    # Добавляем столбец с типом квартиры
    df['room_type'] = df['rooms_count'].apply(process_rooms_count)
    df = df.drop(columns=['rooms_count'])  # заменили на room_type

    # Добавляем столбец с расстоянием
    df['distance'] = df.apply(compute_distance, axis=1)

    df.to_csv('intermediate_step.csv', index=False)
    #df = df.drop(columns=['underground'])

    # One-hot кодирование категориальных признаков
    categorical_cols = ['district', 'underground', 'materials', 'room_type']
    #categorical_cols = ['district', 'materials', 'room_type']
    df = pd.get_dummies(df, columns=categorical_cols, drop_first=False)

    # Получение финального вектора признаков (без price_per_month)
    features = df.drop(columns=['price_per_month', 'street', 'house_number'])

    # Получение вектора откликов
    target = df['price_per_month']

    return features, target


'''
Данная функция преобразует категориальное значение
в список в соответствии с принципом one-hot кодирования 
'''
def one_hot_encode(value: str, categories: List[str]) -> List[int]:
    return [1 if value == category else 0 for category in categories]


'''
Данная функция принимает текстовые значения с 
фронта и возвращает удобный для модели числовой
вектор
'''
def data_to_vector(data: Dict[str, Any]) -> List[float]:
    district = data['district']
    street = data['street']
    house_number = data['house_number']
    metro_station = data['metro_station']

    # Расстояние до метро
    distance = distance_from_address(street, house_number, metro_station)

    house_material = data['house_material']
    room_type = data['room_type']
    total_meters = float(data['total_meters'])
    floor = float(data['floor'])
    total_floors = float(data['total_floors'])


    # Формируем DataFrame
    input_dict = {
        'floor': floor,
        'floors_count': total_floors,
        'total_meters': total_meters,
        'distance': distance,
        f'district_{district}': 1,
        #f'underground_{metro_station}': 1,
        f'materials_{house_material}': 1,
        f'room_type_{room_type}': 1
    }
    # Все отсутствующие в row колонки заполняем нулями
    full_input_dict = {col: input_dict.get(col, 0) for col in FEATURES.columns.tolist()}

    # Итоговый входной dataframe для модели
    input_df = pd.DataFrame([full_input_dict])

    print("длина DataFrame: ", len(input_df.columns.tolist()))
    return input_df
