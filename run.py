import logging

from app import api
import sys
sys.stdout = open('debug.log', 'w')

app = api.create_app()

if __name__ == '__main__':
    try:
        logging.info('Useful message')
        logging.error('Something bad happened')
        app.run()
    except Exception as e:
        print(e, type(e))
        sys.stdout.close()