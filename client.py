from random import randint, randrange
import time
import requests
import rfq_pb2
import rfp_pb2
import json

# url_pb_post = 'http://ec2-18-221-227-182.us-east-2.compute.amazonaws.com:5005/protobufbt'
# url_json_post = 'http://ec2-18-221-227-182.us-east-2.compute.amazonaws.com:5005/jsonstr'

# url_pb_post = 'http://localhost:5005/protobufbt'
# url_json_post = 'http://localhost:5005/jsonstr'


# protocol buffer data communication
def post_pb_bytes():
    # Create Fields
    rfq_id = int(round(time.time() / 10000))
    account_id = randint(1, 9)
    product_number = randint(1, 9)
    # random letter from A to I
    product_category = str(chr(randrange(65, 74)))
    quantity = randint(1, 9) * randint(1, 100)

    send_request = rfq_pb2.ClientRequest()
    send_request.rfq_id = rfq_id
    send_request.account_id = account_id
    send_request.product_number = product_number
    send_request.product_category = product_category
    send_request.quantity = quantity
    # serialization
    request_bt = send_request.SerializeToString()
    response = requests.post(url_pb_post, data=request_bt)
    print("")
    print("The Request with content:")
    print(send_request)
    print("of type " + str(type(send_request)))
    print("is sent as:")
    print(request_bt)
    print("of type " + str(type(request_bt)))
    # deserialization
    rsp = rfp_pb2.ServerResponse()
    rsp.ParseFromString(response.content)
    print("")
    print("Response is received as:")
    print(response.content)
    print("of type " + str(type(response.content)))
    print("")
    print("and is deserialized to:")
    print(rsp)
    print("of type " + str(type(rsp)))
    print("")
    print("")


# JSON text based data communication
def post_json_str():
    # Create Fields
    rfq_id = int(round(time.time() / 10000))
    account_id = randint(1, 9)
    product_number = randint(1, 9)
    # random letter from A to I
    product_category = str(chr(randrange(65, 74)))
    quantity = randint(1, 9) * randint(1, 100)

    send_request = {"rfq_id": rfq_id,
                    "account_id": account_id,
                    "product_number": product_number,
                    "product_category": product_category,
                    "quantity": quantity}

    # serialization
    request_str = json.dumps(send_request)
    response = requests.post(url_json_post, data=request_str)
    print("")
    print("The Request with content:")
    print(send_request)
    print("of type " + str(type(send_request)))
    print("is sent as:")
    print(request_str)
    print("of type " + str(type(request_str)))
    print("")
    # deserialization
    rsp = json.loads(response.text)
    print("Response is received as:")
    print(response.text)
    print("")
    print("of type " + str(type(response.text)))
    print("and is deserialized to")
    print(rsp)
    print("of type " + str(type(rsp)))
    print("")
    print("")


while True:
    print("1. Make a request with Protocol Buffer serialization")
    print("2. Make a request with JSON text based serialization")
    print("0. Exit")
    choice = int(input("Please enter your choice: "))
    if choice == 1:
        post_pb_bytes()
    elif choice == 2:
        post_json_str()
    elif choice == 0:
        print("----Client Terminated----")
        exit(0)
    else:
        print("Please enter 1 or 2")
        continue
