Spy Cat Agency API

This is a CRUD application for managing spy cats, their missions, and targets.
The API is built using FastAPI and SQLModel, and allows full management of cats and missions for the Spy Cat Agency (SCA).



Getting Started

1. Clone the Repository
   git clone [https://github.com/your-username/spy-cat-agency.git](https://github.com/your-username/spy-cat-agency.git)
   cd spy-cat-agency


2 Install Required Libraries
pip install fastapi uvicorn sqlmodel requests

fastapi - main framework for API

uvicorn - server to run FastAPI

sqlmodel - database ORM (like SQLAlchemy)

requests - for external API calls (TheCatAPI)




3. Create & Activate Virtual Environment

   Windows (PowerShell):
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   Windows (CMD):
   python -m venv venv
   .\venv\Scripts\activate.bat

4. Install Dependencies
   pip install -r requirements.txt

5. Run the FastAPI Server
   uvicorn main:app --reload

Server will run on: [http://127.0.0.1:8000](http://127.0.0.1:8000)
Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)



API Endpoints

Cats:

GET /cats/ - List all cats
POST /cats/ - Create a new cat
GET /cats/{id} - Get a single cat by ID
PUT /cats/{id}/salary?salary={value} - Update a cat's salary
DELETE /cats/{id} - Remove a cat from the system

Missions:

GET /missions/ - List all missions
POST /missions/ - Create a new mission with targets
GET /missions/{id} - Get a single mission
PUT /missions/{id}/assign_cat/{cat_id} - Assign a cat to a mission
PUT /missions/{id}/complete - Mark a mission as completed
DELETE /missions/{id} - Delete a mission (only if unassigned)

Targets:

GET /targets/{id} - Get a single target
PUT /targets/{id}/notes?notes={text} - Update notes of a target (if not completed)



Postman Collection

The full Postman collection contains all endpoints and ready-to-use request examples.
Download or open it in Postman:

GitHub (raw JSON): ./SpyCatAgency.postman_collection.json
Postman Cloud link: [https://yuramishchuk1703-4465482.postman.co/workspace/%25D0%25AE%25D1%2580%25D0%25B8%25D0%25B9-%25D0%259C%25D0%25B8%25D1%2589%25D1%2583%25D0%25BA's-Workspace~f8c13efc-f516-4ad8-89b8-882b792f0764/collection/48946515-040ecead-33a9-4ca7-bbb7-19d4a3727e77?action=share&source=copy-link&creator=48946515]
Features:

Manage Spy Cats (create, list, update salary, delete)
Manage Missions with 1-3 Targets
Assign Cats to Missions
Track mission and target completion
Notes for targets with automatic freeze when completed
Validation of cat breeds using TheCatAPI



Notes:

FastAPI provides interactive docs at /docs (Swagger UI)
JSON:API style endpoints
All requests/response bodies are validated automatically
Make sure the server is running before using Postman or Apidog



Requirements:

Python 3.11+
FastAPI
SQLModel
Uvicorn
http.client

How to Test:

1. Import SpyCatAgency.postman_collection.json into Postman or Apidog
2. Start server (uvicorn main:app --reload)
3. Use Send button to execute requests
