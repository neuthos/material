import json
from urllib.request import Request, urlopen
from odoo.tests.common import HttpCase

BASE_ENPOINT = '/api/materials'
class TestMaterialController(HttpCase):

    def test_create_material(self):
        data = {
            'code': 'TEST001',
            'name': 'New Material',
            'type': 'cotton',
            'buy_price': 180,
            'supplier_id': 1
        }

        url = self.env['ir.config_parameter'].sudo().get_param('web.base.url') + BASE_ENPOINT
        req = Request(url=url, data=json.dumps(data).encode(), headers={'Content-Type': 'application/json'}, method='POST')
        response = urlopen(req)
        res = json.loads(response.read().decode('utf-8'))
        res = res['result']

        self.assertTrue(res['success'])
        self.assertEqual(res['message'], 'Material created successfully')

        created_material = self.env['material.material'].search([('code', '=', 'TEST001')])
        self.assertEqual(len(created_material), 1)
        self.assertEqual(created_material.name, 'New Material')
        self.assertEqual(created_material.type, 'cotton')
        self.assertEqual(created_material.buy_price, 180)
        self.assertEqual(created_material.supplier_id.id, 1)

    def test_get_materials(self):
        material1 = self.env['material.material'].create({
            'code': 'TEST001',
            'name': 'Material 1',
            'type': 'fabric',
            'buy_price': 150,
            'supplier_id': 1
        })
        material2 = self.env['material.material'].create({
            'code': 'TEST002',
            'name': 'Material 2',
            'type': 'jeans',
            'buy_price': 200,
            'supplier_id': 2
        })
        
        url = self.env['ir.config_parameter'].sudo().get_param('web.base.url') + BASE_ENPOINT + '?page=1&size=2'
        req = Request(url=url, method='GET')
        response = urlopen(req)
        res = json.loads(response.read().decode('utf-8'))
    
        self.assertTrue(res['success'])
        self.assertEqual(res['message'], 'data fetched')
        self.assertEqual(len(res['data']['rows']), 2)

    def test_update_material(self):
        material = self.env['material.material'].create({
            'code': 'CODE112',
            'name': 'Material Fabric',
            'type': 'fabric',
            'buy_price': 150,
            'supplier_id': 1
        })

        data = {
            'name': 'Material Jeans',
            'type': 'jeans',
            'buy_price': 200,
        }

        url = self.env['ir.config_parameter'].sudo().get_param('web.base.url') + BASE_ENPOINT + '/' + str(material.id)
        req = Request(url=url, data=json.dumps(data).encode(), headers={'Content-Type': 'application/json'}, method='PUT')
        response = urlopen(req)
        res = json.loads(response.read().decode('utf-8'))
        res = res['result']
        updated_material = res['data']

        self.assertTrue(res['success'])
        self.assertEqual(res['message'], 'Material updated successfully')


        self.assertEqual(updated_material['name'], 'Material Jeans')
        self.assertEqual(updated_material['type'], 'jeans')
        self.assertEqual(updated_material['buy_price'], 200)


    def test_delete_material(self):
        material = self.env['material.material'].create({
            'code': 'TEST001',
            'name': 'Material',
            'type': 'fabric',
            'buy_price': 150,
            'supplier_id': 1
        })

        url = self.env['ir.config_parameter'].sudo().get_param('web.base.url') + BASE_ENPOINT + '/' + str(material.id)
        req = Request(url=url, method='DELETE')
        response = urlopen(req)
        res = json.loads(response.read().decode('utf-8'))

        self.assertTrue(res['success'])
        self.assertEqual(res['message'], 'Material deleted successfully')

        deleted_material = self.env['material.material'].browse(material.id)
        self.assertFalse(deleted_material.exists())