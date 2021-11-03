from flask import request

import config
from app.api.products import bp
from app.models import Product, db_util
from app.models.shema import ProductSchema, ProductQueryArgsSchema
from flask.views import MethodView


# todonow sorting
@bp.get('')
class Products(MethodView):
    @bp.arguments(ProductQueryArgsSchema, location='json')
    @bp.response(ProductSchema(many=True))
    @bp.paginate(max_page_size=config.validation_config.MAX_PAGE_SIZE)
    def get(self, args, pagination_parameters):
        """Product list"""
        page = request.args.get('page', 1, type=int)
        pagination_parameters.item_count = db_util.get_count(session=db_util.sc_session,
                                                             table_class=Product)

        products = db_util.get_from_db_multiple_filter(open_session=db_util.sc_session,
                                                       table_class=Product,
                                                       all_objects=True)
        result_prod = products[pagination_parameters.first_item: pagination_parameters.last_item + 1]
        return result_prod
