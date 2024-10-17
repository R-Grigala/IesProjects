from flask_restx import reqparse, fields, inputs
from src.extensions import api


accounts_ns = api.namespace('Accounts', description='API endpoint for Role Management', path='/api')

user_model = accounts_ns.model('User', {
    'uuid': fields.String(required=True, type=str, description='The unique UUID of the user'),
    'name': fields.String(required=True, type=str, description='The name of the user'),
    'lastname': fields.String(required=True,  type=str, description='The lastname of the user'),
    'email': fields.String(required=True, type=inputs.email(check=True), description='The email of the user'),
    'role_name': fields.String(required=True, type=str, description='The role ID associated with the user')
})

# auth parser
user_parser = reqparse.RequestParser()

user_parser.add_argument('name', required=True, type=str, help='Name example: Roma (1-20 characters)')
user_parser.add_argument('lastname', required=True, type=str, help='LastName example: Grigalashvili (1-20 characters)')
user_parser.add_argument("old_password", required=False, type=str, help="Old password example: Grigalash1")
user_parser.add_argument("new_password", required=False, type=str, help="New Password example: Grigalash27")
user_parser.add_argument("repeat_new_password", required=False, type=str, help="Repeat new Password example: Grigalash27")
user_parser.add_argument("change_password", required=True, type=inputs.boolean, help="Password example: true")
user_parser.add_argument('role_name', required=True, type=str, help='Name of the role example: User')


# Role model for documentation in Swagger UI
roles_model = accounts_ns.model('Roles', {
    'name': fields.String(required=True, description='Role Name'),
    'is_admin': fields.Boolean(description='Admin Privileges'),
    'can_users': fields.Boolean(description='Permission to manage users'),
    'can_project': fields.Boolean(description='Permission to manage projects'),
    'can_geophysic': fields.Boolean(description='Permission to manage geophysic data'),
    'can_geologic': fields.Boolean(description='Permission to manage geologic data'),
    'can_hazard': fields.Boolean(description='Permission to manage hazard data'),
    'can_geodetic': fields.Boolean(description='Permission to manage geodetic data'),
})


# Parser for Roles
roles_parser = reqparse.RequestParser()
roles_parser.add_argument('name', type=str, required=False, help='Role name')
roles_parser.add_argument('is_admin', type=bool, required=False, help='Admin Privileges')
roles_parser.add_argument('can_users', type=bool, required=False, help='Manage Users')
roles_parser.add_argument('can_project', type=bool, required=False, help='Manage Projects')
roles_parser.add_argument('can_geophysic', type=bool, required=False, help='Manage Geophysic Data')
roles_parser.add_argument('can_geologic', type=bool, required=False, help='Manage Geologic Data')
roles_parser.add_argument('can_hazard', type=bool, required=False, help='Manage Hazard Data')
roles_parser.add_argument('can_geodetic', type=bool, required=False, help='Manage Geodetic Data')

accounts_model = api.model(
    'Accounts',
    {
        "id": fields.Integer(description="User ID"),
        "username": fields.String(description="Full Name (name + lastname)"),
        "email": fields.String(description="User Email"),
        "role": fields.Nested(roles_model, description="Role Details"),
    },
)