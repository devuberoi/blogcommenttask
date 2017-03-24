from flask import jsonify
from time import time
# helper function for json response
def respond(response):
    http_status = response.pop('http_status', 200)
    response['status'] = 'success'
    if http_status not in [200, 201]:
        response['status'] = 'failed'
    return jsonify(response), http_status

get_timestamp = lambda: int(time() * 1000)
