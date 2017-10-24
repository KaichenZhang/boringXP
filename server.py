from flask import Flask, request
from flask_restful import Resource, Api
from flask_jsonpify import jsonify
import json
import rfq_pb2

app = Flask(__name__)
api = Api(app)

with open('priceData.json', 'r') as data_file:
    data = json.load(data_file)

request_log = []


class GetLog(Resource):
    def get(self):
        with open('log.json', 'w') as log_file:
            json.dump({'records': request_log}, log_file, indent=5)
        with open('log.json') as data_file:
            log_data = json.load(data_file)
        return jsonify(log_data)


class HandleRequests(Resource):
    def post(self):
        rcv = rfq_pb2.ClientRequest()
        # deserialization
        rcv.ParseFromString(request.data)

        record = {
            'rfq_id': rcv.rfq_id,
            'account_id': rcv.account_id,
            'product_number': rcv.product_number,
            'product_category': rcv.product_category,
            'quantity': rcv.quantity
        }

        request_log.append(record)

        for item in data["priceList"]:
            if rcv.product_number == item["product_number"]:
                print("Requested product found")
                return jsonify(unit_price=item["unit_price"],
                               price_validation_period=item["price_validation_period"])

        return jsonify(notification="no_such_item")


api.add_resource(GetLog, '/get') # Route_1
api.add_resource(HandleRequests, '/post') # Route_2

if __name__ == '__main__':
    app.run(host='127.0.0.1', port = 5005)
