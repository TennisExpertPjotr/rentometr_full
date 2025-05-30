from typing import List
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import data_processor as dp
import numpy as np

linear_model = None


# Обучение модели линейной регрессии
def train_ln_model():
    global linear_model

    # Если данные ещё не загружены — загружаем
    if dp.FEATURES is None or dp.TARGET is None:
        dp.FEATURES, dp.TARGET = dp.load_dataframe('data\\MO_dataset.csv')

    # Разделение на train/test
    X_train, X_test, y_train, y_test = train_test_split(
        dp.FEATURES, dp.TARGET, test_size=0.2, random_state=47
        )

    # Обучаем модель линейной регрессии
    linear_model = LinearRegression()
    linear_model.fit(X_train, y_train)

    # Предсказания модели
    y_pred = linear_model.predict(X_test)

    # Оценка качества модели на тестовой выборке
    score_linear = linear_model.score(X_test, y_test)
    print(f"R² линейной регрессии: {score_linear:.2f}")
    mae = mean_absolute_error(y_test, y_pred)
    print(f"Средняя ошибка модели: {mae:.0f} руб.")
    print("Модель успешно обучена!")


'''
Эта функция предсказывает стоимость найма квартиры при помощи
модели линейной регрессии. Округляем с точностью до 1000 рублей.
'''
def predict_with_ln(vector) -> int:
    global linear_model

    if linear_model is None:
        raise ValueError("Модель линейной регрессии не обучена.")

    predicted_price = linear_model.predict(vector)
    #print(predicted_price)
    return int(np.round(predicted_price[0] // 1000) * 1000)
