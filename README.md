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