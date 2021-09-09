__author__ = 'U582788'

from flask import *
import pandas as pd
from mongodb import dis_pharma_db
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return 'asdf'

# this is for HPC NMPA website update
@app.route('/getDummydata')
def testdummy():
    # No need after using flask-cors
    # response = jsonify({'some': 'data'})
    # response.headers.add('Access-Control-Allow-Origin', '*')
    # return response
    return jsonify({'some': 'data'})

# this is for HPC NMPA website update
@app.route('/postDummydata', methods=['POST'])
def testdummypost():
    # print(request.form)
    db = dis_pharma_db()
    db.insertDatatoNewProductfromTamperMonkey(request.form)
    return jsonify(code=200)

# this is for HPC NMPA website update ingredient
@app.route('/postIngredientdata', methods=['POST'])
def postingredient():
    db = dis_pharma_db()
    db.insertDatatoIngredientsfromTamperMonkey(request.form)
    return jsonify(code=200)

# this is for HPC NMPA website delete new records
@app.route('/deletenewrecord', methods=['POST'])
def deletenewrecord():
    db = dis_pharma_db()
    db.deleteDatafromnewproducts(request.form)
    return jsonify(code=200)



# this is for Pharma NMPA website update
@app.route('/insertpharmadata', methods=['POST'])
def insertpharmadata():
    db = dis_pharma_db()
    db.insertDatatoPEGUSCHNfromTamperMonkey(request.form)
    # print(request.form)
    return jsonify(code=200)



# this is for Lazada website
@app.route('/insertlazadaproducts', methods=['POST'])
def insertlazadaproduct():
    # print(request.form)
    db = dis_pharma_db()
    db.insertDatatoLazadaProductfromTamperMonkey(request.form)
    return jsonify(code=200)

@app.route('/insertlazadaproducts_new', methods=['POST'])
def insertlazadaproduct_new():
    # print(request.form)
    db = dis_pharma_db()
    db.insertDatatoLazadaProductfromTamperMonkeyNew(request.form)
    return jsonify(code=200)

@app.route('/insertlazadaproductdetail', methods=['POST'])
def insertlazadaproductdetail():
    # print(request.form)
    data = json.loads(request.form['data'])
    try:
        dic = {'url': request.form['url'], 'fields': data.get('fields'), 'extract_date':'2021-09'}
        db = dis_pharma_db()
        db.insertDatatoLazadaProductDetailfromTamperMonkey(dic)
    except Exception as e:
        print('error')
        pass
    # db.insertDatatoLazadaProductfromTamperMonkey(request.form)
    return jsonify(code=200)



# this is for QiChaCha website
@app.route('/insertqichacha', methods=['POST'])
def insertqichacha():
    print(request.form)
    result = ""
    for a in request.form.keys():
        result = result + a
    db = dis_pharma_db()
    # databasename = 'dis_pharma'
    databasename = 'dcs_antiform'
    db.insertqichacha(result, databasename)
    return jsonify(code=200)


if __name__ =='__main__':
    app.run(debug = True)