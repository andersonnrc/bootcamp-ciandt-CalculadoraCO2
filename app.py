from flask import Flask, request, jsonify, render_template
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import requests

app = Flask(__name__)

# Fatores de emissão em kg CO2 por km
FATORES_EMISSAO = {
    'bicicleta': 0.0,
    'onibus': 0.089,
    'carro': 0.12,
    'caminhao': 0.96
}

PRECO_CREDITO_CARBONO = 100.00 # R$ por tonelada


def obter_coordenadas(cidade):
    # Alterado para um user_agent mais único para evitar bloqueios do Nominatim
    geolocator = Nominatim(user_agent="calculadora_co2_bootcamp_ciandt")
    try:
        location = geolocator.geocode(cidade, timeout=10)
        if location:
            return location.longitude, location.latitude
    except Exception as e:
        print(f"Erro ao buscar coordenadas para {cidade}: {e}")
    return None, None


def calcular_distancia_api(origem, destino):
    lon_orig, lat_orig = obter_coordenadas(origem)
    lon_dest, lat_dest = obter_coordenadas(destino)
    
    if not (lon_orig and lon_dest):
        print("Coordenadas não encontradas para uma das cidades.")
        return None
        
    url = f"http://router.project-osrm.org/route/v1/driving/{lon_orig},{lat_orig};{lon_dest},{lat_dest}?overview=false"
    
    try:
        resposta = requests.get(url, timeout=5)
        
        if resposta.status_code == 200:
            dados = resposta.json()
            if dados.get('code') == 'Ok':
                distancia_km = dados['routes'][0]['distance'] / 1000
                print("Distância calculada via API OSRM.")
                return round(distancia_km, 2)
        else:
            print(f"API OSRM indisponível (Status {resposta.status_code}). Acionando Fallback...")
            
    except Exception as e:
        print(f"Erro na requisição OSRM: {e}. Acionando Fallback...")
        
    # ==========================================
    # PLANO B: Cálculo Geodésico (Linha Reta + Margem)
    # ==========================================
    coord_orig = (lat_orig, lon_orig)
    coord_dest = (lat_dest, lon_dest)
    
    # Calcula a distância em linha reta em km
    distancia_reta = geodesic(coord_orig, coord_dest).kilometers
    
    # Adiciona 20% para aproximar a distância real de rodovias
    distancia_estimada = distancia_reta * 1.2
    print(f"Distância estimada via Geopy (Linha reta + 20%): {distancia_estimada} km")
    
    return round(distancia_estimada, 2)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calcular', methods=['POST'])
def calcular():
    dados = request.json
    origem = dados.get('origem')
    destino = dados.get('destino')
    distancia = dados.get('distancia')
    transporte_selecionado = dados.get('transporte', 'carro')

    # Se a distância não foi preenchida manualmente, busca na API
    if not distancia:
        distancia = calcular_distancia_api(origem, destino)
        if not distancia:
            return jsonify({'erro': 'Não foi possível calcular a distância. Tente inserir manualmente.'}), 400
    else:
        distancia = float(distancia)

    # Calcula emissão de todos para o quadro de comparação
    emissoes = {}
    for meio, fator in FATORES_EMISSAO.items():
        emissoes[meio] = round(distancia * fator, 2)

    emissao_selecionada = emissoes[transporte_selecionado]
    emissao_carro = emissoes['carro']
    
    # Lógica de economia vs Carro
    economia_kg = round(emissao_carro - emissao_selecionada, 2)
    percentual_vs_carro = round((emissao_selecionada / emissao_carro) * 100, 2) if emissao_carro > 0 else 0

    # Lógica de Créditos de Carbono
    creditos_necessarios = emissao_selecionada / 1000
    custo_estimado = creditos_necessarios * PRECO_CREDITO_CARBONO

    resultado = {
        'rota': f"{origem} → {destino}",
        'distancia': distancia,
        'meio_transporte': transporte_selecionado.capitalize(),
        'emissao_total_kg': emissao_selecionada,
        'economia_kg': economia_kg if economia_kg > 0 else 0,
        'percentual_vs_carro': percentual_vs_carro,
        'comparacao': emissoes,
        'creditos': {
            'necessarios': round(creditos_necessarios, 4),
            'custo_estimado': round(custo_estimado, 2)
        }
    }
    
    return jsonify(resultado)


if __name__ == '__main__':
    app.run(debug=True)
