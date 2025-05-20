"""
This is Fake Flask App.
Simulation is designed to practice basic flask skills.

All new ednpoins to be added in `API Endpoints` section
========================================================
How to use? 
Copy this module content and execute in one of the below online compilers:

https://www.programiz.com/python-programming/online-compiler/
https://pycompile.com/
https://www.online-python.com/

========================================================
Task1

Create new endpoint `/api/data` to insert new data item. 
Expected request body: {"id": 1, "value": 100}
In order to insert data item to database use DataOrmObj and db.add method 
Extra: Add exceptuion handling. 

Acceptance criteria:
    Run this script. The following response should appear in terminal
    ```
    {
      "status": 200,
      "data": {
        "msg": "Success",
        "data": {
          "id": 1,
          "name": "X",
          "value": 42
        }
      }
    }
    ```
    instead of: `{"error": "404 Not Found", "path": "/api/data", "method": "POST"}`
    
=========================================================
Task 2

Implement endpoint `/api/data` to update data item record in db. 
Expected request body: {"id": 1, "value": 100}
Use db.update method and with arguments obj_id, data

Acceptance criteria:
    Run this script. The following response should appear in terminal
    ```
    {
      "status": 200,
      "data": {
        "msg": "Updated",
        "data": {
          "id": 1,
          "name": "X",
          "value": 100
        }
      }
    }
    ```
    instead of: `{"error": "404 Not Found", "path": "/api/data", "method": "PUT"}`
"""

import json
from functools import wraps


# === STUB: Simulated request and response ===
class Request:
    def __init__(self, method, path, body=None):
        self.method = method.upper()
        self.path = path
        self.body = body or {}

class Response:
    def __init__(self, status=200, data=None):
        self.status = status
        self.data = data

    def json(self):
        return json.dumps({"status": self.status, "data": self.data}, indent=2)

# === ROUTER REGISTRY ===
routes = {}

def endpoint(path, methods=['GET']):
    def decorator(func):
        for method in methods:
            routes[(path, method.upper())] = func
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator

# === STUB: ORM-like data object ===
class DataOrmObj:
    _id_counter = 1

    def __init__(self, name, value):
        self.id = DataOrmObj._id_counter
        DataOrmObj._id_counter += 1
        self.name = name
        self.value = value

    def update(self, **kwargs):
        self.name = kwargs.get("name", self.name)
        self.value = kwargs.get("value", self.value)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "value": self.value}

# === STUB: Fake DB ===
class FakeDB:
    def __init__(self):
        self.store = {}
    
    def query(self, sql):
        return [{"id": 1, "name": "stub"}]
    
    def add(self, obj):
        self.store[obj.id] = obj
        return obj

    def update(self, obj_id, data):
        obj = self.store.get(obj_id)
        if not obj:
            raise ValueError("Object not found")
        obj.update(**data)
        return obj

    def get(self, obj_id):
        return self.store.get(obj_id)

db = FakeDB()


# === ROUTER EXECUTOR ===
def simulate_request(method, path, body=None):
    req = Request(method, path, body)
    handler = routes.get((path, method.upper()))
    if handler:
        resp = handler(req)
        print(resp.json())
    else:
        print(json.dumps({"error": "404 Not Found", "path": path, "method": method}))

        
# === API Endpoints ===
@endpoint("/api/data", methods=['GET'])
def get_data(req):
    result = db.query("SELECT * FROM dummy")
    return Response(200, result)

@endpoint("/api/echo", methods=['POST'])
def post_echo(req):
    return Response(200, {"echo": req.body})
             

# === TEST ===
simulate_request("POST", "/api/data", {"name": "X", "value": 42})
simulate_request("PUT", "/api/data", {"id": 1, "value": 100})
simulate_request("PUT", "/api/data", {"id": 999, "value": 100})

simulate_request("GET", "/api/data")
simulate_request("POST", "/api/echo", {"msg": "Hello!"})
simulate_request("DELETE", "/api/data")
