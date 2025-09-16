import requests
import os

def get_api_data(rodada):
    """
    Args:
        rodada: Número da rodada

    Returns:
        Dados da API ou gera exceção se falhar.
    """
    uri = f'https://api.football-data.org/v4/competitions/BSA/matches?matchday={rodada}'
    headers = { 'X-Auth-Token': os.getenv("TOKEN_API_BRASILEIRAO") }

    try:
        response = requests.get(uri, headers=headers, timeout=20)
        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao conectar na API: {e}")
        raise e  
