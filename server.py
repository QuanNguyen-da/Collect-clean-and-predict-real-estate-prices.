from flask import Flask, request, jsonify
import util

# Khởi tạo Flask app
app = Flask(__name__)


# API để dự đoán giá nhà
@app.route('/get_predict_price', methods=['GET'])
def predict_home_price():
    try:
        area = float(request.args.get('Area'))
        bathroom = float(request.args.get('Bathroom'))
        bedroom = float(request.args.get('Bedroom'))
        province = str(request.args.get('Province'))

        response = jsonify({
            'Predict': util.get_predict_price(area, bathroom, bedroom, province)
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        return jsonify({'error': str(e)})

# Chạy server Flask
if __name__ == "__main__":
    print("Starting Python Flask Server For Prediction...")
    util.load_save_predict()
    app.run()
