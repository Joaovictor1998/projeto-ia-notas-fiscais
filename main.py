import zipfile
import xml.etree.ElementTree as ET
import pandas as pd
import os
import joblib

def processar_notas_zip(caminho_zip):
    dados = []
    
    with zipfile.ZipFile(caminho_zip, 'r') as z:
        arquivos_xml = [f for f in z.namelist() if f.endswith('.xml')]
        
        for arquivo in arquivos_xml:
            with z.open(arquivo) as f:
                try:
                    tree = ET.parse(f)
                    root = tree.getroot()
                    
                    def find_val(tag):
                        el = root.find(f".//{{*}}{tag}")
                        return float(el.text) if el is not None else 0.0

                    def find_text(tag):
                        el = root.find(f".//{{*}}{tag}")
                        return el.text if el is not None else ""

                    # Extração com os nomes das suas tags
                    valor_bruto = find_val('ValorServicos')
                    valor_liquido = find_val('ValorLiquidoNfse')
                    # Somando impostos (ISS + INSS conforme seu XML mostrou)
                    total_impostos = find_val('ValorIss') + find_val('ValorInss')
                    data_raw = find_text('DataEmissao')
                    
                    if valor_bruto > 0:
                        dados.append({
                            'Data': pd.to_datetime(data_raw[:10]),
                            'Valor Bruto': valor_bruto,
                            'Impostos': total_impostos,
                            'Valor Liquido': valor_liquido
                        })
                except Exception as e:
                    continue
                    
    return pd.DataFrame(dados)

# --- EXECUÇÃO E SERIALIZAÇÃO ---

arquivo_zip = ''
df_notas = processar_notas_zip(arquivo_zip)

if not df_notas.empty:
    # 1. Cálculos de resumo
    print(f"--- Relatório Anual ---")
    print(f"Total de Notas: {len(df_notas)}")
    print(f"Total de Impostos (ISS+INSS): R$ {df_notas['Impostos'].sum():,.2f}")
    print(f"Valor Líquido Total: R$ {df_notas['Valor Liquido'].sum():,.2f}")

    # 2. Salvando com joblib (conforme planejado)
    if not os.path.exists('modelos'):
        os.makedirs('modelos')
    
    joblib.dump(df_notas, 'modelos/dataframe_consolidado.joblib')
    print("\n[SUCESSO] Dados salvos em 'modelos/dataframe_consolidado.joblib'")
else:
    print("Nenhum dado foi processado. Verifique se o arquivo ZIP está na pasta correta.")
