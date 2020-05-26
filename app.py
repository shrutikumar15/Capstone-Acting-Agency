import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError
from models import setup_db, Movie, Actor
from auth import requires_auth
from auth import AuthError


def create_app(test_config=None):
    
    app = Flask(__name__)
    setup_db(app)
    CORS(app,  resources={'/': {'origins': '*'}})


    @app.route("/")
    def home():
        hiText = "Hi ! I`m Shruti"
        return str(hiText)


    @app.route("/actors", methods=["GET"])
    @requires_auth('get:actors')
    def get_actors(token):
        try:
            actors = Actor.query.all()
            return jsonify({"success": True, "actors": [d.format() for d in actors]}), 200
        except:
            abort(404)


    @app.route("/movies", methods=["GET"])
    @requires_auth('get:movies')
    def get_movies(token):
        try:
            movies = Movie.query.all()
            return jsonify({"success": True, "movies": [d.format() for d in movies]}), 200
        except:
            abort(404)


    @app.route("/actors/create", methods=["POST"])
    @requires_auth('post:actors')
    def create_actor(token):
        try:
            req = request.get_json()
            act = Actor(name=req['name'], gender=req['gender'], age=req['age'])
            act.insert()
            actors = Actor.query.all()
            return jsonify({"success": True, "actors": [d.format() for d in actors]}), 200
        except:
            abort(404)


    @app.route("/movies/create", methods=["POST"])
    @requires_auth('post:movies')
    def create_movie(token):
        try:
            req = request.get_json()
            mov = Movie(title=req['title'], release_date=req['release_date'])
            mov.insert()
            movies = Movie.query.all()
            return jsonify({"success": True, "movies": [d.format() for d in movies]}), 200
        except:
            abort(404)


    @app.route("/actors/<int:id>", methods=["DELETE"])
    @requires_auth('delete:actor')
    def delete_actor(payload, id):
        try:
            actor = Actor.query.filter(Actor.id == id).one_or_none()
            if actor is None:
                abort(404)
            else:
                actor.delete()
                actors = Actor.query.all()
                return jsonify({"success": True, "actors": [d.format() for d in actors]}), 200
        except:
            abort(404)


    @app.route("/movies/<int:id>", methods=["DELETE"])
    @requires_auth('delete:movie')
    def delete_movie(payload, id):
        try:
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            if movie is None:
                abort(404)
            else:
                movie.delete()
                movies = Movie.query.all()
                return jsonify({"success": True, "movies": [d.format() for d in movies]}), 200
        except:
            abort(404)


    @app.route("/actors/<int:id>", methods=["PATCH"])
    @requires_auth('patch:actor')
    def patch_actor(payload, id):
        try:
            actor = Actor.query.filter(Actor.id == id).one_or_none()
            req = request.get_json()
            if('name' in req):
                actor.name = req['name']
            if('gender' in req):
                actor.gender = req['gender']
            if('age' in req):
                actor.age = req['age']
            actor.update()
            actors = Actor.query.all()
            return jsonify({"success": True, "actors": [d.format() for d in actors]}), 200
        except:
            abort(404)


    @app.route("/movies/<int:id>", methods=["PATCH"])
    @requires_auth('patch:movie')
    def patch_movie(payload, id):
        try:
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            req = request.get_json()
            if('title' in req):
                movie.title = req['title']
            if('release_date' in req):
                movie.release_date = req['release_date']
            movie.update()
            movies = Movie.query.all()
            return jsonify({"success": True, "movies": [d.format() for d in movies]}), 200
        except:
            abort(404)


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resourse not found"
        }), 404


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422


    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'code': 405,
            'success': False,
            'message': 'method not allowed'
        }), 405


    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'code': 500,
            'success': False,
            'message': 'server error'
        }), 500


    @app.errorhandler(AuthError)
    def internal_auth_error(error):
        return jsonify({
            'error': error.error,
            'success': False,
            'message': error.status_code
        }), error.status_code
    
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
# Casting Director
# eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ilh0WUI5NUJrYkdYTHdnb0FrV1VMWSJ9.eyJpc3MiOiJodHRwczovL3NocnV0aWt1bWFyLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwMDIxMzEzNzAxOTkwMzkzMjQ5MyIsImF1ZCI6WyJjYXBzdG9uZSIsImh0dHBzOi8vc2hydXRpa3VtYXIuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU5MDUxNzYyMywiZXhwIjoxNTkwNTk2NjIzLCJhenAiOiJkMEFwcU1kQ1dZSElFQ3ZuWlVmWERYM3loaWN0bDZSaiIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9ycyJdfQ.Ghkmd0PtnMhycc0rRjlygXNezTYQ4cT2KOYWrK0WgZjGWo3hSEZgRkDKvcfOh7CWD2S6r1zA1VaQh7ZpukjHebED9X8YHjYnLzzddCjmNvmaLygIjZUGGYskvERqWDoQLwrKqaT8QHBwu36eF9zrgRyVBv1KC7znm32aPhtJx2EUjZykOCp1nwoq3sg1aYACkzhXogIPXxbM1wFJWLNSH0ACnibgk6-9RIQPDEO_JqsnxK5frSH6tjM7bNQVa8RTqD0BnZMLgwckP5RmfPnGBHW7SyZKAmrbV6-rFWQb-uwoHZsULLCTjJIe1Wg7l0MJ9k_HR-EI47SEq4YEiaF-Cg
# Casting Assistant
# eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ilh0WUI5NUJrYkdYTHdnb0FrV1VMWSJ9.eyJpc3MiOiJodHRwczovL3NocnV0aWt1bWFyLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwMTM0MDUyNzExMjgzODI3NjQxOSIsImF1ZCI6WyJjYXBzdG9uZSIsImh0dHBzOi8vc2hydXRpa3VtYXIuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU5MDUxOTgwNywiZXhwIjoxNTkwNTk4ODA3LCJhenAiOiJkMEFwcU1kQ1dZSElFQ3ZuWlVmWERYM3loaWN0bDZSaiIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.L4kV453m6gs3lmgbnuU3gJUYIuBq_M1mBggu8qDpwocuGBXHfMXv25QEjduCFv0P3DIbG78HgYPhpnV2AWo8PeFf4Zb-gOW9rU9GNCKKf1qh_NoI8fjR29eezwkaoNgBvcDR3nEpl-p8M6_Krh5hIF088VifihMarvMVQzIPy-L4Lye8ypX5AMmP6Xyr-6TRijMP0Gwm5pa67HgJ6gzXqYmEWuVU-Yw2INShdRncTQIEI23n2f5nx1uk5lJx74S8Oh1DIdokPUlKjQRAPrhn7fS8WPWic000THoQwafE87VT7dxEeoED8RfkqlaSjX5AaAulJjrvsmOWxm9C8NGYcA
# Executive Producer
# eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ilh0WUI5NUJrYkdYTHdnb0FrV1VMWSJ9.eyJpc3MiOiJodHRwczovL3NocnV0aWt1bWFyLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwODg4OTI5ODA5OTE3Mjg5NjM1NCIsImF1ZCI6WyJjYXBzdG9uZSIsImh0dHBzOi8vc2hydXRpa3VtYXIuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU5MDUxOTg1MywiZXhwIjoxNTkwNTk4ODUzLCJhenAiOiJkMEFwcU1kQ1dZSElFQ3ZuWlVmWERYM3loaWN0bDZSaiIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.mVnZq-k6JBE3qhwVqZNvsd5A6kI4GahLwU2jixXzz3poI_DFzXGbuOX7SlyBOL7JBVmbm0kxn96M389WaBInolHba5XX-0YlJPvo4FDflH__-MYNX6jpDDybd3onYV3_vGjXfB0xfjLFg_n-AKrt-WzQp6s4SVsDA1552NM7G1wOXmpCfAyyMR71qwhY6md-lFnrbC8Po_v8FY-k4QwVGgxlmnEJl6mmUylPBBKQH8DiBuuDw_Q0Vmj7o1gtd10dj6mYFrtX8yjwcdUGwQzX2lnXfLxPb3p3HYlcFmxrlZ2ryyeaYGiJfhkDMyBTFtBDxVZ7JgXgnGwynd646P-P7g
