import zipfile
import xml.etree.ElementTree as ET

caminho_zip = 'dados/NotaFiscaldeServiçoEletrônicaNFSe_de_181_ate_246.zip'

with zipfile.ZipFile(caminho_zip, 'r') as z:
    primeiro_xml = [f for f in z.namelist() if f.endswith('.xml')][0]
    with z.open(primeiro_xml) as f:
        tree = ET.parse(f)
        root = tree.getroot()
        print(f"--- Estrutura da Nota: {primeiro_xml} ---")
        for elem in root.iter():
            # Imprime o nome da tag e o valor se ele não for vazio
            if elem.text and elem.text.strip():
                print(f"Tag: {elem.tag.split('}')[-1]} | Valor: {elem.text}")
