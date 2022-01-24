from functools import reduce, wraps

from flask import abort, g, request


def require_json_body(query_params: list):
    def real_decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            # Must check the raw request body instead of get_json()
            #   Using get_json on empty request body triggers automatically the
            #   error_controller.bad_request_error (400) handler
            d = request.get_data()
            if not d:
                abort(400, {'message': 'The request body is required'})

            body = request.get_json()
            missing_params = [k for k in query_params if k not in body.keys()]
            if len(missing_params) == 1:
                abort(400, {'message': 'The {} is missing'.format(missing_params[0])})

            if len(missing_params) > 1:
                reduced_params = reduce('{}, {}'.format, missing_params)
                abort(400, {'message': 'The {} are missing'.format(reduced_params)})

            return function(*args, **kwargs)
        return wrapper
    return real_decorator


def require_query_params(query_params: list):
    def real_decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            missing_params = [k for k in query_params if k not in request.args.keys()]
            if len(missing_params) == 1:
                abort(400, {'message': 'The {} is missing'.format(missing_params[0])})

            if len(missing_params) > 1:
                reduced_params = reduce('{}, {}'.format, missing_params)
                abort(400, {'message': 'The {} are missing'.format(reduced_params)})

            return function(*args, **kwargs)
        return wrapper
    return real_decorator
