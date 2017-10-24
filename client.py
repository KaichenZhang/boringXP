from flask import Flask, render_template, request
import requests
import rfq_pb2

app = Flask(__name__)

url_post = 'http://localhost:5005/post'
url_get = 'http://localhost:5005/get'

response=[]


# Index
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        # Get Form Fields
        rfq_id = int(request.form['rfq_id'])
        account_id = int(request.form['account_id'])
        product_number = int(request.form['product_number'])
        product_category = request.form['product_category']
        quantity = int(request.form['quantity'])

        send_request = rfq_pb2.ClientRequest()
        send_request.rfq_id = rfq_id
        send_request.account_id = account_id
        send_request.product_number = product_number
        send_request.product_category = product_category
        send_request.quantity = quantity
        # serialization
        request_str = send_request.SerializeToString()
        response.append(requests.post(url_post, data=request_str))
        # return redirect(url_for('post_request'))

    if request.method == 'GET'and request.args == "log":
        return "asd"

    return render_template('clientPage.html', response = response)




# send_request = rfq_pb2.ClientRequest()
# send_request.rfq_id=1234
# send_request.account_id=1
# send_request.product_number=5
# send_request.product_category="E"
# send_request.quantity=100

# serialization
# request_str = send_request.SerializeToString()
# print(request_str)



# get the response from server which is in JSON format
# response = requests.post(url_post, data=request_str)
# requests.post(url_post, data=request_str)
# requests.post(url_post, data=request_str)
# requests.post(url_post, data=request_str)
# requests.post(url_post, data=request_str)
# requests.post(url_post, data=request_str)

# get_server = requests.get(url_get)


# print(response.text)
# print('GET LOG FILE:')
# print(get_server.text)

if __name__ == '__main__':

    app.run(debug=True, host='127.0.0.1', port = 5000)