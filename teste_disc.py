import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import sqlite3
import random
import string

def gerar_codigo_acesso():
    """Gera um código único para acesso aos resultados."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

def criar_banco():
    """Cria o banco de dados e a tabela se ainda não existir."""
    conn = sqlite3.connect("disc_test.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resultados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE,
            dominancia REAL,
            influencia REAL,
            estabilidade REAL,
            conformidade REAL
        )
    ''')
    conn.commit()
    conn.close()

def salvar_resultado(codigo, resultado):
    """Salva os resultados no banco de dados."""
    conn = sqlite3.connect("disc_test.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO resultados (codigo, dominancia, influencia, estabilidade, conformidade)
        VALUES (?, ?, ?, ?, ?)
    ''', (codigo, resultado['Dominância'], resultado['Influência'], resultado['Estabilidade'], resultado['Conformidade']))
    conn.commit()
    conn.close()

def aplicar_teste_disc(respostas):
    """
    Processa as respostas do teste DISC e gera um perfil.
    :param respostas: Lista de respostas do teste.
    :return: Dicionário com os resultados DISC.
    """
    categorias = ['Dominância', 'Influência', 'Estabilidade', 'Conformidade']
    resultados = dict.fromkeys(categorias, 0)
    
    pesos = {
        'D': 'Dominância',
        'I': 'Influência',
        'S': 'Estabilidade',
        'C': 'Conformidade'
    }
    
    for r in respostas:
        if r in pesos:
            resultados[pesos[r]] += 1
    
    total = sum(resultados.values())
    if total > 0:
        for k in resultados:
            resultados[k] = round((resultados[k] / total) * 100, 2)
    
    return resultados

def exibir_resultados(df):
    st.write("### Resultados do Teste DISC")
    st.dataframe(df)
    
    fig, ax = plt.subplots()
    ax.bar(df.columns, df.iloc[0], color=['red', 'blue', 'green', 'orange'])
    ax.set_xlabel("Categorias")
    ax.set_ylabel("Porcentagem")
    ax.set_title("Distribuição do Perfil DISC")
    st.pyplot(fig)

def main():
    criar_banco()
    
    st.title("Teste DISC Online")
    st.write("Responda as perguntas e descubra seu perfil DISC")
    
    perguntas = {
        "Quando estou sob pressão, minha tendência é:": ["Ser assertivo e direto (D)", "Ser comunicativo e otimista (I)", "Ser paciente e calmo (S)", "Ser detalhista e analítico (C)"],
        "Em situações sociais, eu geralmente sou:": ["Líder e dominante (D)", "Extrovertido e persuasivo (I)", "Agradável e compreensivo (S)", "Reservado e meticuloso (C)"],
        "Prefiro trabalhar em um ambiente que seja:": ["Competitivo e desafiador (D)", "Interativo e dinâmico (I)", "Estável e previsível (S)", "Estruturado e organizado (C)"],
        "Meu estilo de tomada de decisão é mais:": ["Rápido e firme (D)", "Baseado em intuição e pessoas (I)", "Cauteloso e harmonioso (S)", "Lógico e baseado em dados (C)"],
        "Quando enfrento desafios, minha primeira reação é:": ["Enfrentá-los de frente e com força (D)", "Motivar e influenciar os outros (I)", "Buscar consenso e apoio (S)", "Analisar todas as opções antes de agir (C)"]
    }
    
    respostas = []
    
    for pergunta, opcoes in perguntas.items():
        resposta = st.radio(pergunta, opcoes)
        respostas.append(resposta[-2])  # Pegamos apenas a letra final (D, I, S ou C)
    
    if st.button("Enviar Respostas"):
        resultado_final = aplicar_teste_disc(respostas)
        df_resultado = pd.DataFrame([resultado_final])
        exibir_resultados(df_resultado)
        
        codigo_acesso = gerar_codigo_acesso()
        salvar_resultado(codigo_acesso, resultado_final)
        st.write(f"Seu código de acesso aos resultados: `{codigo_acesso}`")

if __name__ == "__main__":
    main()
