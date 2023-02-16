from flask import Flask
from flask_restful import Api, Resource

from services.dummy_service import DummyService
from dotenv import load_dotenv

load_dotenv("./module_editly.env")

app = Flask(__name__)
api = Api(app)


api.add_resource(DummyService, "/dummy/<vin>")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
