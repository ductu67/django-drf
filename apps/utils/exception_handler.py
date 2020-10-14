from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

import apps.utils.response_interface as rsp


# from apps.utils.base.error_code import ErrorCode, ErrorLevel
# todo: improve this handler
# from apps.utils.base.exception import CustomException


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    exception_class = exc.__class__.__name__
    if response:
        if exception_class == 'ParseError':
            message = 'JSON parse error'
        elif exception_class == "ValidationError":
            try:
                list_errors = list(exc.detail.items())
                data_error = []
                for error in list_errors:
                    data_error.append("{} : {}".format(error[0], error[1][0]))
                    message = ', '.join(data_error)
            except Exception:
                message = 'Invalid ' + list(list(exc.detail.items())[0][1][0].items())[0][0]
        else:
            message = exc.detail
        try:
            status_code = exc.status_code
        except Exception:
            status_code = status.HTTP_400_BAD_REQUEST
    else:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        message = exc.args[0]

    general_response = rsp.Response(False, message=message, data=None).generate_response()
    response = Response(data=general_response, status=status_code)
    return response
