import config.validation_config
from app.models import db_util, Product


def get_sorting_rule(request):
    """check that given sorting parameter is allowed by application"""
    if 'sort_by' in request.args:
        sort_by = request.args.get('sort_by') or None
        if sort_by in config.validation_config.ALLOWED_SORTING_FIELDS:
            return dict(sort_by=sort_by)
    return None


def get_filtering_rule(request):
    """
    filter rule to filtering data via name or article
    """

    filter_by_name = request.args.get('name') or None
    filter_by_article = request.args.get('article') or None
    filter_rule = dict()
    if filter_by_name:
        filter_rule['name'] = filter_by_name
    if filter_by_article and len(filter_by_article):
        filter_rule['article'] = filter_by_article
    return None if len(filter_rule) == 0 else filter_rule


def get_products(sorting_rule: dict = None, filtering_rule: dict = None):
    """
    get products using rules
    :param sorting_rule: via sorting rule
    :param filtering_rule: via filtering rule
    :return: filtered and sorted products, if required
    """
    products = None
    conditions = []
    if filtering_rule is None:
        # pass rules and return all products
        products = db_util.get_from_db_multiple_filter(open_session=db_util.sc_session,
                                                       table_class=Product,
                                                       all_objects=True)
    else:
        # filter products
        if filtering_rule:
            name = filtering_rule.get('name') or None
            article = filtering_rule.get('article') or None
            if name:
                # noinspection PyUnresolvedReferences
                conditions.append(Product.name.contains(name))
            if article:
                conditions.append(Product.article == article)

            products = db_util.get_from_db_multiple_filter(open_session=db_util.sc_session,
                                                           table_class=Product,
                                                           identifier_to_value=conditions,
                                                           get_type='many')
    if sorting_rule:
        if sorting_rule['sort_by'] == 'name':
            print('sort by name')
            products = sorted(products, key=lambda prod: prod.name)
        elif sorting_rule['sort_by'] == 'article':
            products = sorted(products, key=lambda prod: prod.article)
            print('sort by article')

        # sort products by name or article
    return products
