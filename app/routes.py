from flask import json, request, jsonify
import flask
from bson import json_util
from app import app
from app import db
from bson.objectid import ObjectId

@app.route('/')
@app.route('/index')
def index():
    return flask.jsonify(json.loads(json_util.dumps(db.notafiscal.find({}).sort("_id", 1))))

@app.route("/create")
def create():
    return flask.render_template('create.html')

@app.route('/createAction', methods=['POST'])
def createAction():
    json_data = request.form.to_dict()
    if json_data:
        if db.notafiscal.insert_one(json_data).inserted_id is not None:
            return jsonify(mensagem='Nota fiscal inserida')
        else:
            return jsonify(mensagem='Não inserida')
    else:
        return jsonify(mensagem='Nada a inserir')

@app.route("/update/<string:id>")
def update(id):
    try:
        nota = db.notafiscal.find_one({"_id": ObjectId(id)})
        if nota is not None:
            return flask.render_template('update.html', nota=nota)
        else:
            return jsonify(mensagem='Nota não encontrada')
    except Exception as e:
        return jsonify(mensagem=f'Erro: {str(e)}')


@app.route('/updateAction', methods=['POST'])
def updateAction():
    json_data = request.form.to_dict()
    if json_data:
        if db.notafiscal.update_one(
            {'_id': ObjectId(json_data["_id"])},
            {"$set": {
                'numero': json_data["numero"],
                'comprador': json_data["comprador"],
                'cnpj': json_data["cnpj"],
                'endereco': json_data["endereco"],
                'telefone': json_data["telefone"],
                'data': json_data["data"],
                'valor': json_data["valor"],
                'itens': json_data["itens"]
            }}
        ).modified_count > 0:
            return jsonify(mensagem='Nota fiscal alterada')
        else:
            return jsonify(mensagem='Não alterada')
    else:
        return jsonify(mensagem='Nada a alterar')

@app.route("/delete/<string:id>")
def delete(id):
    try:
        result = db.notafiscal.delete_one({"_id": ObjectId(id)})
        if result.deleted_count > 0:
            return jsonify(mensagem='Nota removida com sucesso')
        else:
            return jsonify(mensagem='Nota não encontrada')
    except Exception as e:
        return jsonify(mensagem=f'Erro: {str(e)}')