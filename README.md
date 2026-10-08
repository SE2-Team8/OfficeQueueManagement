# OfficeQueueManagement
The Office Queue Management is a system that manages the queues for desk services open the public (e.g., post office, medical office). In the same office, various counters can handle different types of services (e.g., shipping or accounts management).

### Notes on client venv setup and installation

Flet framework should require python 3.10 or newer to work

To setup the client, just navigate to the client folder and:
- create a virtual enviroment
- activate it
- (once it is active) get all the packages into the venv

On windows, once you are in the correct client folder, it should roughly be:
```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Notes on client execution

To execute the client, use (once in the client folder, inside the virtual enviroment):
```
flet run src/main.py [server_url]
```
server_url can also be directly specified as `server_ip:server_port`. If this argument is not provided, the client will assume that 
the server is running on the same machine, on port 8000. When specified, it should not be 127.0.0.1, localhost nor 0.0.0.0 even if 
the server is running on the same machine as the client, as this url is forwarded to other devices in order to reach the server.

### Notes on server venv setup and initialization

To set up the server, you have to do the same steps done for the client

### Notes on the server architecture

The server is based on a Feature Based Architecture, which means that every feature will have different folders, with the same kind of files inside. These files are:
- `models.py`: it contains the classes of the ORM (SQLAlchemy) which define the database's physic tables.
- `router.py`: it defines the HTTP endpoints for the application.
- `schemas.py`: it utilizes the library Pydantic to define and validate the datas' format which enter and exit the APIs.
- `services.py`: it is the brain of the application, with all the rules and algorithms.

Then there is the file for the database, which it doesn't exist on premise, but will grow iteratively during the project developement, thanks to the `models.py` files.

Finally there is the `main.py` file, which simply works as an assembler of the features' routers.

To execute the server, use (once in the server folder, inside the virtual enviroment):
```
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```