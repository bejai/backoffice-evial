# project/server/models.py

import datetime
from flask import current_app
from project.server import db, bcrypt


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode('utf-8')
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User {0}>'.format(self.email)


class Foto(db.Model):

    __tablename__ = 'fotos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    radar_id = db.Column(db.Integer, db.ForeignKey('radares.id'), nullable=False) # ID de radar
    secuencia_id = db.Column(db.Integer, db.ForeignKey('secuencias.id'), nullable=False)
    web_path = db.Column(db.String(255), unique=True, nullable=False)
    fs_path = db.Column(db.String(255), unique=True, nullable=False)
    vel_max = db.Column(db.Integer, nullable=False)
    vel = db.Column(db.Integer, nullable=False)
    secuencia = db.Column(db.String(255), unique=False, nullable=False)
    order = db.Column(db.Integer, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    processed = db.Column(db.Boolean, nullable=False, default=False)
    reprocess = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, customer_id,radar_id,secuencia_id,web_path,fs_path,vel_max,vel,secuencia,order,registered_on,processed=False,reprocess=False):
        self.customer_id = customer_id
	self.radar_id = radar_id
	self.secuencia_id = secuencia_id
	self.web_path = web_path
	self.fs_path = fs_path
	self.vel_max = vel_max
	self.vel = vel
	self.order = order
	self.secuencia = secuencia
        self.registered_on = registered_on # datetime.datetime.now()
	self.processed = processed
	self.reprocess = reprocess

    def get_secuencia_from_string(self,s):
	r = Secuencia.query.filter_by(secuencia=s).first()
	if r: return r
	return None

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<Foto {0}>'.format(self.web_path)


class Secuencia(db.Model):

    __tablename__ = 'secuencias'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    radar_id = db.Column(db.Integer, db.ForeignKey('radares.id'), nullable=False) # ID de radar
    web_path = db.Column(db.String(255), unique=True, nullable=False)
    fs_path = db.Column(db.String(255), unique=True, nullable=False)
    vel_max = db.Column(db.Integer, nullable=False)
    vel = db.Column(db.Integer, nullable=False)
    secuencia = db.Column(db.String(255), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    processed = db.Column(db.Boolean, nullable=False, default=False)
    reprocess = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, customer_id,radar_id,web_path,fs_path,vel_max,vel,secuencia,registered_on,processed=False,reprocess=False):
        self.customer_id = customer_id
	self.radar_id = radar_id
	self.web_path = web_path
	self.fs_path = fs_path
	self.vel_max = vel_max
	self.vel = vel
	self.secuencia = secuencia
        self.registered_on = registered_on # datetime.datetime.now()
	self.processed = processed
	self.reprocess = reprocess

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<Secuencia {0}>'.format(self.web_path)


class Radar(db.Model):

    __tablename__ = 'radares'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    pub_id = db.Column(db.String(50), unique=True, nullable=False) # ID de radar para Evial/barrio
    configuration = db.Column(db.String(2048), unique=False, nullable=True)
    registered_on = db.Column(db.DateTime, nullable=False)
    online = db.Column(db.Boolean, nullable=False, default=False)
    conn_port = db.Column(db.String(3), unique=False, nullable=True)

    def __init__(self, customer_id,pub_id,configuration,registered_on,online,conn_port='000'):
        self.customer_id = customer_id
	self.pub_id = pub_id
	self.configuration = configuration
        self.registered_on = registered_on # datetime.datetime.now()
	self.online = online
	self.conn_port = conn_port

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<Radar {0}>'.format(self.pub_id)


class Customer(db.Model):

    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pub_id = db.Column(db.String(50), unique=True, nullable=False) # ID de customer / barrio / country para Evial
    nombre = db.Column(db.String(255), unique=False, nullable=True)
    acta = db.Column(db.Boolean, nullable=False, default=False)
    acta_template = db.Column(db.String(255), unique=False, nullable=True) # Path al acta dot
    registered_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, pub_id,nombre,acta,acta_template,registered_on):
        self.pub_id = pub_id
	self.nombre = nombre
	self.acta = acta
	self.acta_template = acta_template
        self.registered_on = registered_on # datetime.datetime.now()

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<Customer {0}>'.format(self.pub_id)


