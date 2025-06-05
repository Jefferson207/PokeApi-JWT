import httpx

async def fetch_pokemon_info(pokemon_list: list[str]):
    results = []

    async with httpx.AsyncClient() as client:
        for name in pokemon_list:
            try:
                # Paso 1: Info básica del Pokémon
                poke_response = await client.get(f"https://pokeapi.co/api/v2/pokemon/{name.lower()}")
                if poke_response.status_code != 200:
                    raise ValueError("Pokémon no encontrado")
                poke_data = poke_response.json()

                types = [t["type"]["name"] for t in poke_data["types"]]
                height = poke_data["height"]
                weight = poke_data["weight"]
                species_url = poke_data["species"]["url"]

                # Paso 2: Obtener URL de la cadena evolutiva
                species_response = await client.get(species_url)
                evolution_chain_url = species_response.json()["evolution_chain"]["url"]

                # Paso 3: Obtener la cadena evolutiva ordenada
                chain_response = await client.get(evolution_chain_url)
                chain_data = chain_response.json()["chain"]

                evolution_chain = []
                current = chain_data
                while current:
                    evolution_chain.append(current["species"]["name"])
                    evolves = current.get("evolves_to")
                    current = evolves[0] if evolves else None

                # Agregar al resultado
                results.append({
                    "name": name.lower(),
                    "height": height,
                    "weight": weight,
                    "types": types,
                    "evolution_chain": evolution_chain
                })

            except Exception:
                results.append({
                    "name": name.lower(),
                    "error": "Pokémon no encontrado"
                })

    return results
