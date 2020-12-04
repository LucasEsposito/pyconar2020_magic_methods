from gevent import monkey
monkey.patch_all()

from bottle import response, route, run, request
import logging
import gevent
import argparse


@route('/api/v1/test', method='GET')
def test():
    return "OK"


@route('/api/v1/add', method='POST')
def add():
    data_a = request.forms.get('data_a', type=int)
    data_b = request.forms.get('data_b', type=int)
    res = data_a + data_b
    print("Adding %s + %s" % (data_a, data_b))

    return str(res)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', help='Host to bind the API server on',
                        default='localhost', action='store', required=False)
    parser.add_argument('-p', '--port', help='Port to bind the API server on',
                        default=8080, action='store', required=False)
    args = parser.parse_args()
    args.port = int(args.port)
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    logging.info(args)
    run(host=args.host, port=args.port, server='gevent')

