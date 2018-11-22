# -*- encoding: utf-8 -*-
# __author__ = JasonWu(jaronemo@msn.com)
from odoo import api, models


class ProductOrderPoint(models.Model):
    _inherit = 'product.product'

    @api.multi
    def create_ordering_rule(self, min_qty=0.0, max_qty=0.0, qty_multiple=1.0):
        self.ensure_one()
        op_obj = self.env['stock.warehouse.orderpoint']

        for p in self:
            op_rules = op_obj.search([('product_id', '=', p.id)])
            op_vals = {
                'product_id': p.id,
                'product_min_qty': min_qty,
                'product_max_qty': max_qty,
                'qty_multiple': qty_multiple,
                'active': True,
                'product_uom': p.uom_id.id,
            }

            if p.type in ('product', 'consu') and not op_rules:
                self.env['stock.warehouse.orderpoint'].create(op_vals)

    @api.model
    def create(self, vals):
        res = super(ProductOrderPoint, self).create(vals)

        if res:
            res.create_ordering_rule()

            return res
