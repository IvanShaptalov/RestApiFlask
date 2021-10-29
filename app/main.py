from app.models.db_util import db_control
from config import run_config
from app.models import db_util

app = run_config.app


@app.route('/')
def hello_world():  # put
    return 'Hello World!'


if __name__ == '__main__':
    db_util.create_all()
    app.run()
