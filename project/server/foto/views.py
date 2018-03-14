# project/server/foto/views.py


from flask import render_template, Blueprint, url_for, redirect, flash, request
from flask_login import login_user, logout_user, login_required

from project.server import bcrypt, db
from project.server.models import User, Foto, Secuencia
# from project.server.user.forms import LoginForm, RegisterForm
from project.server.foto.forms import ProcessForm

import datetime


foto_blueprint = Blueprint('foto', __name__,)


#@user_blueprint.route('/register', methods=['GET', 'POST'])
#def register():
#    form = RegisterForm(request.form)
#    if form.validate_on_submit():
#        user = User(
#            email=form.email.data,
#            password=form.password.data
#        )
#        db.session.add(user)
#        db.session.commit()
#
#        login_user(user)
#
#        flash('Thank you for registering.', 'success')
#        return redirect(url_for("user.members"))

#    return render_template('user/register.html', form=form)


#@user_blueprint.route('/login', methods=['GET', 'POST'])
#def login():
#    form = LoginForm(request.form)
#    if form.validate_on_submit():
#        user = User.query.filter_by(email=form.email.data).first()
#        if user and bcrypt.check_password_hash(
#                user.password, request.form['password']):
#            login_user(user)
#            flash('You are logged in. Welcome!', 'success')
#            return redirect(url_for('user.members'))
#        else:
#            flash('Invalid email and/or password.', 'danger')
#            return render_template('user/login.html', form=form)
#    return render_template('user/login.html', title='Please Login', form=form)


#@user_blueprint.route('/logout')
#@login_required
#def logout():
#    logout_user()
#    flash('You were logged out. Bye!', 'success')
#    return redirect(url_for('main.home'))


@foto_blueprint.route('/fotos')
@login_required
def fotos():
    foto = Foto.query.filter_by(id=1).first()
    return render_template('foto/fotos.html', frame=foto)

@foto_blueprint.route('/fotos_10')
@login_required
def fotos_10():
    fotos = Foto.query.order_by(Foto.secuencia, Foto.order).limit(25).all()
    return render_template('foto/fotos_10.html', fotos=fotos)

@foto_blueprint.route('/fotos_table')
@login_required
def fotos_table():
    fotos = Foto.query.order_by(Foto.secuencia, Foto.order).limit(25).offset(100000).all()
    w, h = 160, 120
    return render_template('foto/fotos_table.html', fotos=fotos, w=w, h=h)

@foto_blueprint.route('/fotos_table_offset/<int:offset>')
@login_required
def fotos_table_offset(offset=0):
    fotos = Foto.query.order_by(Foto.secuencia, Foto.order).limit(25).offset(offset).all()
    w, h = 160, 120
    return render_template('foto/fotos_table.html', fotos=fotos, w=w, h=h)

@foto_blueprint.route('/fotos_modal/<int:offset>')
@login_required
def fotos_modal(offset=0):
    fotos = Foto.query.order_by(Foto.secuencia, Foto.order).limit(25).offset(offset).all()
    w, h = 160, 120
    return render_template('foto/fotos_modal.html', fotos=fotos, w=w, h=h)

@foto_blueprint.route('/fotos_secuencia/<int:secuencia_id>')
@login_required
def fotos_secuencia(secuencia_id=0):
    fotos = Foto.query.filter_by(secuencia_id=secuencia_id).order_by(Foto.order).all()
    w, h = 160, 120
    form = ProcessForm()
    return render_template('foto/fotos_modal.html', fotos=fotos, w=w, h=h, form=form)

@foto_blueprint.route('/secuencias')
@login_required
def secuencias():
    secuencias = Secuencia.query.limit(25).all()
    return render_template('foto/secuencias_table.html', secuencias=secuencias)
