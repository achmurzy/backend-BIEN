from decimal import Decimal
from flask import json

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if type(obj) is Decimal:
            return str(obj)
        else:
            # raises TypeError: obj not JSON serializable
            return json.JSONEncoder.default(self, obj)