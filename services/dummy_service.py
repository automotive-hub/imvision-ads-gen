from flask_restful import Resource

from models.dummy_model import DummyModel


class DummyService(Resource):
    def get(self):
        dummyModel = DummyModel("test name", "test year")
        return {"name": dummyModel.name, "year": dummyModel.year}

