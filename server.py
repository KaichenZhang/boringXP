import time
from flask import Flask, request
import json
import rfq_pb2
import rfp_pb2

app = Flask(__name__)

with open('priceData.json', 'r') as data_file:
    data = json.load(data_file)

request_log = []


# Handle the request with binary data
@app.route('/protobufbt', methods=['POST'])
def response_to_client_pb():
    timestamp = int(round(time.time() / 10000))
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

    rsp = rfp_pb2.ServerResponse()

    for item in data["priceList"]:
        if rcv.product_category == item["product_category"] and rcv.product_number == item["product_number"]:
            print("Requested product found")
            rsp.unit_price = item["unit_price"]
            rsp.price_validation_period = "valid from " + str(timestamp) + " to " + str(
                item["price_validation_period_span"] + timestamp)
            print(rsp)
            # serialization
            return rsp.SerializeToString()

    # if no such item in the database
    rsp.unit_price = 0
    rsp.price_validation_period = ""

    return rsp.SerializeToString()


# Handle the request with JSON text based data
@app.route('/jsonstr', methods=['POST'])
def response_to_client_json():
    timestamp = int(round(time.time() / 10000))
    # deserialization
    rcv = json.loads(request.data)

    record = {
        'rfq_id': rcv["rfq_id"],
        'account_id': rcv["account_id"],
        'product_number': rcv["product_number"],
        'product_category': rcv["product_category"],
        'quantity': rcv["quantity"]
    }

    request_log.append(record)
    rsp = {}
    for item in data["priceList"]:
        if rcv["product_category"] == item["product_category"] and rcv["product_number"] == item["product_number"]:
            print("Requested product found")
            i = item["unit_price"]
            j = "valid from " + str(timestamp) + " to " + str(item["price_validation_period_span"] + timestamp)
            rsp = {"unit_price": i, "price_validation_period": j}
            print(rsp)
            # serialization
            return json.dumps(rsp)

    # if no such item in the database
    return json.dumps(rsp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, threaded=True)
    # app.run(debug=True, port=5005)
