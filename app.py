import json

from flask import Flask,request,render_template
app = Flask(__name__)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/cars_api"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/restapi'  #conn -- mysql
app.config["SQLALCHEMY_ECHO"] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.template_folder = "pages/"

#
db = SQLAlchemy(app)  # Flask app instance --> sqlalchemy --> db configuration.
#db--> type ?? --> SQLAlChemy --> what that object is aware --> app --> Flask instance
    #---> configuration de kr rh hai..
class Product(db.Model):
    __tablename__ ='product11'
    id=db.Column("product_id",db.Integer,primary_key=True)
    name=db.Column("Product_name",db.String(20))
    image = db.Column('customer_photo', db.String(255), default='NA')
db.create_all()

@app.route("/",methods=['GET'])
def welcome_page():
    return "api is running......."
@app.route("/add/product",methods=['POST'])

def add_product():
    reqdata=request.get_json()
    prod=Product(id=reqdata.get("id"),
                 name=reqdata.get("name"))
    db.session.add(prod)
    db.session.commit()
    return json.dumps({"success":"Product added succesfully"})

@app.route("/show/product",methods=['GET'])
def show_all_product():
    prodList=Product.query.all()
    projson=[]
    for prod in prodList:
       prod={"id":prod.id,"name":prod.name}
       projson.append(prod)
    return json.dumps(projson)

@app.route("/search/product/<int:pid>",methods=['GET'])
def search_product(pid):
    prod=Product.query.filter_by(id=pid).first()
    if prod:
        return json.dumps({"id":prod.id,"name":prod.name})
    else:
        return json.dumps({"error":"not found"})


@app.route('/api/v1/customer/image',methods=['POST'])
def save_customer_with_image():
    #pure json in body -- request.get_json()
    #multimediate --> request.form -- jsoncontents ---> multimediate contents -- request.files
    reqBody = request.form   # form data -
    multimedia = request.files

    print('FORMDATA', reqBody)
    print('Multimedia Contents ---',multimedia)

    prod = Product(name=reqBody.get('name'))
    if multimedia.get('CUSTOMER_DP'):
        prod.image = 'E:\\ashwini\\flask_demo\\flask_restapi\\resource\\{}.png'.format(reqBody.get('name'))
    db.session.add(prod)
    db.session.commit()
    message = "Customer recorded successfully...!"

    file =multimedia.get('CUSTOMER_DP')
    file.save('E:\\ashwini\\flask_demo\\flask_restapi\\resource\\{}.png'.format(reqBody.get('name')))
    return json.dumps({"SUCCESS": message})






if __name__=='__main__':
    app.run(debug=True)
