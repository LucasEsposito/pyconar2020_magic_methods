import requests


base_url = "http://127.0.0.1:8080/api/v1"


class Number():

    def __init__(self, number):
        self.number = number

    def __add__(self, other):
        if isinstance(other, int):
            number_to_add = other
        elif isinstance(other, Number):
            number_to_add = other.number
        else:
            return NotImplemented

        data = {'data_a': self.number, 'data_b': number_to_add}
        r = requests.post(base_url + "/add", data=data)
        return Number(int(r.text))

    def __radd__(self, other):
        return self.__add__(other)

    def __repr__(self):
        return str(self.number)
