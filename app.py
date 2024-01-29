import os
from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from models import db, bcrypt
from flask_cors import CORS
from users import UserRegistrationResource, UserLoginResource, UserResource, RefreshTokenResource
from Events import EventResource, AdminEventResource
from tickets import TicketResource, AdminTicketResource
from review import ReviewResource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stellar.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies'] 
app.config['JWT_COOKIE_CSRF_PROTECT'] = False  # Disable CSRF protection for cookies
app.config['JWT_COOKIE_SECURE'] = False  # Set to True in a production environment with HTTPS
app.config['JWT_REFRESH_COOKIE_PATH'] = '/refresh'  
app.config['JWT_REFRESH_COOKIE_SECURE'] = False  # Set to True in a production environment with HTTPS
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = False  # Use False to make refresh tokens never expire

api = Api(app)
jwt = JWTManager(app)

db.init_app(app)
bcrypt.init_app(app)
CORS(app)

migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

api.add_resource(UserRegistrationResource, '/register')
api.add_resource(UserLoginResource, '/login')
api.add_resource(UserResource, '/user')
api.add_resource(RefreshTokenResource, '/refresh_token')
api.add_resource(EventResource, '/events', '/events/<int:event_id>')
api.add_resource(AdminEventResource, '/admin/events', '/admin/events/<int:event_id>')
api.add_resource(TicketResource, '/tickets', '/tickets/<int:ticket_id>')
api.add_resource(AdminTicketResource, '/admin/tickets', '/admin/tickets/<int:ticket_id>')
api.add_resource(ReviewResource, '/reviews', '/reviews/<int:review_id>')


if __name__ == '_main_':
    app.run(debug=True, use_reloader=True)