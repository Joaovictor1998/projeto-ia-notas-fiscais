import joblib
import matplotlib.pyplot as plt 


# 1. Carrega os dados que já processamos
df['mes'] = df['Data'].dt.strftime('%Y-%m')
mensal = df.groupby('Mes')[['Valor Bruto', 'Valor Liquido']].sum()


# 3. Cria o gráfico
mensal.plot(kind='bar', figsize=(10, 6), color=['#1f77b4', '#2ca02c'])
plt.title('Faturamento Mensal: Bruto vs Líquido')
plt.xlabel('Mês')
plt.ylabel('Valor (R$)')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()


# Exibe o gráfico
plt.show()
