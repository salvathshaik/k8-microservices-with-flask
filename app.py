from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import socket
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongo:27017/dev" #using dev named DB
mongo = PyMongo(app)
db = mongo.db
@app.route("/") #health-check-api
def index():
    hostname = socket.gethostname()
    title = 'Welcome to Salwad Basha Task App'
    message="Welcome to Tasks app! I am running inside {} pod!".format(hostname)
    return render_template('index.html', title=title, body_text=message)
@app.route("/tasks") #to list all the tasks
def get_all_tasks():
    tasks = db.task.find()
    data = []
    for task in tasks:
        item = {
            "id": str(task["_id"]),
            "task": task["task"]
        }
        data.append(item)
    return jsonify(
        data=data
    )
@app.route("/task", methods=["POST"]) #to add task by giving task value
def create_task():
    data = request.get_json(force=True)
    db.task.insert_one({"task": data["task"]})
    return jsonify(
        message="Task saved successfully!"
    )
@app.route("/task/<id>", methods=["PUT"]) #to update the task using it's ID
def update_task(id):
    data = request.get_json(force=True)["task"]
    response = db.task.update_one({"_id": ObjectId(id)}, {"$set": {"task": data}})
    if response.matched_count:
        message = "Task updated successfully!"
    else:
        message = "No Task found!"
    return jsonify(
        message=message
    )
@app.route("/task/<id>", methods=["DELETE"]) #to delete one task using its ID
def delete_task(id):
    response = db.task.delete_one({"_id": ObjectId(id)})
    if response.deleted_count:
        message = "Task deleted successfully!"
    else:
        message = "No Task found!"
    return jsonify(
        message=message
    )
@app.route("/tasks/delete", methods=["POST"]) #to delete all the tasks at once
def delete_all_tasks():
    db.task.delete_many({}) #Use 'delete_many' with an empty filter to delete all documents
    return jsonify(
        message="All Tasks deleted!"
    )
if __name__ == "__main__": #running this app using port 5000 while we run this file(app.py) it will initialize
    app.run(host="0.0.0.0", port=5000)
