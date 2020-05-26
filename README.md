# Capstone Project
#Casting Agency Specifications
The Casting Agency models a company that is responsible for creating movies and managing as well as assigning actors to those movies. 

No frontend is developed for this app, you can use it using cURL or Postman

## Getting Started

### Installing Dependencies

#### Python 3.7

#### PIP Dependencies

Install dependencies 

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- Flask

- SQLAlchemy

- Postgres

## Running the server
Create the database:
createdb Capstone

To run the server, execute:

```bash
$env:FLASK_APP = "app.py"
flask run 
```
Setting the FLASK_ENV variable to development will detect file changes and restart the server automatically.

## Hosting
This project has been deployed using Heroku and can be found at this URL:  https://capstone-acting-agency.herokuapp.com

## Identity and Auth
Auth0 login: https://auth0.com/

Recieve Token: 
https://shrutikumar.auth0.com/authorize?audience=capstone&response_type=token&client_id=d0ApqMdCWYHIECvnZUfXDX3yhictl6Rj&redirect_uri=http://127.0.0.1:5000

Token check: https://jwt.io/

## Roles
- Base URL: You can run this API locally at the default `http://127.0.0.1:5000/`
- Authentication: This app has 3 users. Each has his own token which are provided in `setup.sh` file. Details about each user privlages are provided below.

#### Casting Assistant
- Can view actors and movies
#### Casting Director
- All permissions a Casting Assistant has and…
- Add or delete an actor from the database
- Modify actors or movies
#### Executive Producer
- All permissions a Casting Director has and…
- Add or delete a movie from the database

## API reference
```bash 
GET - /actors (get:movies) permissions required
  - Fetch all Actors with name, age, gender and id 
	- Request Argument : None
	- Example
    {
    "actors": [
        {
            "age": 38,
            "gender": "male",
            "id": 1,
            "name": "Timothee Chalamet"
        }
     ],
    "success": true
    }
    
GET - /movies (get:movies) permissions required
  - Fetch all Movies with title, release_date and id 
	- Request Argument : None
	- Example
    {
    "movies": [
        {
            "id": 1,
            "release_date": "Sun, 31 Dec 2000 00:00:00 GMT",
            "title": "Harry Potter"
        },
        {
            "id": 2,
            "release_date": "Sun, 31 Dec 2000 00:00:00 GMT",
            "title": "Twilight"
        }
    ],
    "success": true
    }
```
```bash 
POST - /movies/create (post:movies) permission required
  - Creates new Movie
	- Request Argument :   {
            "release_date": "Sun, 31 Dec 2000 00:00:00 GMT",
            "title": "New Moon"
        }
	- Returns : JSON response containing request status
	- Example
        {
    "movies": [
        {
            "id": 1,
            "release_date": "Sun, 31 Dec 2000 00:00:00 GMT",
            "title": "Harry Potter"
        },
        {
            "id": 2,
            "release_date": "Sun, 31 Dec 2000 00:00:00 GMT",
            "title": "New Moon"
        }
    ],
    "success": true
    }
    
POST - /actors/create (post:actors) permission required
  - Creates new Actor
	- Request Argument :   {
            "age": 28,
            "gender": "female",
            "name": "Emma Watson"
        }
	- Returns : JSON response containing request status
	- Example
  {
       "actors": [
        {
            "age": 28,
            "gender": "female",
            "id": 1,
            "name": "Emma Watson"
        }
     ],
    "success": true
    }
```
```bash
PATCH - /movies/<int:id> (patch:movie) permission required
  - Edits existing Movie
	- Request Argument :   {
            "release_date": "Sun, 31 Dec 2000 00:00:00 GMT",
            "title": "New Moon Rising"
        }
	- Returns : JSON response containing request status
	- Example
        {
    "movies": [
        {
            "id": 1,
            "release_date": "Sun, 31 Dec 2000 00:00:00 GMT",
            "title": "Harry Potter"
        },
        {
            "id": 2,
            "release_date": "Sun, 31 Dec 2000 00:00:00 GMT",
            "title": "New Moon Rising"
        }
    ],
    "success": true
    }
    
PATCH - /actors/<int:id> (patch:actor) permission required
  - Edits Existing Actor
	- Request Argument :   {
            "age": 27,
            "gender": "female",
            "name": "Emma Stone"
        }
	- Returns : JSON response containing request status
	- Example
       "actors": [
        {
            "age": 27,
            "gender": "female",
            "id": 1,
            "name": "Emma Stone"
        }
     ],
    "success": true
    }
```
```bash
DELETE - /actors/<int:id> (delete:actor) permission required
  - Deletes existing Actor by taking ID
  - Returns : JSON response containing request status
  - Example
  {
       "actors": [
        {
            "age": 28,
            "gender": "female",
            "id": 1,
            "name": "Emma Watson"
        }
     ],
    "success": true
    }
   
DELETE- /movies/<int:id> (delete:movie) permission required
  - Deletes existing Movie by taking ID
  - Returns : JSON response containing request status
  - Example
  {
    "movies": [
        {
            "id": 2,
            "release_date": "Sun, 31 Dec 2000 00:00:00 GMT",
            "title": "New Moon"
        }
    ],
    "success": true
    }
```
# Testing
Testing with unittest library
```bash
drop database capstone_test
create database capstone_test
python test_app.py
```
