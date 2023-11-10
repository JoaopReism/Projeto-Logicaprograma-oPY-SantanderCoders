""""""
from fastapi import FastAPI

app = FastAPI()


def calcular_vpl(valor, taxa, ano):
    """"""
    return valor / (1 + taxa)**ano


def comprar_vs_alugar(aluguel, valor_imovel, taxa_juros_imovel, taxa_juros_aluguel, taxa_juros_aplicacao, anos):
    """"""
    # Fluxos de caixa para comprar o imóvel
    fluxo_caixa_compra = []
    valor_imovel_atualizado = valor_imovel
    for _ in range(1, anos+1):
        lucro = valor_imovel_atualizado * taxa_juros_imovel
        valor_imovel_atualizado += lucro
        fluxo_caixa_compra.append(lucro)

    # Fluxos de caixa para alugar o imóvel
    fluxo_caixa_aluguel = []
    aluguel_atualizado = aluguel
    valor_aplicado_atualizado = valor_imovel
    for _ in range(1, anos+1):
        lucro = valor_aplicado_atualizado * taxa_juros_aplicacao
        valor_ano_aluguel = 12*aluguel_atualizado
        lucro_real = lucro-valor_ano_aluguel
        fluxo_caixa_aluguel.append(lucro_real)
        valor_aplicado_atualizado += lucro_real
        aluguel_atualizado *= (1+taxa_juros_aluguel)

    # Cálculo do VPL para comprar o imóvel
    lista_vpl_compra = [calcular_vpl(valor, taxa_juros_aplicacao, ano)
                        for ano, valor in enumerate(fluxo_caixa_compra)]

    # Cálculo do VPL para alugar o imóvel
    lista_vpl_aluguel = [calcular_vpl(valor, taxa_juros_aplicacao, ano)
                         for ano, valor in enumerate(fluxo_caixa_aluguel)]

    resultado = {}
    for i in range(anos):
        vpl_compra = sum([lista_vpl_compra[x] for x in range(i+1)])
        vpl_aluguel = sum([lista_vpl_aluguel[x] for x in range(i+1)])
        if vpl_compra > vpl_aluguel:
            resultado[f"ano {i+1}"] = "COMPRAR"
        else:
            resultado[f"ano {i+1}"] = "ALUGAR"
    return resultado

# Exemplo de uso da calculadora


@app.get('/aluguelvscompra/{aluguel_mensal}/{valor_do_imovel}/{taxa_juros_imovel}/{taxa_juros_aluguel_anual}/{taxa_juros_aplicacao_anual}/{anos}')
def check_resultado(aluguel_mensal: float,
                    valor_do_imovel: float,
                    taxa_juros_imovel: float,
                    taxa_juros_aluguel_anual: float,
                    taxa_juros_aplicacao_anual: float,
                    anos: int):
    """Verifica se é mais rentável comprar ou alugar o imóvel"""
    resultado = comprar_vs_alugar(aluguel_mensal, valor_do_imovel,
                                  taxa_juros_imovel, taxa_juros_aluguel_anual, taxa_juros_aplicacao_anual, anos)
    return resultado
