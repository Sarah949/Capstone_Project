import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db_drop_and_create_all, setup_db, Actor, Movie
from auth import AuthError, requires_auth
from flask_cors import CORS
import datetime
import jwt

JWT_SECRET = os.environ.get('JWT_SECRET', 'abc123abc1234')


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # Initialize the datbase
    db_drop_and_create_all()

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Controll-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Controll-Allow-Origin', "*")
        response.headers.add('Access-Controll-Allow-Methods',
                             'GET, PUT, POST, DELETE, OPTIONS')
        return response

    @app.route('/')
    def get_greeting():
        # excited = os.environ['EXCITED']
        greeting = "Hello"
        # if excited == 'true': greeting = greeting + "!!!!!"
        return greeting

    '''
    GET /movies
      - require the 'get:movies' permission
      - contain the movie.format() data representation
      - returns status code 200 and
      json {"success": True, "movies": movies_list}
      where movies_list is the list of movies
      or appropriate status code indicating reason for failure
    '''

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies():
        movies = Movie.query.all()
        movies_list = [movie.format() for movie in movies]

        if len(movies) == 0:
            return abort(404)

        return jsonify({
          'success': True,
          'movies': movies_list
        })

    '''
    GET /actors
      - require the 'get:actors' permission
      - contain the actor.format() data representation
      - returns status code 200 and
      json {"success": True, "actors": actors_list}
      where actors_list is the list of actors
      or appropriate status code indicating reason for failure
    '''
    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors():
        actors = Actor.query.all()
        actors_list = [actor.format() for actor in actors]

        if len(actors) == 0:
            return abort(404)

        return jsonify({
          'success': True,
          'actors': actors_list
        })

    '''
    DELETE /movies/<id>
      - where <id> is the existing model id
      - respond with a 404 error if <id> is not found
      - delete the corresponding row for <id>
      - require the 'delete:movies' permission
      - returns status code 200 and
      json {"success": True, "delete": id}
      where id is the id of the deleted record
      or appropriate status code indicating reason for failure
    '''

    @app.route("/movies/<int:id>", methods=["DELETE"])
    @requires_auth("delete:movies")
    def delete_movie(id):
        
        moviequ = Movie.query.filter(Movie.id == id).one_or_none()

        if moviequ is None:
            abort(404)
        try:
            moviequ.delete()

            return jsonify({
              'success': True,
              'deleted': id,
            }), 200

        except:
            abort(422)

    '''
    DELETE /actors/<id>
        - where <id> is the existing model id
        - respond with a 404 error if <id> is not found
        - delete the corresponding row for <id>
        - require the 'delete:actors' permission
        - returns status code 200 and
        json {"success": True, "delete": id}
        where id is the id of the deleted record
        or appropriate status code indicating reason for failure
    '''
    @app.route("/actors/<int:id>", methods=["DELETE"])
    @requires_auth("delete:actors")
    def delete_actor(id):
        
        actorqu = Actor.query.filter(Actor.id == id).one_or_none()

        if actorqu is None:
            abort(404)

        try:  
            actorqu.delete()

            return jsonify({
              'success': True,
              'deleted': id,
            }), 200

        except:
            abort(422)

    '''
    POST /movies
      - create a new row in the movies table
      - require the 'post:movies' permission
      - contain the movie.format() data representation
      - returns status code 200 and
      json {"success": True, "movies": movie}
      where movie is the newly created movie
      or appropriate status code indicating reason for failure
    '''
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie():
        body = request.get_json()

        addtitle = body.get('title', None)
        addrelease = body.get('release_date', None)

        try:
            addmovie = Movie(title=addtitle, release_date=addrelease)
            addmovie.insert()

            moviequ = Movie.query.all()
            movie = [movie.format() for movie in moviequ]

            return jsonify({
                "success": True,
                "movies": movie,
            }), 201
        except:
            abort(422)

    '''
    POST /actors
      - create a new row in the actors table
      - require the 'post:actors' permission
      - contain the actor.format() data representation
      - returns status code 200 and
      json {"success": True, "actors": actor}
      where actor is the newly created actor
      or appropriate status code indicating reason for failure
    '''
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor():
        body = request.get_json()

        addname = body.get('name', None)
        actorAge = body.get('age', 0)
        addgender = body.get('gender', None)

        try:
            addactor = Actor(name=addname, age=actorAge, gender=addgender)
            addactor.insert()

            actors = Actor.query.all()
            actor = [actor.format() for actor in actors]

            return jsonify({
                "success": True,
                "actors": actor,
            }), 201
        except:
            abort(400)

    '''
    PATCH /actors/<id>
      - where <id> is the existing model id
      - respond with a 404 error if <id> is not found
      - update the corresponding row for <id>
      - require the 'patch:actors' permission
      - contain the actor.format() data representation
      - returns status code 200 and
      json {"success": True, "actors": actor}
      where actor is the updated actor
      or appropriate status code indicating reason for failure
    '''
    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def replace_actor(id):
        body = request.get_json()
        

        try:
            actor = Actor.query.filter(Actor.id == id).one_or_none()
            if actor is None:
                abort(404)
            else:
                new_name = body.get('name', actor.name)
                new_gender = body.get('gender', actor.gender)
                new_age = body.get('age', actor.age)
                actor.name = new_name
                actor.gender = new_gender
                actor.age = new_age
                actor.update()

                return jsonify({
                    'success': True,
                    "actors": actor.format(),
                })
        except:
            abort(400)

    '''
    PATCH /movies/<id>
      - where <id> is the existing model id
      - respond with a 404 error if <id> is not found
      - update the corresponding row for <id>
      - require the 'patch:movies' permission
      - contain the movie.format() data representation
      - returns status code 200 and
      json {"success": True, "movies": movie}
      where movie is the updated movie
      or appropriate status code indicating reason for failure
    '''
    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def replace_movie(id):
        body = request.get_json()
        

        try:
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            if movie is None:
                abort(404)
            else:
                new_title = body.get('title', movie.title)
                new_release = body.get('release_date', movie.release_date)
                movie.title = new_title
                movie.release = new_release
                movie.update()

                return jsonify({
                    'success': True,
                    "movies": movie.format(),
                })
        except:
            abort(400)

    # Error Handling

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found",
        }), 404

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error,
        }), 401

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
          "success": False,
          "error": 400,
          "message": "bad request"
          }), 400

    @app.errorhandler(500)
    def bad_request(error):
        return jsonify({
          "success": False,
          "error": 500,
          "message": "internal server error"
          }), 500

    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
