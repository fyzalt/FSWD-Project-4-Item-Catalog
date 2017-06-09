from flask import Flask, render_template, request, \
                  redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Layout, Building, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Clash of Clan Catalog"

engine = create_engine('sqlite:///cocbuildingwithuser.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login', methods=['GET', 'POST'])
def showLogin():
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    request.get_data()
    # Obtain one-time code
    code = request.data.decode('utf-8')

    try:
        # Exchange code foe credentials with google ap1 server
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store credential information for later use
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')

    # Check if user already logged in
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # At this point, the access token is valid
    # Store the access token in the session for later use.
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    # Store user info in the session
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't create new user
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' <" style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    return output


@app.route('/logout')
def showLogout():
    gdisconnect()
    flash('Successfully Logged Out ')
    return redirect(url_for('cocLayout'))


@app.route('/gdisconnect')
def gdisconnect():
    # Check if user is connected.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# User Helper Functions
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


# JSON ENDPOINT ADDED
@app.route('/layout/JSON')
def allLayoutJSON():
    allLayout = session.query(Layout).all()
    return jsonify(allLayout=[i.serialize for i in allLayout])


@app.route('/layout/<int:layout_id>/building/JSON')
def layoutJSON(layout_id):
    layout = session.query(Layout).filter_by(id=layout_id).one()
    items = session.query(Building).filter_by(layout_id=layout_id).all()
    return jsonify(Layout=[i.serialize for i in items])


@app.route('/layout/<int:layout_id>/building/<int:building_id>/JSON')
def buildingJSON(layout_id, building_id):
    building = session.query(Building).filter_by(id=building_id).one()
    return jsonify(Building=building.serialize)


# Creat route and function to display all base layout
@app.route('/')
@app.route('/layout')
def cocLayout():
    layout = session.query(Layout).all()
    if 'username' not in login_session:
        return render_template('publiclayout.html', layout=layout)
    else:
        return render_template('layout.html', layout=layout)


# Create a new base layout
@app.route('/layout/new', methods=['GET', 'POST'])
def newLayout():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newLayout = Layout(name=request.form['name'], user_id=login_session['user_id'])
        session.add(newLayout)
        flash('New Base %s Successfully Created' % newLayout.name)
        session.commit()
        return redirect(url_for('cocLayout'))
    else:
        return render_template('newlayout.html')


# Edit a base layout
@app.route('/layout/<int:layout_id>/edit/', methods=['GET', 'POST'])
def editLayout(layout_id):
    editedLayout = session.query(Layout).filter_by(id=layout_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedLayout.user_id != login_session['user_id']:
        return render_template('showwarning.html')
    if request.method == 'POST':
        if request.form['name']:
            editedLayout.name = request.form['name']
            flash('Layout Successfully Edited ')
            return redirect(url_for('cocLayout'))
    else:
        return render_template('editlayout.html', layout_id=layout_id, item=editedLayout)


# Delete a layout
@app.route('/layout/<int:layout_id>/delete/', methods=['GET', 'POST'])
def deleteLayout(layout_id):
    layoutToDelete = session.query(Layout).filter_by(id=layout_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if layoutToDelete.user_id != login_session['user_id']:
        return render_template('showwarning.html')
    if request.method == 'POST':
        session.delete(layoutToDelete)
        flash('%s Successfully Deleted' % layoutToDelete.name)
        session.commit()
        return redirect(url_for('cocLayout'))
    else:
        return render_template('deletelayout.html', item=layoutToDelete)


# Creat route and function to display all buildings under a layout
@app.route('/layout/<int:layout_id>/building')
def cocBuilding(layout_id):
    layout = session.query(Layout).filter_by(id=layout_id).one()
    items = session.query(Building).filter_by(layout_id=layout.id)
    author = getUserInfo(layout.user_id)
    if 'username' not in login_session or author.id != login_session['user_id']:
        return render_template('publicbuilding.html', layout=layout, items=items, author=author)
    else:
        return render_template('building.html', layout=layout, items=items, author=author)


# Create route and function to add new building under a layout
@app.route('/layout/<int:layout_id>/new/', methods=['GET', 'POST'])
def newBuildingItem(layout_id):
    layout = session.query(Layout).filter_by(id=layout_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if login_session['user_id'] != layout.user_id:
        return render_template('showwarning2.html', layout_id=layout_id)
    if request.method == 'POST':
        newBuilding = Building(name=request.form['name'], description=request.form['description'],
                               level=request.form['level'], category=request.form['category'], layout_id=layout_id)
        session.add(newBuilding)
        session.commit()
        flash("New Building Constructed!")
        return redirect(url_for('cocBuilding', layout_id=layout_id))
    else:
        return render_template('newbuilding.html', layout_id=layout_id)


# Create route and function to edit existing building
@app.route('/layout/<int:layout_id>/<int:building_id>/edit', methods=['GET', 'POST'])
def editBuildingItem(layout_id, building_id):
    layout = session.query(Layout).filter_by(id=layout_id).one()
    editedItem = session.query(Building).filter_by(layout_id=layout_id, id=building_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if login_session['user_id'] != layout.user_id:
        return render_template('showwarning2.html', layout_id=layout_id)
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['level']:
            editedItem.level = request.form['level']
        if request.form['category']:
            editedItem.category = request.form['category']
        session.add(editedItem)
        session.commit()
        flash("Construction Done!")
        return redirect(url_for('cocBuilding', layout_id=layout_id))
    else:
        return render_template(
            'editbuilding.html', layout_id=layout_id, building_id=building_id, item=editedItem)


# Creat route and function to delete existing building
@app.route('/layout/<int:layout_id>/<int:building_id>/delete', methods=['GET', 'POST'])
def deleteBuildingItem(layout_id, building_id):
    layout = session.query(Layout).filter_by(id=layout_id).one()
    itemToDelete = session.query(Building).filter_by(id=building_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if login_session['user_id'] != layout.user_id:
        return render_template('showwarning2.html', layout_id=layout_id)
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Building Implosion Done")
        return redirect(url_for('cocBuilding', layout_id=layout_id))
    else:
        return render_template(
            'deletebuilding.html', layout_id=layout_id, item=itemToDelete)


if __name__ == '__main__':
    app.secret_key = 'g7HC2ZpP47Y827VT2shix2GI'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
