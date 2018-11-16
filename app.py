from flask import Flask, request, make_response
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.contrib.cache import SimpleCache
from L.Login import cachehave
from flask import flash, redirect, url_for
from L.Account import Account
from L.AccountTable import AccountTable
import tool

autologinCache = SimpleCache()   #用于自动登陆的缓存


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')


app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'  # for example, '3ef6ffg4'


@app.route('/', methods=['post', 'get'])
def home():
    return redirect(url_for('login'))


@app.route('/login', methods=['post', 'get'])
def login():
    user = request.cookies.get('userID')
    if cachehave(user,  autologinCache):
        return redirect(url_for('table'))
    else:
        return render_template('Login/login.html')


@app.route('/dispatch', methods=['get', 'post'])
def chart():
    return render_template('Admin/dispatch.html')


@app.route('/system', methods=['get', 'post'])
def calendar():
    return render_template('Admin/system.html')


@app.route('/revenue', methods=['get', 'post'])
def grid():
    return render_template('Admin/revenue.html')


@app.route('/icon', methods=['get', 'post'])
def icon():
    return render_template('Admin/icon.html')


@app.route('/tour', methods=['get', 'post'])
def tour():
    return render_template('Admin/tour.html')


@app.route('/user_info', methods=['post', 'get'])
def user_info():
    return app.send_static_file('user_info.html')


@app.route('/ticket', methods=['get'])
def ticket():
    return app.send_static_file('ticket.html')


@app.route('/logincookie', methods=['post', 'get'])
def giveweb():
    user = request.form.get('user')
    password = request.form.get('password')

    a = Account(user, password)
#   AccountTable().insert_account(a)
    t = AccountTable().login(a)
    if t==2:
        res = app.make_response(redirect('table'))
        res.set_cookie('userID', user)
        autologinCache.set(user, 1, timeout=1 * 60)
        return res


@app.route('/userTable', methods=['get', 'post'])
def user_table():
    bus_list = tool.get_buses()
    return render_template('User/user.html', buses=bus_list)


@app.route('/blank', methods=['get', 'post'])
def result():
    start = request.form.get('起点站')
    end = request.form.get("终点站")
    bus_list = tool.get_bus(start, end)
    return render_template('User/user.html', buses=bus_list)


@app.route('/adminTable', methods=['get', 'post'])
def table():
    context = {
        'shift': 'text',
        'starttime': '14:00',
        'arrivetime': '15:00',
        'fare': '100',
        'remainvote': '50'
    }
    return render_template('Admin/table.html', **context)


if __name__ == '__main__':
    app.run(port=8000, debug=True)
