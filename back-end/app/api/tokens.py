from datetime import datetime

from flask import jsonify, g
from app import db
from app.api import bp
from app.api.auth import basic_auth, token_auth


@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = g.current_user.get_jwt()
    user = g.current_user
    user.last_login_time = datetime.utcnow()
    db.session.commit()
    return jsonify({'token': token})
