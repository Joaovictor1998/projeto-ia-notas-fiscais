import joblib
import pandas as pd 
from sklearn.linear_model import LinearRegression
import numpy as np 


# 1. Carregar os dados que você extraiu dos XMLs
df = joblib.load('modelos/dataframe_consolidado.joblib')

# 2. Preparar os dados por mês
df['Mes_Num'] = df['Data'].dt.month
faturamento_mensal = df.groupby('Mes_Num')['Valor Liquido'].sum().reset_index()

# Criamos uma coluna "Lag" (o valor do mês anterior)
faturamento_mensal['Mes_Anterior'] = faturamento_mensal['Valor Liquido'].shift(1)
faturamento_mensal = faturamento_mensal.dropna() # Remove o primeiro mês que não tem anterior


# 3. Definir X (entrada) e y (saída)
x = faturamento_mensal[['Mes_Anterior']]
y = faturamento_mensal['Valor Liquido']


# 4. Treinar o modelo
modelo_previsao = LinearRegression()
modelo_previsao.fit(x, y)


# 5. Salvar o modelo treinado com joblib!
joblib.dump(modelo_previsao, 'modelos/modelo_previsao_financeira.joblib')


print("--- Modelo treinado e salvo com sucesso! ---")

# Fazendo uma previsão simples para o próximo mês
ultimo_valor = faturamento_mensal['Valor Liquido'].iloc[-1]
previsao = modelo_previsao.predict([[ultimo_valor]])

print(f"Com base no último mês (R$ {ultimo_valor:,.2f}),")
print(f"a previsão para o próximo mês é: R$ {previsao[0]:,.2f}")
