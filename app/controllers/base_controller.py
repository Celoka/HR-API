from flask import jsonify, make_response


class BaseController:

    def __init__(self, request):
        self.request = request


    def request_params(self, *keys):
        json = self.request.get_json()
        if keys:
            values = list()
            for key in keys:
                values.append(json[key]) if key in json else values.append(None)
            return values
        return json


    def get_json(self):
        return self.request.get_json()

    def handle_response(self, msg="OK", payload=None, status_code=200):
        data = {'msg': msg}
        if payload is not None:
            data['payload'] = payload
        response = jsonify(data)
        response.status_code = status_code
        return response
