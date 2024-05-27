# -*- coding: utf-8 -*-
import json
import logging
from odoo import http
from odoo.http import Response, request, JsonRequest
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

DEFAUL_ENDPOINT = '/api/materials'

class MaterialController(http.Controller):

    def _err_exception(self, e, code=500, message=None):
        json_headers = {'Content-Type': 'application/json'}
        if isinstance(e, ValidationError):
            return Response(json.dumps({'success': False, 'code': 400, 'message': e.name or "Validation error occurred."}), status=400, headers=json_headers)
        else:
            return Response(json.dumps({'success': False, 'code': code or 500, 'message': message or str(e) or "An error occurred."}), status=code or 500, headers=json_headers)

    def _err_exception_json(self, e, code=500, message=None):
        if isinstance(e, ValidationError):
            return {'success': False, 'code': 400, 'message': e.name or "Validation error occurred."}
        else:
            return {'success': False, 'code': code or 500, 'message': message or str(e) or "An error occurred."}


    def _res_handler(self, data: any, message = None):
        json_headers = { 'Content-Type': 'application/json' }
        output = { 'success': True, 'message': message or 'Success', 'data': data }
        return Response(json.dumps(output), headers=json_headers)
    
    def _res_handler_json(self, data: any, message = None):
        output = { 'success': True, 'message': message or 'Success', 'data': data }
        return output

    @http.route(DEFAUL_ENDPOINT, auth='public', type='http', methods=['GET'])
    def list(self, material_type=None, name=None, code=None, order_by=None, page=1, size=10):
        try:

            domain = []
    
            if page:
                page  = int(page) or 1
            if size:
                size  = int(size) or 10
            if material_type:
                domain.append(('type', '=', material_type))
            if name:
                domain.append(('name', 'ilike', '%' + name + '%'))
            if code:
                domain.append(('code', '=', code))
            if order_by:
                order_by = ' '.join(request.params.get('order_by').split(','))

            materials = request.env['material.material'].sudo().search(domain, order=order_by)
            
            total_count = len(materials)
            total_pages = (total_count + size - 1) // size
            offset = (page - 1) * size
            limited_materials = materials[offset:offset + size]

            results = []

            for m in limited_materials:
                output = {
                    'id': m.id,
                    'code': m.code,
                    'name': m.name,
                    'type': m.type,
                    'buy_price': m.buy_price,
                    'supplier_id': m.supplier_id.id,
                    'supplier': {
                        'id': m.supplier_id.id,
                        'name': m.supplier_id.name,
                        'email': m.supplier_id.email,
                        'phone': m.supplier_id.phone,
                    }
                }
                results.append(output)

            pagination_data = {
                'page': page,
                'size': size,
                'total_rows': total_count,
                'total_pages': total_pages,
            }

            return self._res_handler({'rows': results, 'pagination': pagination_data}, 'data fetched')
        except Exception as e:
            return self._err_exception(e)

    @http.route('/api/partners', auth='public', type='http', methods=['GET'])
    def get_partners(self):
        try:
            partners = request.env['res.partner'].sudo().search([], order='name')
            results = []
            for p in partners:
                output = {
                    'id': p.id,
                    'name': p.name,
                    'display_name': p.display_name,
                    'phone': p.phone,
                    'email': p.email,
                }
                results.append(output)
            
            return self._res_handler(results, 'data fetched')
        except Exception as e:
            return self._err_exception(e)
    
    @http.route(DEFAUL_ENDPOINT + '/type', auth='public', type='http', methods=['GET'])
    def get_material_type(self):
        try:
            results = [
                { 'value': 'fabric', 'label': 'Fabric' },
                { 'value': 'jeans', 'label': 'Jeans' },
                { 'value': 'cotton', 'label': 'Cotton' }
            ]
            
            return self._res_handler(results, 'data fetched')
        except Exception as e:
            return self._err_exception(e)

    @http.route(DEFAUL_ENDPOINT, auth='public', type='json', methods=['POST'], csrf=False)
    def create(self):
        try:
            data = json.loads(request.httprequest.data)
            
            code = data.get('code')
            name = data.get('name')
            material_type = data.get('type')
            buy_price = float(data.get('buy_price'))
            supplier_id = int(data.get('supplier_id'))
            
            new_material = request.env['material.material'].sudo().create({
                'code': code,
                'name': name,
                'type': material_type,
                'buy_price': buy_price,
                'supplier_id': supplier_id
            })

            output = {
                'id': new_material.id,
                'code': new_material.code,
                'name': new_material.name,
                'type': new_material.type,
                'buy_price': new_material.buy_price,
                'supplier_id': new_material.supplier_id.id,
                'supplier_name': new_material.supplier_id.name,
            }

            return self._res_handler_json(output, 'Material created successfully')
        except ValidationError as e:
            return self._err_exception_json(e, 400, str(e))
        except Exception as e:
            return self._err_exception_json(e);

    @http.route(DEFAUL_ENDPOINT + '/<int:material_id>', auth='public', type='json', methods=['PUT'])
    def update(self, material_id):
        try:
            data = request.jsonrequest
            material = request.env['material.material'].sudo().browse(material_id)
            print(material.name, 565656)
            if not material.exists():
                return self._err_exception_json(None, 404, 'Material not found')

            with request.env.cr.savepoint():
                material.write({
                    'code': data.get('code', material.code),
                    'name': data.get('name', material.name),
                    'type': data.get('type', material.type),
                    'buy_price': data.get('buy_price', material.buy_price),
                    'supplier_id': data.get('supplier_id', material.supplier_id.id)
                })
                updated_material = {
                    'id': material.id,
                    'code': material.code,
                    'name': material.name,
                    'type': material.type,
                    'buy_price': material.buy_price,
                    'supplier_id': material.supplier_id.id,
                }
                print(updated_material, 898989)
                return self._res_handler_json(updated_material, 'Material updated successfully')
        except ValidationError as e:
            request.env.cr.rollback()
            return self._err_exception_json(e, 400, str(e))
        except Exception as e:
            request.env.cr.rollback() 
            return self._err_exception_json(e)
        
    @http.route(DEFAUL_ENDPOINT + '/<int:material_id>', auth='public', type='http', methods=['DELETE'], csrf=False)
    def delete_material(self, material_id):
        try:
            material = request.env['material.material'].sudo().browse(material_id)

            if not material.exists():
                return self._err_exception(None, 404, 'Material not found')

            with request.env.cr.savepoint():
                material.unlink()
                return self._res_handler(None, 'Material deleted successfully')
        except Exception as e:
            request.env.cr.rollback()
            return self._err_exception(e)
