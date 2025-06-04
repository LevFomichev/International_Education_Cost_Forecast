from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)
model = joblib.load('model_service/model_pipeline.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    # Гарантированная проверка данных
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    input_data = request.get_json()
    
    # Жесткая проверка полей
    required_fields = ['Country', 'City', 'University', 'Program', 'Level']
    missing = [field for field in required_fields if field not in input_data]
    if missing:
        return jsonify({'error': f'Missing fields: {missing}'}), 400
    
    # Гарантированное преобразование в float
    try:
        df = pd.DataFrame([input_data])
        prediction = float(model.predict(df)[0])
        return jsonify({'prediction': prediction})
    except Exception as e:
        return jsonify({'error': 'Prediction failed'}), 500  # Упрощенное сообщение об ошибке

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)