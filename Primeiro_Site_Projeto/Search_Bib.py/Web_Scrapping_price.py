from bs4 import BeautifulSoup
import requests
import json

#link do jogo na web do play
response_play = requests.get("https://store.playstation.com/pt-br/product/UP6312-PPSA28038_00-0375433414453693")
website_play = response_play.text
soup_play = BeautifulSoup(website_play, "html.parser")

#link do jogo na web so xbox
response_xbox = requests.get("https://www.xbox.com/pt-br/games/store/halo-campaign-evolved-standard-edition/9n6j4rnfpkkl")
website_xbox = response_xbox.text
soup_xbox = BeautifulSoup(website_xbox, "html.parser")

#link do jogo na web na steam
response_steam = requests.get("https://store.steampowered.com/app/2806050/Halo_Campaign_Evolved/")
website_steam = response_steam.text
soup_steam = BeautifulSoup(website_steam, "html.parser")

#Parametros para identificar seus preços
play_price = soup_play.find(name="span", class_="psw-t-title-m").text
xbox_price = soup_xbox.select_one('span[class*="Price-module__boldText"]').text.strip().replace('+', '')
steam_price = f"R${soup_steam.find(name="div", class_="game_purchase_price price").text.replace('R$', '').strip()}"

#Atualiza a sinopse
sinopse_atualizada = "Halo: Campaign Evolved é um remake completo da campanha do primeiro jogo da franquia, reconstruído do zero na Unreal Engine 5 para celebrar os 25 anos da série. A história acompanha o supersoldado Master Chief e sua inteligência artificial Cortana após um pouso forçado em um misterioso mundo em forma de anel conhecido como Halo. Enquanto lutam contra as forças alienígenas da aliança Covenant para resgatar sobreviventes da nave Pillar of Autumn, a dupla descobre um segredo mortal escondido na estrutura que ameaça destruir toda a vida na galáxia. Além de modernizar os gráficos, a jogabilidade e as cenas cinematográficas das dez missões originais, o jogo adiciona três fases inéditas que funcionam como prólogo ao lado do Sargento Johnson e oferece modo cooperativo para até quatro jogadores."

#Abrindo o arquivo json para conferir si as variaveis existem para substituilas
caminho_dos_arquivos = 'D:/VisualCode/GitHub/Primeiro_Site_Projeto/Search_Bib.py/Bib_jogos_data.json'
with open(caminho_dos_arquivos, 'r', encoding='utf-8') as arquivos:
    dados_json = json.load(arquivos)

# 2. Atualizar as variáveis dentro do dicionário correspondente
for jogo in dados_json['jogos']:
    if jogo['id'] == 'halo': 
        # Atualiza os valores com as suas variáveis raspadas
        jogo['sinopse'] = sinopse_atualizada
        jogo['precos']['xbox'] = xbox_price
        jogo['precos']['playstation'] = play_price
        jogo['precos']['steam'] = steam_price
        break 

with open(caminho_dos_arquivos, 'w', encoding='utf-8') as arquivos:
    json.dump(dados_json, arquivos, indent=4,  ensure_ascii=False)

print("Preços atualizados com sucesso no JSON!")