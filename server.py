import time
from flask import Flask, request
import json
import rfq_pb2
import rfp_pb2
from rfpmod import Rfp
from rfqmod import Rfq

app = Flask(__name__)

with open('priceData.json', 'r') as data_file:
    data = json.load(data_file)


# Handle the request with binary data
@app.route('/protobufbt', methods=['POST'])
def response_to_client_pb():
    timestamp = int(round(time.time() / 10000))
    rcv = rfq_pb2.ClientRequest()
    # deserialization
    rcv.ParseFromString(request.data)

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

    # serialization
    return rsp.SerializeToString()


# Handle the request with JSON text based data
@app.route('/jsonstr', methods=['POST'])
def response_to_client_json():
    timestamp = int(round(time.time() / 10000))
    # deserialization
    rcv = json.loads(request.data)
    # create client request instance
    client_request = Rfq(rcv["rfq_id"], rcv["account_id"], rcv["product_number"], rcv["product_category"],
                         rcv["quantity"])

    for item in data["priceList"]:
        if client_request.product_category == item["product_category"] and \
                        client_request.product_number == item["product_number"]:
            print("Requested product found")
            # create response instance
            send_response = Rfp(item["unit_price"], "valid from " + str(timestamp) + " to " + str(
                item["price_validation_period_span"] + timestamp))
            # serialization
            # convert object instance send_response to dictionary
            return json.dumps(send_response.__dict__)

    # if no such item in the database
    send_response = Rfp(0, "")

    # serialization
    return json.dumps(send_response.__dict__)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, threaded=True)
