import httpx
from httpx import HTTPStatusError, RequestError

async def fetch_pokemon_info(pokemon_list: list[str]):
    results = []

    async with httpx.AsyncClient() as client:
        for name in pokemon_list:
            try:
                # Paso 1: Info básica del Pokémon
                poke_response = await client.get(f"https://pokeapi.co/api/v2/pokemon/{name.lower()}")
                poke_response.raise_for_status()
                poke_data = poke_response.json()

                types = [t["type"]["name"] for t in poke_data["types"]]
                height = poke_data["height"]
                weight = poke_data["weight"]
                species_url = poke_data["species"]["url"]

                # Paso 2: Obtener URL de la cadena evolutiva
                species_response = await client.get(species_url)
                species_response.raise_for_status()
                evolution_chain_url = species_response.json()["evolution_chain"]["url"]

                # Paso 3: Obtener la cadena evolutiva ordenada
                chain_response = await client.get(evolution_chain_url)
                chain_response.raise_for_status()
                chain_data = chain_response.json()["chain"]

                if "species" not in chain_data:
                    raise KeyError("La estructura de evolución es inválida")

                evolution_chain = []
                current = chain_data
                while current:
                    evolution_chain.append(current["species"]["name"])
                    evolves = current.get("evolves_to")
                    current = evolves[0] if evolves else None

                results.append({
                    "name": name.lower(),
                    "height": height,
                    "weight": weight,
                    "types": types,
                    "evolution_chain": evolution_chain
                })

            except HTTPStatusError as http_err:
                results.append({
                    "name": name.lower(),
                    "error": f"Error HTTP: {http_err.response.status_code}"
                })
            except RequestError:
                results.append({
                    "name": name.lower(),
                    "error": "Error de conexión con la PokeAPI"
                })
            except KeyError:
                results.append({
                    "name": name.lower(),
                    "error": "Error al procesar datos de evolución"
                })
            except Exception as e:
                results.append({
                    "name": name.lower(),
                    "error": f"Error inesperado: {str(e)}"
                })

    return results