"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    # response_body = {
    #     "hello": "world",
    #     "family": members
    # }

    if members == "Member not found":
        return jsonify(members), 400
    return jsonify(members), 200

@app.route('/members/<int:members_id>', methods=['GET'])
def handle_member():
    members = jackson_family.get_member(members._id)
    json_text = jsonify(members)
    return json_text

@app.route('/members', methods=['POST'])
def add_member():
    request_body = request.json 
    members = jackson_family.add_members(request_body)
    # print("Incoming request with the following body", request_body)
    
    if members == "Member not found":
        return jsonify(members), 400
    return jsonify(members), 200

# underscore

@app.route('/members/<int:members_id>', methods=['DELETE'])
def delete_todo(members_id):
    member = jackson_family.delete_member(members_id) 
    return jsonify(member)

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
