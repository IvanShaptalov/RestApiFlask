from marshmallow import Schema, fields


class PriceSchema(Schema):
    currency = fields.String()
    count = fields.Integer()
    product_id = fields.Integer()


class ProductSchema(Schema):
    name = fields.String()
    article = fields.String()
    pricelist = fields.List(fields.Nested(PriceSchema))


class ProductQueryArgsSchema(Schema):
    name = fields.String()
