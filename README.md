# 🌿 Calculadora de Emissão de CO₂

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![VSCode](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)

Uma aplicação web completa (Monolítica) desenvolvida para calcular e comparar as emissões de dióxido de carbono (CO₂) de diferentes meios de transporte em viagens intermunicipais. O projeto visa promover a conscientização ambiental, permitindo que os usuários compreendam o impacto de suas escolhas de mobilidade e descubram o custo para compensar essas emissões através de Créditos de Carbono.

---

## ✨ Funcionalidades

* **Cálculo de Distância Automatizado:** Integração com a API pública **OSRM** para buscar a distância real de rodovias entre duas cidades.
* **Sistema de Alta Disponibilidade (Fallback):** Caso a API externa falhe, a aplicação possui um "Plano B" que calcula a distância geodésica (linha reta) entre as coordenadas usando a biblioteca `geopy`, acrescida de uma margem de segurança para simular curvas de estradas.
* **Múltiplos Modais:** Cálculo baseado em fatores de emissão específicos para Bicicleta (0kg/km), Ônibus, Carro e Caminhão.
* **Comparativo Inteligente:** O sistema utiliza o Carro como *baseline* (100%) para demonstrar a economia (em kg e em porcentagem) ao optar por modais mais limpos.
* **Créditos de Carbono:** Estimativa automática de quantos créditos são necessários para neutralizar a viagem e o custo financeiro aproximado dessa ação.

---

## 🏗️ Arquitetura e Estrutura do Projeto

O projeto segue a separação de responsabilidades (MVC adaptado para Flask), isolando regras de negócio no backend e lógica de interface no frontend puro, sem a necessidade de frameworks Javascript complexos.
```text
calculadora_co2/
│
├── app.py                 # Lógica de rotas, fallback e cálculo de emissões (Backend)
├── requirements.txt       # Dependências do projeto
│
├── static/                # Arquivos estáticos servidos pelo Flask
│   ├── css/
│   │   └── style.css      # Estilização visual (Flexbox, Grid, UI baseada em Cards)
│   └── js/
│       └── main.js        # Consumo assíncrono da API interna e manipulação do DOM
│
└── templates/             
    └── index.html         # Estrutura da interface
```

---

## 🚀 Como executar o projeto localmente
Siga os passos abaixo para rodar a aplicação na sua máquina:

### 1. Pré-requisitos
Certifique-se de ter o Python 3.8+ instalado na sua máquina.

### 2. Clonar e preparar o ambiente

Abra o seu terminal e execute os comandos:

Clone o repositório (substitua pela sua URL caso suba para o GitHub)
```bash
git clone [https://github.com/andersonnrc/bootcamp-ciandt-CalculadoraCO2.git](https://github.com/andersonnrc/bootcamp-ciandt-CalculadoraCO2.git)
```

Entre na pasta do projeto
```bash
cd bootcamp-ciandt-CalculadoraCO2
```

Crie um ambiente virtual para isolar as bibliotecas
```bash
python3 -m venv .calculadoraco2
```
Ative o ambiente virtual

No Linux/macOS:
```bash
source .calculadoraco2/bin/activate
```
No Windows:
```bash
.calculadoraco2u\Scripts\activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Rodar o servidor Flask
```bash
python app.py
```

A aplicação estará disponível no seu navegador no endereço: http://127.0.0.1:5000.

---

## 💻 Como Utilizar
##### 1. Insira a Origem (ex: Porto Alegre) e o Destino (ex: São Paulo).
##### 2. Opcionalmente, marque a caixa de inserir a distância manualmente caso já saiba a quilometragem exata.
##### 3. Escolha o Meio de Transporte clicando no card correspondente.
##### 4. Clique em Calcular Emissão e visualize os relatórios de impacto ambiental!

![](/images/app.png "Resultado após o cálculo da emissão de CO₂")

---

## 👨‍💻 Contato

[Linkedin](https://www.linkedin.com/in/anderson-ribeiro-carvalho)
