# save this as app.py
from flask import Flask, request

app = Flask(__name__)

@app.route("/webhooks", methods=['GET', 'POST'])
def webhooks():
    req = request.get_json(silent=True, force=True)
    print(req)
    queryResult = req['queryResult']
    print(queryResult)
    action = queryResult['action']
    print(action)
    parameters = queryResult['parameters']
    return {
        "fulfillmentText": getResponseForAction(action, parameters)
    }

def getResponseForAction(action, parameters):
    return "yep for sure!!!"