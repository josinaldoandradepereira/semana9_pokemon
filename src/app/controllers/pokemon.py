from flask import Blueprint
from flask.wrappers import Response
from src.app import mongo_client
from bson import json_util

pokemons = Blueprint("pokemons", __name__,  url_prefix="/pokemons")

@pokemons.route("/list_pokemons_generation_one", methods = ["GET"])
def list_pokemons_generation_one():
  pokemons_query = mongo_client.pokemons.aggregate([
    {
        '$match': {
            'Generation': 1
        }
    }, {
        '$lookup': {
            'from': 'combats', 
            'localField': '#', 
            'foreignField': 'Winner', 
            'as': 'winners'
        }
    }, {
        '$project': {
            'Name': 1, 
            'winners': {
                '$size': '$winners'
            }
        }
    }, {
        '$match': {
            'winners': {
                '$gte': 5
            }
        }
    }, {
        '$sort': {
            'winners': -1
        }
    }
  ])

  return Response(
    response=json_util.dumps({'records' : pokemons_query}),
    status=200,
    mimetype="application/json"
  )