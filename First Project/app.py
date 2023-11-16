from flask import Flask, request, jsonify, make_response, redirect

# from flask_jwt_extended import JWTManager
# app.config["JWT_SECRET_KEY"] = "Elsamman"
# jwt = JWTManager(app)

#### First task this API app has been built in local python datebase so once i quit flask all date will be deleted ####


app = Flask(__name__)


users = []  # Empty list to add the users because im not using datebase

stores = [
    {"owner_id": 0, "items": [], "item_count": 0}
]  # list for stores to add on the the id's and items

owners_id = []  # Empty list to add IDs for users because im not using datebase


@app.post("/register")
def register():  # This route is to register new users
    user_id = (
        len(users) + 1
    )  # This to make ID for each user and then add it in the owner id list
    request_userdata = (
        request.get_json()
    )  # This is the given data by the client "Insomia"
    new_user = {
        "name": request_userdata["name"],
        "phone": request_userdata["phone"],
        "email": request_userdata["email"],
        "password": request_userdata["password"],
    }
    if any(len(value) == 0 for value in new_user.values()):
        # if the client forget to write any data from the 4 requested data it will ask to fill all fields
        return jsonify({"Sorry": "All fields are required"}), 400

    if any(
        new_user["email"] == user["email"] or new_user["phone"] == user["phone"]
        for user in users
    ):
        # if email or phone number already on user list then it will show a massage "User already exists"
        return jsonify({"Sorry": "User already exists"}), 400

    users.append(new_user)
    owners_id.append(user_id)
    # if the 2 condintions above where not a problem then the user will be added in the user list and his id will be add in owner id list

    return (
        jsonify({"message": "User registered successfully", "redirect_url": "/store"}),
        201,
    )


@app.get("/register")
def get_register_users():
    # I made this route just to check the user list and this is due to im not using any database so i needed to check the list
    return users


@app.post("/login")
def login():
    # This route is for login and this by only 2 fields email and password that has been given before in the register route
    request_login_data = request.get_json()
    login_user = {
        "email": request_login_data["email"],
        "password": request_login_data["password"],
    }
    for user in users:
        if (
            login_user["email"] == user["email"]
            and login_user["password"] == user["password"]
        ):
            return redirect("/store")
    return jsonify({"Sorry": "Please Check your email or password"}), 400


@app.get("/owner_id")
def owner_id():
    # I made this route just to check the owner_id list and this is due to im not using any database so i needed to check the list
    return owners_id


@app.get("/store")
def get_stores():
    # I made this route just to check the store list and this is due to im not using any database so i needed to check the list
    return {"stores": stores}


@app.post("/add_store")
def create_stores():
    request_data = request.get_json()
    new_store = {"owner id": owners_id[-1], "Items": [request_data]}
    stores.append(new_store)
    return new_store, 201


@app.post("/store/<int:owner_id>")
def find_owner_store(owner_id):
    request_products = request.get_json()
    my_store = {}
    for store in stores:
        if store["owner_id"] == owner_id:
            my_store = store
            # break
    product_name = request_products["product_name"]
    product_price = request_products["product_price"]
    my_store["items"].append(
        {"product_name": product_name, "product_price": product_price}
    )
    return my_store


@app.get("/store/<int:owner_id>")
def get_owner_store(owner_id):
    request_products = request.get_json()
    my_store = {}
    for store in stores:
        if store["owner_id"] == owner_id:
            my_store = store
            break
    product_name = request_products["product_name"]
    product_price = request_products["product_price"]
    my_store["items"].append(
        {"product_name": product_name, "product_price": product_price}
    )
    return my_store


@app.post("/store/<int:owner_id>/item")
def create_item(owner_id):
    request_data = request.get_json()
    for store in stores:
        if store["owner_id"] == owner_id:
            new_item = {"name": request_data["name"], "price": request_data["price"]}
            store["Items"].append(new_item)
            return new_item, 201
    return {"Message": "store not found"}, 404


@app.get("/store/<int:owner_id>/item")
def get__item_in_store(owner_id):
    for store in stores:
        if store["owner_id"] == owner_id:
            return {"Items": store["Items"]}
    return {"Message": "store not found"}, 404
