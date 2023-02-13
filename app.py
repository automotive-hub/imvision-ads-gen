from flask import Flask
from flask_restful import Api, Resource

from services.dummy_service import DummyService

app = Flask(__name__)
api = Api(app)


api.add_resource(DummyService, "/dummy")

if __name__ == "__main__":
    app.run(debug=True)
