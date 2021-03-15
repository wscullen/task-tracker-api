from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy

from api.exts import db
from api.routes.Task import tasks_blueprint

def register_extensions(app):
  db.init_app(app)

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../tmp/test.db'
    
    register_extensions(app)
    app.register_blueprint(tasks_blueprint)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)