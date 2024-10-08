from flask_restx import Resource
from flask_jwt_extended import jwt_required, current_user

from src.models import User, Role
from src.api.nsmodels import users_ns, roles_model

@users_ns.route('/roles')
@users_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Forbidden', 404: 'Not Found'})
class RolesListApi(Resource):
    @jwt_required()
    @users_ns.doc(security='JsonWebToken')
    @users_ns.marshal_with(roles_model)
    def get(self):
        # Check if the user has permission
        if not current_user.check_permission('can_users'):
            return {"error": "არ გაქვს მომხმარებლის ნახვის ნებართვა."}, 403
        
        # Fetch all roles from the database
        roles = Role.query.all()
        
        if not roles:
            return {'error': 'როლი ვერ მოიძებნა.'}, 404
        
        return roles, 200