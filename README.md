# Capstone Project
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies.

### Installing Dependencies 

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/starter` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

# Casting Agency Specifications
## Models

    Movies with attributes title and release date
    Actors with attributes name, age and gender

## Endpoints

    GET /actors and /movies
    DELETE /actors/ and /movies/
    POST /actors and /movies and
    PATCH /actors/ and /movies/

## Roles

    Casting Assistant
        Can view actors and movies
    Casting Director
        All permissions a Casting Assistant has and…
        Add or delete an actor from the database
        Modify actors or movies
    Executive Producer
        All permissions a Casting Director has and…
        Add or delete a movie from the database

## Tests

    One test for success behavior of each endpoint
    One test for error behavior of each endpoint
    At least two tests of RBAC for each role

# API Reference
## Endpoints

GET '/movies'
- Fetches a list of movies.
- Requires the 'get:movies' permission
- Request Arguments: None
- Returns: list of movies.
{
    "movies": [
        {
            "id": 1,
            "release_date": "Thu, 11 Mar 2021 21:00:00 GMT",
            "title": "Yes Day"
        }
    ],
    "success": true
}



GET '/actors'
- Fetches a list of actors.
- Requires the 'get:actors' permission
- Request Arguments: None
- Returns: list of actors
- Sample: 
{
    "actors": [
        {
            "age": 49,
            "gender": "Female",
            "id": 1,
            "name": "Jennifer Garner"
        }
    ],
    "success": true
}


POST '/actors'

- Require the post:actors permission
- Create a new row in the actors table
- Contain the actor.get_actor data representation returns status code 200 and json {"success": True, "actors": actor} where actor an array containing only the newly created actor or appropriate status code indicating reason for failure

Here is a returned sample fromat

{
  "actors": [
    {
      "age": 24,
      "gender": "Female",
      "id": 1,
      "name": "Actor Name"
    }
  ],
  "success": true
}


POST '/movies'

- Require the post:movies permission
- Create a new row in the movies table
- Contain the movie.get_movie data representation returns status code 200 and json {"success": True, "movies": movie} where movie an array containing only the newly created movie or appropriate status code indicating reason for failure.

Here is a result sample format:

{
  "movies": [
    {
      "id": 1,
      "release_date": "Thu, 14 May 2021 14:02:13 GMT",
      "title": "Movie Name"
    }
  ],
  "success": true
}

PATCH '/actors/<id>'

- Require the 'patch:actors' permission
- Update an existing row in the actors table
- Contain the actor.get_actor data representation returns status code 200 and json {"success": True, "actors": actor} where actor an array containing only the updated actor or appropriate status code indicating reason for failure

He is a sample for a modified actor in a format:

{
  "actors": [
    {
      "age": 49,
      "gender": "female",
      "id": 1,
      "name": "Actor updated name"
    }
  ],
  "success": true
}

PATCH '/movies/<id>'

- Require the patch:movies permission
- Update an existing row in the movies table
- Contain the movie.format data representation returns status code 200 and json {"success": True, "movies": movie} where movie an array containing only the updated movie or appropriate status code indicating reason for failure

Here is an example of the modified movie in a format:

{
  "movies": [
    {
      "id": 1,
      "release_date": "Thu, 14 May 2021 17:02:13 GMT",
      "title": "Updated Movie Info"
    }
  ],
  "success": true
}

DELETE '/actors/<id>'

- Require the delete:actors permission
- Delete the corresponding row for <id> where <id> is the existing model id
- Respond with a 404 error if <id> is not found
- Returns status code 200 and json {"success": True} where id is the id of the deleted record or appropriate status code indicating reason for failure

return jsonify({
    "success": True,
    "deleted": id
})

DELETE /movies/<movie_id>

- Require the delete:movies permission
- Delete the corresponding row for <id> where <id> is the existing model id
- Respond with a 404 error if <id> is not found
- Returns status code 200 and json {"success": True, "deleted": id} where id is the id of the deleted record or appropriate status code indicating reason for failure

return jsonify({
    "success": True,
    "deleted": id
})