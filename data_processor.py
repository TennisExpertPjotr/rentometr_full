from typing import List, Dict, Any

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


'''По названию станции метро возвращает число'''
def num_from_metro_name(metro_station: str) -> float:
    if metro_station != '':
        return 10.0
    else:
        return 0.01


'''По названию района возвращает число'''
def num_from_district_name(district: str) -> float:
    if district != '':
        return 10.0
    else:
        return 0.01


'''По типу материала возвращает число'''
def num_from_material(house_material: str) -> float:
    if house_material != '':
        return 10.0
    else:
        return 0.01


'''Возвращает число по типу комнаты'''
def num_from_room_type(room_type: str) -> float:
    if room_type == 'Студия':
        return -1.0
    elif room_type == '4+':
        return 4.0
    else:
        return float(room_type)


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

    distance = distance_from_address(
        district, street, house_number, metro_station)

    metro_num = num_from_metro_name(metro_station)
    district_num = num_from_district_name(district)
    num_material = num_from_material(data['house_material'])

    room_type = data['room_type']
    rooms_num = num_from_room_type(room_type)
    total_meters = float(data['total_meters'])
    floor = float(data['floor'])
    total_floors = float(data['total_floors'])
    balcony = float(data['balcony'])

    vector = [rooms_num,
              total_meters,
              floor,
              total_floors,
              district_num,
              metro_num,
              distance,
              balcony,
              num_material]

    return vector
