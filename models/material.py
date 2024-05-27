# models/material.py
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Material(models.Model):
    _name = 'material.material'
    _description = 'Material'

    code = fields.Char(string='Material Code', required=True)
    name = fields.Char(string='Material Name', required=True)
    type = fields.Selection([
        ('fabric', 'Fabric'),
        ('jeans', 'Jeans'),
        ('cotton', 'Cotton')
    ], string='Material Type', required=True)
    buy_price = fields.Float(string='Material Buy Price', required=True)
    supplier_id = fields.Many2one('res.partner', string='Related Supplier', required=True)

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'Material code must be unique!')
    ]

    @api.model
    def create(self, vals):
        if vals.get('buy_price') and vals['buy_price'] < 100:
            raise ValidationError('buy price cannot be less than 100')
        return super(Material, self).create(vals)

    def write(self, vals):
        if vals.get('buy_price') and vals['buy_price'] < 100:
            raise ValidationError('buy price cannot be less than 100')
        return super(Material, self).write(vals)
