from flask import Flask
from flask_cors import cross_origin, CORS
from flask_restful import Api, Resource

from services.dummy_service import DummyService
from dotenv import load_dotenv

load_dotenv("./module_editly.env")

app = Flask(__name__)
api = Api(app)
CORS(app, supports_credentials=True)

api.add_resource(DummyService, "/dummy/<vinWithSalt>")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", ssl_context='adhoc')
