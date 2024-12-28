from flask import request
from flask_restx import Namespace, Resource, fields
from app.models.building import Building
from app import db
from app.utils.auth import admin_required

ns_buildings = Namespace('buildings', description='Операції з будинками')

# Модель для Swagger-документації
building_model = ns_buildings.model('Building', {
    'name': fields.String(required=True, description='Назва будинку'),
    'address': fields.String(required=True, description='Адреса будинку'),
    'num_floors': fields.Integer(required=True, description='Кількість поверхів')
})

@ns_buildings.route('/')
class BuildingListResource(Resource):
    @ns_buildings.marshal_list_with(building_model)
    @admin_required
    def get(self):
        """Отримати список усіх будинків"""
        buildings = Building.query.all()
        return buildings

    @ns_buildings.expect(building_model)
    @admin_required
    def post(self):
        """Створити новий будинок"""
        data = request.json
        new_building = Building(
            name=data['name'],
            address=data['address'],
            num_floors=data['num_floors']
        )
        db.session.add(new_building)
        db.session.commit()
        return {"message": "Будинок створено"}, 201


@ns_buildings.route('/<int:building_id>')
@ns_buildings.param('building_id', 'Унікальний ідентифікатор будинку')
class BuildingResource(Resource):
    @ns_buildings.marshal_with(building_model)
    @admin_required
    def get(self, building_id):
        """Отримати дані конкретного будинку"""
        building = Building.query.get_or_404(building_id)
        return building

    @ns_buildings.expect(building_model)
    @admin_required
    def put(self, building_id):
        """Оновити дані будинку"""
        data = request.json
        building = Building.query.get_or_404(building_id)
        building.name = data.get('name', building.name)
        building.address = data.get('address', building.address)
        building.num_floors = data.get('num_floors', building.num_floors)
        db.session.commit()
        return {"message": "Дані будинку оновлено"}, 200

    @admin_required
    def delete(self, building_id):
        """Видалити будинок"""
        building = Building.query.get_or_404(building_id)
        db.session.delete(building)
        db.session.commit()
        return {"message": "Будинок видалено"}, 200
