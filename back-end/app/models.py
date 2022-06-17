import base64
import os
from datetime import datetime, timedelta

import jwt
from flask import url_for, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data


class User(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))  # 不保存原始密码
    sex = db.Column(db.String(64))
    phone = db.Column(db.Integer)
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    avatar = db.Column(db.String(128))
    last_login_time = db.Column(db.DateTime, default=datetime.utcnow)
    create_time = db.Column(db.DateTime(), default=datetime.utcnow)
    accumulate_duration = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 将后端User对象转化为Json对象
    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            'sex': self.sex,
            'phone': self.phone,
            'location': self.location,
            'about_me': self.about_me,
            'create_time': self.create_time.isoformat() + 'Z',
            'last_login_time': self.last_login_time.isoformat() + 'Z',
            'accumulate_duration': self.accumulate_duration,
            '_links': {
                'self': url_for('api.get_user', id=self.id),
                'avatar': self.avatar,
            }
        }
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    # token = db.Column(db.String(32), index=True, unique=True)
    # token_expiration = db.Column(db.DateTime)

    # def get_token(self, expires_in=3600):
    #     now = datetime.utcnow()
    #     if self.token and self.token_expiration > now + timedelta(seconds=60):
    #         return self.token
    #     self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
    #     self.token_expiration = now + timedelta(seconds=expires_in)
    #     db.session.add(self)
    #     return self.token
    #
    # def revoke_token(self):
    #     self.token_expiration = datetime.utcnow() - timedelta(seconds=1)
    #
    # @staticmethod
    # def check_token(token):
    #     user = User.query.filter_by(token=token).first()
    #     if user is None or user.token_expiration < datetime.utcnow():
    #         return None
    #     return user

    def get_jwt(self, expires_in=600):
        now = datetime.utcnow()
        payload = {
            'user_id': self.id,
            # 'name': self.name if self.name else self.username,
            'name': self.username,
            'exp': now + timedelta(seconds=expires_in),
            'iat': now
        }
        print(jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256'))
        return jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256')

    @staticmethod
    def verify_jwt(token):
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256'])
        except (jwt.exceptions.ExpiredSignatureError, jwt.exceptions.InvalidSignatureError) as e:
            # Token过期，或被人修改，那么签名验证也会失败
            return None
        return User.query.get(payload.get('user_id'))


class Like(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, index=True)
    musicID = db.Column(db.String, index=True)
    musicType = db.Column(db.String)


class History(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, index=True)
    musicID = db.Column(db.String, index=True)
    count = db.Column(db.Integer, default=1)
    time = db.Column(db.DateTime, default=datetime.utcnow)


# class Acc(PaginatedAPIMixin, db.Model):
#     userID = db.Column(db.Integer, primary_key=True)

