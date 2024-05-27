# tests/test_material.py
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestMaterial(TransactionCase):

    def setUp(self):
        super(TestMaterial, self).setUp()
        self.Material = self.env['material.material']
        self.partner = self.env['res.partner'].create({
            'name': 'Test Supplier'
        })

    def create_material(self, code = 'MAT1'):
        return self.Material.create({
            'code': code,
            'name': 'Test Material',
            'type': 'fabric',
            'buy_price': 150.0,
            'supplier_id': self.partner.id
        })

    def test_create_material(self):
        material = self.create_material('MAT1')
        self.assertEqual(material.code, 'MAT1')
        self.assertEqual(material.name, 'Test Material')
        self.assertEqual(material.type, 'fabric')
        self.assertEqual(material.buy_price, 150.0)
        self.assertEqual(material.supplier_id.id, self.partner.id)

    def test_read_material(self):
        material = self.create_material('MAT2')
        read_material = self.Material.browse(material.id)
        self.assertEqual(read_material.code, 'MAT2')
        self.assertEqual(read_material.name, 'Test Material')
        self.assertEqual(read_material.type, 'fabric')
        self.assertEqual(read_material.buy_price, 150.0)
        self.assertEqual(read_material.supplier_id.id, self.partner.id)

    def test_update_material(self):
        material = self.create_material('MAT3')
        material.write({
            'name': 'Updated Material',
            'buy_price': 200.0
        })
        self.assertEqual(material.name, 'Updated Material')
        self.assertEqual(material.buy_price, 200.0)

    def test_delete_material(self):
        material = self.create_material('MAT4')
        material_id = material.id
        material.unlink()
        read_material = self.Material.search([('id', '=', material_id)])
        self.assertFalse(read_material)

    def test_buy_price_validation(self):
        with self.assertRaises(ValidationError):
            self.Material.create({
                'code': 'MAT5',
                'name': 'Invalid Material',
                'type': 'jeans',
                'buy_price': 50.0,
                'supplier_id': self.partner.id
            })