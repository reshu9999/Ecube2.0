import json


class AetosResponseBase(object):

    RESPONSE = None

    ALLOWED_STATUS_CODE_MAP = {
        'success': [200],
        'failure': [500, 404]
    }

    @classmethod
    def _api_response(cls, success, data, message, status, mimetype=None):
        response = {
            'success': bool(success),
            'message': message,
            'data': data
        }
        # try:
        #     response = json.dumps(response)
        # except TypeError as e:
        #     response = json.dumps({
        #         'success': False,
        #         'message': 'ERROR: %s' % e
        #     })
        #     status = 500
        return cls.RESPONSE(data=response, status=status)

    @classmethod
    def success_api_response(cls, data, message=None, mimetype=None):
        return cls._api_response(True, data, message or 'Success', 200)

    @classmethod
    def failure_api_response(cls, data, message=None, mimetype=None):
        return cls._api_response(False, data, message or 'Failure', 500)

    @classmethod
    def not_found_api_response(cls, message=None, mimetype=None):
        return cls._api_response(None, dict(), message or 'Not Found', 404)
