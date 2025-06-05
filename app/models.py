from pydantic import BaseModel
from typing import List

class LoginInput(BaseModel):
    username: str
    password: str

class PokemonRequest(BaseModel):
    pokemons: List[str]
