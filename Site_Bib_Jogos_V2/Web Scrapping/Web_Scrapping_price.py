from bs4 import BeautifulSoup
import requests
import json
import re

# Parâmetros para adicionar na biblioteca
NAME_JSON_CALL = "the_witcher_3"
TAGS = "<span>Ação e Aventura</span> | <span>Mundo Aberto</span>"
NAME_GAME = "The Witcher 3: Wild Hunt — Remastered"
SINOPSE = "Em The Witcher 3: Wild Hunt, você assume o papel de Geralt de Rívia, um caçador de monstros mercenário em um mundo aberto de fantasia sombria devastado pela guerra. Sua missão mais importante é encontrar Ciri, a Criança da Profecia — uma arma viva capaz de alterar o destino do mundo — enquanto ela é perseguida pela Caçada Selvagem, uma cavalgada espectral de outro reino. Explore cidades mercantes, ilhas piratas e passagens montanhosas perigosas, tome decisões moralmente complexas com consequências duradouras e domine espadas, sinais mágicos e poções para sobreviver."
URL_XBOX = "https://www.xbox.com/pt-br/games/store/the-witcher-3-wild-hunt-remastered/c261457lcnmj"
URL_PLAY = "https://store.playstation.com/pt-br/product/UP4497-PPSA03972_00-00000000000GOTY7"
URL_STEAM = "https://store.steampowered.com/app/292030/The_Witcher_3_Wild_Hunt/"

def pegar_capa_steam(url_loja_steam):
    match = re.search(r"/app/(\d+)", url_loja_steam)
    if not match:
        return ""
    app_id = match.group(1)
    api_url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
    try:
        dados = requests.get(api_url, timeout=10).json()
        if dados[app_id]["success"]:
            return dados[app_id]["data"]["header_image"]
    except Exception as e:
        print(f"Erro ao buscar capa na Steam: {e}")
    return ""

# Link do jogo na web do Xbox
response_xbox = requests.get(URL_XBOX)
soup_xbox = BeautifulSoup(response_xbox.text, "html.parser")

# Link do jogo na web do PlayStation
response_play = requests.get(URL_PLAY)
soup_play = BeautifulSoup(response_play.text, "html.parser")

# Link do jogo na web na Steam
response_steam = requests.get(URL_STEAM)
soup_steam = BeautifulSoup(response_steam.text, "html.parser")

# Parâmetros para identificar seus preços e capa
xbox_price = soup_xbox.select_one('span[class*="Price-module__boldText"]').text.strip().replace('+', '')
play_price = soup_play.find(name="span", class_="psw-t-title-m").text.strip()
steam_raw = soup_steam.find(name="div", class_="game_purchase_price price").text.replace('R$', '').strip()
steam_price = f"R${steam_raw}"
capa_steam = pegar_capa_steam(URL_STEAM)

# Abrindo o arquivo JSON
caminho_dos_arquivos = 'D:/VisualCode/GitHub/Primeiro_Site_Projeto/Versao_2/Search_Bib.py/Bib_jogos_data.json'
with open(caminho_dos_arquivos, 'r', encoding='utf-8') as arquivos:
    dados_json = json.load(arquivos)

# Atualizar as variáveis dentro do dicionário correspondente
for jogo in dados_json['jogos']:
    if jogo['id'] == NAME_JSON_CALL:
        jogo['nome'] = NAME_GAME
        jogo['capa'] = capa_steam
        jogo['tags'] = TAGS
        jogo['sinopse'] = SINOPSE
        jogo['precos']['xbox'] = xbox_price
        jogo['precos']['playstation'] = play_price
        jogo['precos']['steam'] = steam_price
        jogo['site']['xbox'] = URL_XBOX
        jogo['site']['playstation'] = URL_PLAY
        jogo['site']['steam'] = URL_STEAM
        break

with open(caminho_dos_arquivos, 'w', encoding='utf-8') as arquivos:
    json.dump(dados_json, arquivos, indent=4, ensure_ascii=False)

print("Jogo e capa atualizados com sucesso no JSON!")