from typing import List
from typing import Any
from dataclasses import dataclass
import json

from dataclasses import dataclass
from typing import List


@dataclass
class DealershipInfo:
    name: str
    location: str


@dataclass
class VehicleInfo:
    vehicle_name: str
    vin: str
    price: int
    dealership_info: DealershipInfo
    vehicle_public_url_imgs: List[str]
    vehicle_local_imgs: List[str]


# @dataclass
# class DealershipInfo:
#     name: str
#     location: str

#     @staticmethod
#     def from_dict(obj: Any) -> 'DealershipInfo':
#         _name = str(obj.get("name"))
#         _location = str(obj.get("location"))
#         return DealershipInfo(_name, _location)


# @dataclass
# class Root:
#     vehicleName: str
#     vin: str
#     price: int
#     dealershipInfo: DealershipInfo
#     vehicleIMGs: List[str]

#     @staticmethod
#     def from_dict(obj: Any) -> 'Root':
#         _vehicleName = str(obj.get("vehicleName"))
#         _vin = str(obj.get("vin"))
#         _price = int(obj.get("price"))
#         _dealershipInfo = DealershipInfo.from_dict(obj.get("dealershipInfo"))
#         _vehicleIMGs = [Root.from_dict(y) for y in obj.get("vehicleIMGs")]
#         return Root(_vehicleName, _vin, _price, _dealershipInfo, _vehicleIMGs)

# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)

{
    "vehicleName": "XXX",
    "vin": "xxxx",
    "price": 0,
    "dealershipInfo": {
        "name": "xxx",
        "location": "xxx"
    },
    "vehicleIMGs": [""]
}
