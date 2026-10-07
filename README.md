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
flet run src/main.py
```

To execute the client as a web server where each customer can connect in a LAN, use (once in the client folder, inside the virtual enviroment):
```
flet run --web --host 0.0.0.0 --port 8000 src/main.py
```
(for now port 8000 is also hard-coded in some portions of the code, so keep it 8000)

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