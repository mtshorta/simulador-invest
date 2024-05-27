import pandas as pd
import numpy as np
import streamlit as st
import altair as alt


st.set_page_config(layout="wide", page_title='Simulador de investimentos')

st.sidebar.header('Desenvolvido por :green[Mateus Horta]')
st.sidebar.link_button("Portfolio", "https://mateushorta.com/", use_container_width=True)
st.sidebar.link_button("Instagram", "https://www.instagram.com/mtshorta/", use_container_width=True)
st.sidebar.link_button("Linkedin",  "https://www.linkedin.com/in/mateus-horta/", use_container_width=True)
st.sidebar.link_button("Github",    "https://github.com/mtshorta", use_container_width=True)
st.sidebar.divider()
st.sidebar.text('Caso tenha interesse em uma plataforma \npara fazer a gestão completa da sua \ncarteira de investimento e automatizar \nos dados do seu imposto de renda \nconheça o DOMU')
st.sidebar.link_button("Contrate o DOMU",    "https://hotm.art/matdomu", use_container_width=True)



st.title('Simulação de evolução patrimonial 💰')
col1, col2 = st.columns(2)
inicial    = col1.number_input('Valor Inicial', min_value = 0, value = 1000)
aportes    = col2.number_input('Aporte Mensal', min_value = 0, value = 1000)
juros      = col1.number_input(label='Juros mensal %',step=1.,format="%.2f", value = 0.75)
periodo    = col2.number_input('Período em Meses', min_value = 0, max_value=500, value = 240)


#As colunas são MÊS, JUROS, TOTAL INVESTIDO, TOTAL JUROS, TOTAL ACUMULADO
df = pd.DataFrame(0, range(periodo+1), columns = ['Juros', 'Total Investido', 'Total Juros','Total Acumulado'])


#Ajustando o valor inicial para o valor informado
df.index.name = 'Mês'
df.reset_index(inplace=True)

df.at[0, 'Total Investido'] = inicial
df.at[0, 'Total Acumulado'] = inicial

def roundster (x):
     return "{:.2f}".format(x)
#pd.options.display.float_format = '{:.2f}'.format
for i in range(1, periodo+1):
    df['Juros'][i] = roundster(df['Total Acumulado'][i-1]*juros/100)
    df['Total Investido'][i] = inicial + (i * aportes)
    df['Total Juros'][i] = float(df['Juros'][i]) + float(df['Total Juros'][i-1])
    df['Total Acumulado'][i] = df['Total Investido'][i] + df['Total Juros'][i]


#ANOTHER WAY OF MAKING THE DF
#for i in range(1, periodo+1):
#     df.at[i, 'Juros'] = df.at[i-1, 'Total Acumulado'] * juros / 100
#     df.at[i, 'Total Investido'] = inicial + (i * aportes)
#     df.at[i, 'Total Juros'] = df.at[i, 'Juros'] + df.at[i-1, 'Total Juros']
#     df.at[i, 'Total Acumulado'] = df.at[i, 'Total Investido'] + df.at[i, 'Total Juros']
    


st.divider()
#Display dos resultados
st.subheader('Resultado')

def format_brl(x):
     return f"R${x:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")

col1, col2, col3 = st.columns(3)
col1.metric('Valor total Final', format_brl(df.at[periodo, 'Total Acumulado']))
col2.metric('Valor investido', format_brl(df.at[periodo, 'Total Investido']))
col3.metric('Valor em juros', format_brl(df.at[periodo, 'Total Juros']))

st.divider()


st.subheader('Tabela de dados')
st.dataframe(df, height=500)

st.divider()

# #Formatting BRL THIS WILL FUCKUP THE REST OF THE CODE WHEN I NEED CALCULATIONS
# def format_brl(x):
#      return f"R${x:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
# # Applying the custom formatting function to relevant columns
# df['Juros'] = df['Juros'].apply(format_brl)
# df['Total Investido'] = df['Total Investido'].apply(format_brl)
# df['Total Juros'] = df['Total Juros'].apply(format_brl)
# df['Total Acumulado'] = df['Total Acumulado'].apply(format_brl)





# Prepare data for Altair chart
df_melted = df.melt(id_vars='Mês', value_vars=['Total Investido', 'Total Juros'], 
                    var_name='Tipo', value_name='Valor')

# Create the stacked bar chart with custom order for the stack
bar_chart = alt.Chart(df_melted).mark_bar().encode(
    x=alt.X('Mês:O', title='Mês'),
    y=alt.Y('Valor:Q', title='Valor (R$)', stack='zero'),
    color=alt.Color('Tipo:N', title='Tipo', sort=['Total Investido', 'Total Juros']),
    order=alt.Order('key:N',sort='descending'),
    tooltip=['Mês', 'Tipo', 'Valor']
).properties(
    title='Evolução Patrimonial - Total Investido vs Total Juros',
    width=800,
    height=400
)

def roundster (x):
     return "{:.2f}".format(x)

# Create DataFrame for pie chart
pie_data = pd.DataFrame({
    'Tipo': ['Total Juros', 'Total Investido'],
    'Valor': [roundster(df.at[periodo, 'Total Juros']), df.at[periodo, 'Total Investido']]
})
# Create the pie chart
pie_chart = alt.Chart(pie_data).mark_arc().encode(
    theta = 'Valor',
    color = 'Tipo'
).properties(
    title='Evolução Patrimonial - Total Investido vs Total Juros',
    width=500,
    height=300
)


# Display the charts in Streamlit

st.altair_chart(pie_chart, use_container_width=True)
st.altair_chart(bar_chart, use_container_width=True)
