from flask import Flask, request, jsonify, session, render_template
from data_processor import FEATURES, data_to_vector
from linear_model import predict_with_ln, train_ln_model
from logistic_model import predict_with_lg

import data_processor as dp

app = Flask(__name__)
app.secret_key = '<secret>'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        data = request.get_json()

        session['form_data'] = data

        # Выбранная модель (0 - линейная или 1 - логистическая)
        ml_model = data.pop('ml_model', None)

        vector = data_to_vector(data)

        if 'error' in vector:
            if vector['error'] == 'address_not_found':
                return jsonify({
                    'status': 'naa',
                    'message': 'Адрес не найден'
                })

        predicted_price = -1

        if ml_model == '0':
            predicted_price = predict_with_ln(vector)
        elif ml_model == '1':
            predicted_price = predict_with_lg(vector)



        return jsonify({
            'status': 'success',
            'predicted_price': predicted_price
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


if __name__ == '__main__':
    # Обрабатываем и загружаем датасет
    # dp.FEATURES, dp.TARGET = dp.load_dataframe('MO_dataset.csv')

    dp.FEATURES = dp.pd.read_csv('data\\features_cleared.csv', sep=',')
    print(dp.FEATURES["distance"].head())
    dp.TARGET = dp.pd.read_csv('data\\targets_cleared.csv', sep=',')
    print(dp.TARGET.head())
    # обучение моделей
    train_ln_model()

    # Запускаем основное приложение
    app.run(debug=True)
