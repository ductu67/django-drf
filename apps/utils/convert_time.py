from datetime import datetime

from rest_framework.exceptions import ParseError


def convert_string_to_date(string):
    try:
        return datetime.strptime(string, '%m-%Y')
    except:
        try:
            return datetime.strptime(string, '%m/%Y')
        except:
            raise Exception("wrong in format datetime!")
