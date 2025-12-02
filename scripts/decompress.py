import sys
import zipfile
import os


if len(sys.argv) < 3:

    print("Erro: Faltam argumentos. Uso: python decompress.py <caminho_zip> <pasta_destino>")
    sys.exit(1)

caminho_zip = sys.argv[1]
pasta_destino = sys.argv[2]

print(f"\n* Iniciando Processamento")
print(f"Origem: {caminho_zip}")
print(f"Destino: {pasta_destino}")

# 1. Garante que a pasta de destino existe
os.makedirs(pasta_destino, exist_ok=True)

try:
    with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:

        # Extrai tudo para a pasta especificada
        zip_ref.extractall(pasta_destino)
        
        # Lista os arquivos para log
        arquivos = zip_ref.namelist()

        print(f"Sucesso! {len(arquivos)} arquivo(s) extraído(s):")

        for arq in arquivos:
            print(f" - {arq}")
            
except Exception as e:
    
    print(f"ERRO CRÍTICO ao descompactar: {e}")
    sys.exit(1)