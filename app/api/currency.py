from app.models.db_util import User, Product, sc_session
from app.security.token_provider import token_required
from config.run_config import app
from flask import request, make_response
from app.filters import filter


@app.route("/add_currency/<int:product_id>", methods=['POST', 'GET'])
@token_required
@filter.data_exists(['article', 'name'])
def create_currency(current_user: User, product_id):
    pass
    # todonext create adding currency to product