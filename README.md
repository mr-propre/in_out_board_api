# in_out_board_api
/!\ DISCLAIMER /!\ This API WILL be subject to changes once the API client development has started.

RESTful/CRUD API prototype for the in out board project using FastAPI Python framework.

## Requirements
- Python3.6+
- Python pip
- Python venv
- MongoDB

## Set-Up
- Activate the Python venv (. bin/activate.*).
- Install dependencies with `pip install -r requirements.txt`.
- Create a file named `.env` at the root of the project, it will be used to set the MongoDB connection URI variable. Inside write `MONGO_DETAILS=<your MongoDB connection URI>`.
- Run the Uvicorn server with `python main.py`.

## Usage
By default, the server is running on the 8000 port. You can access the Swagger powered API doc at http://localhost:8000/docs. On this page you can also test the API endpoints, as with Postman.
