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

@pokemons.route("/list_pokemons_winner_than_seven", methods = ["GET"])
def list_pokemons_winner_than_seven():
  pokemons_query = mongo_client.pokemons.aggregate([
    {
        '$lookup': {
            'from': 'combats', 
            'as': 'winners', 
            'let': {
                'id_pokemon': '$#'
            }, 
            'pipeline': [
                {
                    '$match': {
                        '$expr': {
                            '$and': [
                                {
                                    '$eq': [
                                        '$Winner', '$$id_pokemon'
                                    ]
                                }, {
                                    '$or': [
                                        {
                                            '$eq': [
                                                '$First_pokemon', 7
                                            ]
                                        }, {
                                            '$eq': [
                                                '$Second_pokemon', 7
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                }
            ]
        }
    }, {
        '$project': {
            '#': 1, 
            'Name': 1, 
            'winners': {
                '$size': '$winners'
            }
        }
    }, {
        '$match': {
            '#': {
                '$ne': 7
            }, 
            'winners': {
                '$gte': 1
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

@pokemons.route("/list_pokemon_type_fire_alphabetically", methods = ["GET"])
def list_pokemon_type_fire_alphabetically():
  pokemons_query = mongo_client.pokemons.aggregate([
    {
        '$match': {
            'Type 1': 'Fire', 
            'Type 2': None
        }
    }, {
        '$sort': {
            'Name': 1
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
            'Type 1': 1, 
            'winners': {
                '$size': '$winners'
            }
        }
    }
  ])
  
  return Response(
    response=json_util.dumps({'records' : pokemons_query}),
    status=200,
    mimetype="application/json"
  )
