document.getElementById('checkManual').addEventListener('change', function() {
    const inputDistancia = document.getElementById('distancia');
    inputDistancia.disabled = !this.checked;
    if(this.checked) {
        inputDistancia.focus();
    } else {
        inputDistancia.value = ''; // Limpa se desmarcar
    }
});

async function calcularEmissao() {
    const origem = document.getElementById('origem').value;
    const destino = document.getElementById('destino').value;
    const transporte = document.querySelector('input[name="transporte"]:checked').value;
    const isManual = document.getElementById('checkManual').checked;
    const distancia = isManual ? document.getElementById('distancia').value : null;

    if (!origem || !destino) {
        alert("Por favor, preencha a origem e o destino.");
        return;
    }

    // Altera o texto do botão para mostrar processamento
    const btn = document.querySelector('.btn-calcular');
    const textoOriginal = btn.innerText;
    btn.innerText = "A calcular...";
    btn.disabled = true;

    const dados = { origem, destino, transporte, distancia };

    try {
        const resposta = await fetch('/calcular', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });

        const resultado = await resposta.json();

        if (resposta.ok) {
            // Preenche os dados
            document.getElementById('resRota').innerText = resultado.rota;
            document.getElementById('resDistancia').innerText = resultado.distancia;
            document.getElementById('resTransporte').innerText = resultado.meio_transporte;
            document.getElementById('resEmissao').innerText = resultado.emissao_total_kg.toFixed(2).replace('.', ',');
            
            // Trata a economia
            const cardEconomia = document.getElementById('cardEconomia');
            if(resultado.economia_kg > 0) {
                cardEconomia.style.display = 'block';
                document.getElementById('resEconomiaKg').innerText = `${resultado.economia_kg.toFixed(2).replace('.', ',')} kg`;
                document.getElementById('resEconomiaPerc').innerText = `${(100 - resultado.percentual_vs_carro).toFixed(2).replace('.', ',')}% menos emissões que um carro`;
            } else {
                cardEconomia.style.display = 'none';
            }

            // Créditos
            document.getElementById('resCreditos').innerText = resultado.creditos.necessarios.toFixed(4).replace('.', ',');
            document.getElementById('resCusto').innerText = resultado.creditos.custo_estimado.toFixed(2).replace('.', ',');
            
            // Tabela de Comparação
            const lista = document.getElementById('listaComparacao');
            lista.innerHTML = '';
            const icones = {'bicicleta': '🚲', 'carro': '🚗', 'onibus': '🚌', 'caminhao': '🚚'};
            
            for (const [meio, emissao] of Object.entries(resultado.comparacao)) {
                let percVsCarro = (emissao / resultado.comparacao['carro']) * 100;
                if(resultado.comparacao['carro'] === 0) percVsCarro = 0;

                const item = document.createElement('div');
                item.className = 'comparison-item';
                item.innerHTML = `
                    <div>
                        <strong>${icones[meio]} ${meio.charAt(0).toUpperCase() + meio.slice(1)}</strong>
                        <br><span style="color: #666; font-size: 12px;">vs Carro: ${percVsCarro.toFixed(2).replace('.', ',')}%</span>
                    </div>
                    <div style="font-weight: bold; text-align: right;">
                        ${emissao.toFixed(2).replace('.', ',')} kg CO₂
                    </div>
                `;
                lista.appendChild(item);
            }

            document.getElementById('resultados').style.display = 'block';
        } else {
            alert(resultado.erro || "Ocorreu um erro ao calcular.");
        }
    } catch (erro) {
        console.error("Erro:", erro);
        alert("Erro ao comunicar com o servidor. O OSRM pode estar offline.");
    } finally {
        btn.innerText = textoOriginal;
        btn.disabled = false;
    }
}