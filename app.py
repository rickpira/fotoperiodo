import streamlit as st
import math
import datetime
import pandas as pd
import matplotlib.pyplot as plt

# Configuração inicial da página
st.set_page_config(page_title="Calculadora de Fotoperíodo", layout="centered")
st.title("🧮 Calculadora de Fotoperíodo")

st.markdown("""
Este aplicativo calcula o **fotoperíodo** com base na **latitude** e **data** fornecidas.

- Informe a latitude do local (negativa no Hemisfério Sul)
- Selecione uma data do ano
- Clique em **Calcular** para ver os resultados
""")

# Função de cálculo

def calcular_fotoperiodo_dia(latitude, dia_do_ano):
    declinacao = 23.45 * math.sin(math.radians(360 * (284 + dia_do_ano) / 365))
    lat_rad = math.radians(latitude)
    dec_rad = math.radians(declinacao)
    cos_omega = -math.tan(lat_rad) * math.tan(dec_rad)
    cos_omega = max(min(cos_omega, 1), -1)
    omega = math.acos(cos_omega)
    fotoperiodo = (2 * omega * 24) / (2 * math.pi)
    angulo_horario_graus = math.degrees(omega)
    return round(fotoperiodo, 2), round(declinacao, 2), round(angulo_horario_graus, 2)

def classificar_fotoperiodo(f):
    if f < 11:
        return "curto"
    elif f <= 13:
        return "médio"
    else:
        return "longo"

# Entrada do usuário
latitude = st.number_input("🌍 Latitude (ex: -10.0)", value=-10.0, step=0.1)
data = st.date_input("📅 Data", value=datetime.date(2025, 6, 21))

# Botão principal
if st.button("Calcular fotoperíodo"):
    nda = data.timetuple().tm_yday
    fotoperiodo, declinacao, angulo_horario = calcular_fotoperiodo_dia(latitude, nda)
    classificacao = classificar_fotoperiodo(fotoperiodo)

    st.markdown(f"""
    ### Resultado
    - **Data selecionada:** {data.strftime('%d/%m')}  
    - **NDA:** {nda}  
    - **Declinação solar:** {declinacao} °  
    - **Ângulo horário ao nascer do sol:** {angulo_horario} °  
    - **Fotoperíodo estimado:** {fotoperiodo} horas → **dia {classificacao}**
    """)

# Botões adicionais
st.markdown("---")
st.subheader("📊 Análise Anual")

col1, col2 = st.columns(2)

with col1:
    show_table = st.button("Mostrar Tabela Anual")
with col2:
    show_plot = st.button("Mostrar Gráfico Anual")

# Funções auxiliares

def gerar_dados_anuais(latitude):
    dias = list(range(1, 366))
    resultados = [calcular_fotoperiodo_dia(latitude, d) for d in dias]
    fotoperiodos = [r[0] for r in resultados]
    return dias, fotoperiodos

if show_table:
    dias, fotoperiodos = gerar_dados_anuais(latitude)
    df = pd.DataFrame({"Dia do Ano": dias, "Fotoperíodo (h)": fotoperiodos})
    st.dataframe(df)

if show_plot:
    dias, fotoperiodos = gerar_dados_anuais(latitude)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(dias, fotoperiodos)
    ax.set_title(f"Fotoperíodo anual para latitude {latitude}°")
    ax.set_xlabel("Dia do ano")
    ax.set_ylabel("Fotoperíodo (h)")
    ax.grid(True)
    st.pyplot(fig)
