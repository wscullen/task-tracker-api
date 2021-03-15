from flask import Flask, jsonify, request, make_response, current_app, abort
from flask import Blueprint

tasks_blueprint = Blueprint('tasks', __name__)

from api.models.Task import Task, task_schema, tasks_schema

from api import db


tasks = [
    {
      "id": 2,
      "text": "Meeting at School",
      "day": "Feb 6th at 1:30pm",
      "reminder": True
    },
    {
      "text": "Create Landing Page for After Analog",
      "day": "Feb 14th at 7:00pm",
      "reminder": True,
      "id": 5
    },
    {
      "text": "Shaun's Task",
      "day": "Feb 6th at 3:30pm",
      "reminder": False,
      "id": 6
    }
]

def get_highest_id():
    if len(tasks) == 0:
        return 1
    else:
        id = max([task["id"] for task in tasks])
        return id + 1

@tasks_blueprint.route('/tasks', methods=['GET', 'POST', 'OPTIONS'])
def add_or_list_tasks():
   
    db_tasks = Task.query.all()
    current_app.logger.info(db_tasks)
    current_app.logger.info(request.method)
    current_app.logger.info(tasks)
    if request.method == "GET":
        response = make_response(jsonify(tasks_schema.dump(db_tasks)))
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    elif request.method == "POST":
        if not request.json:
            abort(400)
        else:
            new_task = request.json
            for key in ["day", "text", "reminder"]:
                current_app.logger.info(key)
                if key not in new_task:
                    abort(400)

            # new_task["id"] = get_highest_id()
            # current_app.logger.info(get_highest_id())
            # current_app.logger.info(new_task)
            # tasks.append(new_task)
            # current_app.logger.info(tasks)
            # response = jsonify(new_task)

            db_task = Task(
                text=new_task["text"],
                day=new_task["day"],
                reminder=new_task["reminder"]
            )
            db.session.add(db_task)
            db.session.commit()
            db.session.flush()
            current_app.logger.info(db_task.id)
            current_app.logger.info(db_task.as_json)
            # current_app.logger.info(Task.as_json(db_task))
            response = task_schema(db_task)
            response.headers.add('Access-Control-Allow-Origin', '*')
     
            return response

    elif request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        current_app.logger.info(response)
        return response


@tasks_blueprint.route('/tasks/<int:task_id>', methods=['GET', 'DELETE', 'PATCH', 'OPTIONS'])
def fetch_modify_or_delete_task(task_id):
    global tasks
    current_app.logger.info(request.method)
    current_app.logger.info(task_id)
    if request.method == "GET":
        response = Task.get_delete_put_post(task_id)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    elif request.method == "PATCH":
        task_db = Task.query.get(task_id)
        if task_db:
            changes_to_task = request.json
            for key in changes_to_task.keys():
                current_app.logger.info(key)
                if key not in ["reminder", "text", "day"]:
                    abort(400)
                setattr(task_db, key, changes_to_task[key])
            
            db.session.commit()
            response = make_response(task_db.as_json)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        else:
            abort(404)
    elif request.method == "DELETE":
        # task = [task for task in tasks if task["id"] == task_id]
        # new_task_list = [task for task in tasks if task["id"] != task_id]
        # current_app.logger.info(task)
        # if len(task) > 0:
        #     task_deleted = task[0]
        #     tasks = new_task_list
        #     response = jsonify(task_deleted)
        #     response.headers.add('Access-Control-Allow-Origin', '*')
        #     return response
        # else:
        #     abort(404)
        response = Task.get_delete_put_post(task_id)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response



    elif request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        current_app.logger.info(response)
        return response