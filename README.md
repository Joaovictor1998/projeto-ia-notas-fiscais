# 📊 Dashboard de Inteligência Financeira (NFSe) com I.A.

Este projeto é um ecossistema completo para processar Notas Fiscais de Serviço Eletrônicas (NFSe), gerenciar dados financeiros e realizar previsões de faturamento futuro utilizando Machine Learning.

## 🚀 Funcionalidades

- **Extração Automatizada:** Lê arquivos XML de notas fiscais contidos em arquivos ZIP, identificando valores brutos, líquidos e impostos (ISS/INSS).
- **Dashboard Interativo:** Interface web construída com Streamlit para visualização de métricas (KPIs) e gráficos de evolução mensal.
- **Inteligência Artificial:** Modelo de Regressão Linear que analisa o histórico e projeta o faturamento líquido total para o ano de **2026**.
- **Segurança:** Sistema de autenticação via tela de login para proteção de dados sensíveis.
- **Exportação:** Gerador de relatórios em Excel (.xlsx) para facilitar a contabilidade.

## 🛠️ Tecnologias Utilizadas

- **Python 3.11**
- **Pandas:** Manipulação e saneamento de dados.
- **Scikit-Learn:** Treinamento do modelo de Machine Learning.
- **Streamlit:** Criação da interface web.
- **Joblib:** Serialização de modelos e dataframes processados.
- **XML.etree.ElementTree:** Parsing de arquivos fiscais.

## 📋 Como Executar o Projeto

1. **Instale as dependências:**
   ```bash
   pip install streamlit pandas scikit-learn joblib openpyxl

2. Treine o modelo inicial: Execute o script de treinamento para gerar o arquivo .joblib:
    ```bash
    python treinar_previsao.py

3. Inicie o Dashboard:
    ```bash
    streamlit run app.py
