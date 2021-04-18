from flask import Blueprint
from core.utilities.auth_manager import auth
from core.utilities.limiter import limiter

api_test = Blueprint('api_test', __name__)

@api_test.route('/hi', methods=['GET'])
@limiter.limit("1000 per day")
@limiter.limit("3/seconds")
@auth.auth_required()
def hi():
    return { "status": "hi!" }