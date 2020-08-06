from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbhomework


## HTML 화면 보여주기
@app.route('/')
def homework():
    return render_template('index.html')


# 주문하기(POST) API
@app.route('/order', methods=['POST'])
def save_order():
    color = request.form['color_from_client']
    count = request.form['count_from_client']
    name = request.form['name_from_client']
    address = request.form['address_from_client']
    phone = request.form['phone_from_client']
    message = request.form['message_from_client']

    doc = {
        'color': color,
        'count': count,
        'name': name,
        'address': address,
        'phone': phone,
        'message': message
    }
    db.orderList.insert_one(doc)

    return jsonify({'result': 'success', 'msg': '연결되었습니다.!'})


# 주문 목록보기(Read) API
@app.route('/order', methods=['GET'])
def view_orders():
    orderLists = list(db.orderList.find({}, {'_id': False}))


    return jsonify({'result': 'success', 'orderList_from_server': orderLists})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
