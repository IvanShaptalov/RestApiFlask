from flask import request

import config
from app.api.products import bp
from app.filters import product_filtering
from app.models import Product, db_util
from app.models.shema import ProductSchema, ProductQueryArgsSchema
from flask.views import MethodView


from app.utils import resp_shortcut


@bp.get('')
class Products(MethodView):
    @bp.arguments(ProductQueryArgsSchema, location='json')
    @bp.response(ProductSchema(many=True))
    @bp.paginate(max_page_size=config.validation_config.MAX_PAGE_SIZE)
    def get(self, args, pagination_parameters):
        """Product list using pagination, filtering and sorting"""
        pagination_parameters.item_count = db_util.get_count(session=db_util.sc_session,
                                                             table_class=Product)

        sorting_rule = product_filtering.get_sorting_rule(request)
        filtering_rule = product_filtering.get_filtering_rule(request)

        products = product_filtering.get_products(sorting_rule=sorting_rule, filtering_rule=filtering_rule)
        result_prod = products[pagination_parameters.first_item: pagination_parameters.last_item + 1]
        if result_prod:
            return result_prod
        return resp_shortcut(message='Not found', desc='items not found', code=200)
