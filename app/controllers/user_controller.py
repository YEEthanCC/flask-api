import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
import datetime
from app import db
from flask import jsonify, make_response
import jwt
from app import app

def get_all_users():
    users = User.query.all()
    output = []
    for user in users:
        user_data = {}
        user_data['id'] = user.id
        user_data['fullname'] = user.fullname
        user_data['created_at'] = user.created_at
        user_data['updated_at'] = user.updated_at
        output.append(user_data)
    return jsonify({'users': output})

def get_users_by_name(fullname):
    users = User.query.filter_by(fullname=fullname).all()
    output = []
    for user in users:
        user_data = {}
        user_data['id'] = user.id
        user_data['fullname'] = user.fullname
        user_data['created_at'] = user.created_at
        user_data['updated_at'] = user.updated_at
        output.append(user_data)
    return jsonify({'users': output})

def get_user(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({'message': 'No user found!'})
    user_data = {}
    user_data['id'] = user.id
    user_data['fullname'] = user.fullname
    user_data['created_at'] = user.created_at
    user_data['updated_at'] = user.updated_at
    return jsonify({'user': user_data})

def create_user(fullname, pwd):
    hashed_pwd = generate_password_hash(pwd, method='pbkdf2:sha256')
    new_user = User(id=str(uuid.uuid4()), fullname=fullname, pwd=hashed_pwd, created_at=datetime.datetime.now(), updated_at=datetime.datetime.now()) 
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'New user created!'})

def get_user_id(fullname, pwd):
    users = User.query.filter_by(fullname=fullname).all()
    if len(users) == 0:
        return None
    for user in users:
        if check_password_hash(user.pwd, pwd): 
            # token = jwt.encode({'id': user.id, 'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)}, f"{app.config['SECRET_KEY']}")
            # return jsonify({'token': token})
            print(f"user_id={user.id}")
            return user.id
    return None

def delete_user(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({'message': 'No user found!'})
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'The user has been deleted!'})

def udpate_user(id, fullname, pwd):
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({'message': 'No user found!'})
    user.fullname = fullname
    user.pwd = generate_password_hash(pwd, method='pbkdf2:sha256')
    user.updated_at = datetime.datetime.now() 
    db.session.commit()
    return jsonify({'message': 'The user has been updated!'})