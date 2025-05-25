import pandas as pd

from operator import le
from typing import List, Dict, Any


# Здесь хранится обработанный dataframe из файла MO_dataset.csv
FEATURES = None # признаки
TARGET = None   # отклики



'''
Данная функция рассчитывает расстояние от дома
до метро в км при помощи открытого API (Нам
показывали что-то подобное на ХИОДе)
'''
def distance_from_address(
        district: str,
        street: str,
        house_number: str,
        metro_station: str
) -> float:
    distance = 0.978
    return distance


'''
Строим адрес и считаем расстояние
'''
def compute_distance(row):
    return distance_from_address(
        row['district'],
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

    # One-hot кодирование категориальных признаков
    categorical_cols = ['district', 'underground', 'materials', 'room_type']
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
    distance = distance_from_address(
        district, street, house_number, metro_station)

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
        f'underground_{metro_station}': 1,
        f'materials_{house_material}': 1,
        f'room_type_{room_type}': 1
    }
    # Все отсутствующие в row колонки заполняем нулями
    full_input_dict = {col: input_dict.get(col, 0) for col in FEATURES.columns.tolist()}

    # Итоговый входной dataframe для модели
    input_df = pd.DataFrame([full_input_dict])

    print("длина DataFrame: ", len(input_df.columns.tolist()))
    return input_df
