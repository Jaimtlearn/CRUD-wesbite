from App import app, db
from flask import render_template, jsonify, request
from App.models import Item
import json

@app.route('/')
def home():
    return render_template('Home.html',title="Home")

# For adding items
@app.route('/item/add',methods=['POST','GET'])
def adding_items():
    if request.method == 'POST':
        if request.is_json:
            json_content = request.get_json()
            if 'name' not in json_content:
                return jsonify({"msg": "Name is required"}), 400
            item = Item(name=json_content['name'], description=json_content.get('descr'))
            db.session.add(item)
            db.session.commit()
            return jsonify({"msg": "successful"}), 201
        else:
            req = request.args
            if 'name' not in req:
                return jsonify({"msg": "Name is required"}), 400
            item = Item(name=req.get('name'), description=req.get('descr'))
            db.session.add(item)
            db.session.commit()
            return jsonify({"msg": "successful"}), 201

# For getting item/s
@app.route('/item/get')
@app.route('/item/get/<int:id>')
def getting_items(id=None):
    if id is None:
        items = Item.query.all()
        print([item.to_dict() for item in items])
        return jsonify([item.to_dict() for item in items]), 200
    else:
        item = Item.query.get(id)
        if item is None:
            return jsonify({"msg" : "Id not found in database"}),404
        return jsonify(item.to_dict()),200

# For updating item
@app.route('/item/update/json', methods=['PUT'])
def update_iten_with_json():
    print(request.is_json)
    if request.is_json:
        json_content = request.get_json()
        print(json_content)
        if "id" not in json_content:
            return jsonify({"msg" : "Id not passed in json"}),404
        else:
            if "name" not in json_content:
                return jsonify({"msg" : "Name not passed in json"}),404
            if "descr" not in json_content:
                return jsonify({"msg" : "description not passed in json"}),404
            item = Item.query.get(json_content['id'])
            if item is None:
                return jsonify({"msg" : "Id not found in database"}),404
            item.name = json_content['name']
            item.description = json_content['descr']
            db.session.commit()
            return jsonify({"msg" : "Successful updation"}),201
    else:
        return jsonify({"msg" : "send data through json"}),400
            

@app.route('/item/update/params/<int:id>', methods = ['PUT'])
def update_item_with_paramas(id=None):
    req = request.args
    if req is None:
        return jsonify({"msg" : "pass data through params"}),404
    if id is None:
        return jsonify({"msg" : "Id not passed as param"}),404
    if 'name' not in req:
        return jsonify({"msg" : "Name not passed as param"}),404
    if "descr" not in req:
        return jsonify({"msg" : "description not passed in param"}),404
    item = Item.query.get(id)
    if item is None:
        return jsonify({"msg" : "Id not found in database"}),404
    item.name = req['name']
    item.description = req['descr']
    db.session.commit()
    return jsonify({"msg" : "Successful updation"}),201



# For Deleting item
@app.route('/item/delete/<int:id>', methods = ['DELETE', 'GET'])
def DeleteItem(id=None):
    if id is None:
        return jsonify({"msg" : "No id passed. Pass Id as param"})
    else:
        item = Item.query.get_or_404(id)
        if item != 404:
            db.session.delete(item)
            db.session.commit()
        return jsonify({"msg" : "Deletion Successful"}),204
            