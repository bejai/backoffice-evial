# manage.py

import unittest

import coverage
from flask.cli import FlaskGroup

from project.server import create_app, db
from project.server.models import User, Foto, Secuencia, Customer, Radar

# backoffice project imports
import datetime
from os import listdir
import tarfile
import shutil


app = create_app()
cli = FlaskGroup(create_app=create_app)

# code coverage
COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/server/config.py',
        'project/server/*/__init__.py'
    ]
)
COV.start()


@cli.command()
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def drop_db():
    """Drops the db tables."""
    db.drop_all()


@cli.command()
def create_admin():
    """Creates the admin user."""
    db.session.add(User(email='ad@min.com', password='admin', admin=True))
    db.session.commit()


@cli.command()
def create_foto_sample():
    """Creates a foto sample."""
    db.session.add(Foto(customer_id='BerniLab',
			radar_id='labb',
			web_path='fotos/bonzenn',
			fs_path='/var/wwww',
			vel_max=30,
			vel=35,
			order='004',
			secuencia='Bernilab-lab-01-01-2018-12-00-00-30-38',
			registered_on=datetime.datetime.now(),
			processed=False,
			reprocess=False))
    #print dir(db.session)
    print "commited"
    db.session.commit()


@cli.command()
def untar_fotos():
    """Process tar files."""

    tars = listdir('/home/fotos')

    for tar in tars:
	if tar.split('.')[-1:] <> ['tar']: continue
	radar_id_parts = tar.split('.')[0].split('-')[:-3]
	print radar_id_parts
	customer_pub_id = radar_id_parts[0]
	radar_id = '-'.join(radar_id_parts)
	radar_pub_id = radar_id
	print tar
	print customer_pub_id
	print radar_pub_id

	# open tar file
	tf = tarfile.open('/home/fotos/%s' % tar,'r')

	# Busco customer (barrio) que pertenece y si no existe la agrego
	r = Customer.query.filter_by(pub_id=customer_pub_id).first()
	if r is None:
	    s = Customer(pub_id=customer_pub_id, nombre='',acta=False,acta_template='',registered_on=datetime.datetime.now())
	    db.session.add(s)
	    db.session.flush()
	    customer_id = s.id
	    print "customer commited"
	    db.session.commit()
	else:
	    customer_id = r.id

	# Busco radar y si no existe la agrego
	r = Radar.query.filter_by(pub_id=radar_pub_id).first()
	if r is None:
	    s = Radar(pub_id=radar_pub_id, customer_id=customer_id, configuration='', registered_on=datetime.datetime.now(), online=None, conn_port=None)
	    db.session.add(s)
	    db.session.flush()
	    radar_id = s.id
	    print "radar commited"
	    db.session.commit()
	else:
	    radar_id = r.id

	# Start tarfile processing
	for m in tf.getmembers():
	    if m.name.split('.')[-1:] <> ['jpg']: continue
    	    frame_name = m.name.split('/')[-1]
	    parts = frame_name.split('.')[0].split('-')
	    secuencia = '-'.join(parts[:-3])
	    day,month,year,hh,mm,ss,vmax,vel,order = parts[-9],parts[-8],parts[-7],parts[-6],parts[-5],parts[-4],parts[-3],parts[-2],parts[-1]
	    short_name =  m.name.split('/')[4:]
	    m.path = '/home/backoffice/fotos/%s/%s' % (radar_id,'/'.join(short_name))
	    pure_path = 'fotos/%s/%s' % (radar_id,'/'.join(short_name))

	    # Extraigo el file.jpg modificado..
	    tf.extract(m)

	    # Busco la secuencia a la que pertenece y si no existe la agrego
	    r = Secuencia.query.filter_by(secuencia=secuencia).first()
	    if r is None:
		s = Secuencia(customer_id=customer_id, radar_id=radar_id, web_path=pure_path, fs_path=pure_path, vel_max=vmax, vel=vel, secuencia=secuencia, registered_on=datetime.datetime.strptime('%s/%s/%s %s:%s:%s' % (year,month,day,hh,mm,ss), '%Y/%m/%d %H:%M:%S'), processed=False, reprocess=False)
		db.session.add(s)
		db.session.flush()
		secuencia_id = s.id
		print "secuencia commited"
		db.session.commit()
	    else:
		secuencia_id = r.id

	    # Busco la foto, si no existe la agrego
	    f = Foto.query.filter_by(web_path=pure_path).first()
	    if f is None:
		f = Foto(customer_id=customer_id, radar_id=radar_id, secuencia_id=secuencia_id, web_path=pure_path, fs_path=m.path, vel_max=vmax, vel=vel, order=order, secuencia=secuencia,	registered_on=datetime.datetime.strptime('%s/%s/%s %s:%s:%s' % (year,month,day,hh,mm,ss), '%Y/%m/%d %H:%M:%S'), processed=False, reprocess=False)
		db.session.add(f)
		print "foto commited"
		db.session.commit()

	tf.close()


@cli.command()
def list_fotos():
    """List fotos."""
    fotos = db.session.query(Foto).all()
    for f in fotos:
	print f.secuencia


@cli.command()
def list_fotos_10():
    """List fotos."""
    fotos = db.session.query(Foto).all().limit(10)
    for f in fotos:
	print f.secuencia


@cli.command()
def create_data():
    """Creates sample data."""
    pass


@cli.command()
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@cli.command()
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1



if __name__ == '__main__':
    cli()
