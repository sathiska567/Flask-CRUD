from bson import ObjectId
from flask import Flask, request, jsonify
import pymongo

# Create Flask app
app = Flask(__name__)

# Connection string (replace <password> with the actual password)
mongo_uri = "mongodb+srv://sasindusathiska:Pass123@cluster0.glb4eyt.mongodb.net/?retryWrites=true&w=majority"

try:
    mongo = pymongo.MongoClient(mongo_uri, serverSelectionTimeoutMS = 5000)
    db = mongo.get_database('company')  # Access the 'company' database
    mongo.server_info()  # Trigger exception if connection failed
    print("Connected to MongoDB")
    
except Exception as e:
    print("Error - An unexpected error occurred:", e)

# Define the route handler for '/users'
# POST DATA
@app.route('/users', methods=['POST'])
def create_user():
    try:
        user = request.get_json()
        print(user)
        if not user or 'name' not in user or 'lastname' not in user:
            return jsonify({"error": "Invalid input"}), 400

        db_response = db.users.insert_one(user)
        
        return jsonify({
            "message": "User created successfully",
            "user_id": str(db_response.inserted_id)
        }), 200

    except Exception as ex:
        print("##################################")
        print(ex)

# POST DATA
@app.route("/form-details",methods=['POST'])
def form_details():
    try:
        data = request.get_json()
        print(data)
        if not data or 'district' not in data or 'province' not in data:
            return jsonify({"error": "Invalid input"}), 400

        db_response = db.form_data.insert_one(data)
        
        return jsonify({
            "message": "District created successfully",
            "user": str(db_response.inserted_id)
        }), 200
           
    except Exception as ex:
        print(ex)


# GET FORM_DATA
@app.route("/get-form-details", methods=["GET"])
def get_form_details():
    try:
        # Fetch all documents from 'form_data' collection
        data = db.form_data.find({})
        
        # Convert MongoDB cursor to list and handle ObjectId serialization
        data_list = []
        
        for document in data:
            # Convert ObjectId to string for JSON serialization
            document['_id'] = str(document['_id'])
            data_list.append(document)
        
        return jsonify({
            "message": "Form details fetched successfully",
            "data": data_list
        })

    except Exception as ex:
        print(ex)
        return jsonify({
            "error": "An error occurred while fetching form details"
        }), 500  # Internal Server Error


# GET DATA USING ID
@app.route("/get-user-using-id", methods=['POST'])
def get_user_using_id():
    try:
        # Get the _id from request JSON data
        request_data = request.get_json()
        user_id = request_data.get('user_id')

        # Convert user_id to ObjectId
        obj_id = ObjectId(user_id)

        # Query MongoDB using ObjectId
        data = db.form_data.find_one({"_id": obj_id})

        if data:
            # Convert ObjectId to string for JSON serialization
            data['_id'] = str(data['_id'])
            
            return jsonify({
                "data": data
            })
        else:
            return jsonify({
                "error": "User not found"
            }), 404  # Not Found

    except Exception as ex:
        print(ex)
        return jsonify({
            "error": "An error occurred while fetching user details"
        }), 500 
        

# UPDATE DATA
@app.route("/update-data", methods=["POST"])
def update_data():
    try:
        # Get user data from request JSON
        user = request.get_json()
        user_id = user.get('user_id')
        new_district = user.get("district")

        # Convert user_id to ObjectId
        obj_id = ObjectId(user_id)

        # Perform the update operation
        result = db.form_data.update_one(
            {"_id": obj_id},
            {"$set": {"district": new_district}}
        )

        # Check if the document was updated successfully
        if result.modified_count > 0:
            # Fetch the updated document to return in the response
            updated_document = db.form_data.find_one({"_id": obj_id})
            updated_document['_id'] = str(updated_document['_id'])  # Convert ObjectId to string

            return jsonify({
                "message": "User details updated successfully",
                "data": updated_document
            })
        else:
            return jsonify({
                "error": "User not found or no changes applied"
            }), 404  # Not Found

    except Exception as ex:
        print(ex)
        return jsonify({
            "error": "An error occurred while updating user details"
        }), 500  # Internal Server Error


# DELETE DATA
@app.route("/delete-data", methods=["POST"])
def delete_data():
    try:
        user = request.get_json()
        user_id = user.get('user_id')
        
        # convert id -> objectId
        obj_id = ObjectId(user_id)
        
        # delete data
        result = db.form_data.delete_one({"_id": obj_id})
        
        if result.deleted_count > 0:
            return jsonify({
                "message": "User details deleted successfully"                
            })
        
    except Exception as ex:
        print(ex)
        return jsonify({
            "error": "An error occurred while deleting user details"
        })



if __name__ == '__main__':
    app.run(port=80, debug=True)
