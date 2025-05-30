from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import linear_model as lm
import data_processor as dp
import numpy as np

logistic_model = None
FEATURES_LG = None
TARGET_LG = None


# Обучение модели логистической регрессии
def train_lg_model():
    global logistic_model, FEATURES_LG, TARGET_LG

    # Если данные ещё не загружены — загружаем
    if dp.FEATURES is None or dp.TARGET is None:
        dp.FEATURES, dp.TARGET = dp.load_dataframe('data\\MO_dataset.csv')

    # Если модель линейной регрессии ещё необучена - обучаем её
    if lm.linear_model is None:
        from linear_model import train_ln_model
        train_ln_model()
    
    # Получаем предсказания линейной модели
    y_pred_ln = lm.linear_model.predict(dp.FEATURES)

    # Добавляем реальную цену как признак
    FEATURES_LG = dp.FEATURES.copy()
    FEATURES_LG['original_price'] = dp.TARGET.values  # добавляем цену как признак

    # Формируем бинарную целевую переменную: 1 — цена выше на >= 20%
    threshold = 1.1
    target_binary = (dp.TARGET > threshold * y_pred_ln).astype(int)

    # Разделение на train/test
    X_train, X_test, y_train, y_test = train_test_split(
        FEATURES_LG, target_binary, test_size=0.2, random_state=47
    )

    # Обучаем модель логистической регрессии
    logistic_model = LogisticRegression()
    logistic_model.fit(X_train, y_train)

    # Оценка качества модели на тестовой выборке
    y_pred = logistic_model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Accuracy логистической регрессии: {acc:.2f}")
    print("Модель успешно обучена!")


'''
Модель предсказывает, является ли цена за квартиру выше ожидаемой или нет?
'''
def predict_with_lg(vector, original_price):
    global logistic_model
    
    if logistic_model is None:
        raise ValueError("Модель логистической регрессии не обучена.")

    
    residual = original_price - lm.linear_model.predict(vector)[0][0]
    # Добавляем original_price как признак
    vector_with_price = vector.copy()
    vector_with_price['original_price'] = original_price

    prediction = logistic_model.predict(vector_with_price)[0]
    probability = logistic_model.predict_proba(vector_with_price)[0][1]

    if prediction:
        print(f"Цена выше ожидаемой на {residual:.0f}₽ (вероятность завышения: {probability:.2f})")
    else:
        print(f"Цена в пределах нормы (вероятность завышения: {probability:.2f})")

    if prediction:
        return f"Цена выше ожидаемой на {residual:.0f}₽ (вероятность завышения: {probability:.2f})"
    else:
        return f"Цена в пределах нормы (вероятность завышения: {probability:.2f})"
