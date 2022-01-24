from flask import request, jsonify, abort, Blueprint

image_blueprint = Blueprint('image', __name__)

# Previous route :dbname/image/update/:collection
@image_blueprint.route('/images', methods=['POST'])
def upload_image():
    return jsonify({ 'message': 'Not implemented' }), 200
