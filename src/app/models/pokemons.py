from src.app.utils import get_validator_json

def create_collection_pokemons(mongo_client):
  pokemons_validator = get_validator_json("validators","pokemon")

  try:
    mongo_client.create_collection("pokemons")
  except Exception as e:
    print(e)

  mongo_client.command("collMod", "pokemons", validator=pokemons_validator)
  