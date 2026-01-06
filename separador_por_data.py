import os
import re
from pathlib import Path
import shutil
import sys

# Configurar encoding para suportar caracteres especiais
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Dicionários de conversão de datas em extenso
MESES = {
    'janeiro': '01', 'fevereiro': '02', 'março': '03', 'abril': '04',
    'maio': '05', 'junho': '06', 'julho': '07', 'agosto': '08',
    'setembro': '09', 'outubro': '10', 'novembro': '11', 'dezembro': '12'
}

NUMEROS = {
    'um': '1', 'uma': '1', 'dois': '2', 'duas': '2', 'três': '3',
    'quatro': '4', 'cinco': '5', 'seis': '6', 'sete': '7', 'oito': '8',
    'nove': '9', 'dez': '10', 'onze': '11', 'doze': '12', 'treze': '13',
    'quatorze': '14', 'quinze': '15', 'dezesseis': '16', 'dezessete': '17',
    'dezoito': '18', 'dezenove': '19', 'vinte': '20', 'trinta': '30',
    'quarenta': '40', 'cinquenta': '50', 'sessenta': '60', 'setenta': '70',
    'oitenta': '80', 'noventa': '90', 'cem': '100', 'cento': '100'
}


def extrair_datas_extenso(texto):
    """
    Extrai datas em português por extenso do texto.
    Procura por padrões como: "finalizado em 15 de setembro de 2025"
    """
    datas_encontradas = []
    texto_lower = texto.lower()
    
    # Padrão: "numero de mes de ano" (ex: "15 de setembro de 2025")
    # Também procura por variações com "finalizado em", "criado em", etc.
    padrao = r'(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4}|\w+\s+\w+|\w+)'
    
    matches = re.finditer(padrao, texto_lower)
    
    for match in matches:
        dia_str, mes_str, ano_str = match.groups()
        
        try:
            # Converter dia (já é número)
            try:
                dia = int(dia_str)
            except:
                dia = converter_dia(dia_str)
            
            if dia is None or dia < 1 or dia > 31:
                continue
            
            # Converter mês
            mes_str_clean = mes_str.strip()
            mes = MESES.get(mes_str_clean)
            if mes is None:
                continue
            
            # Converter ano
            ano_str_clean = ano_str.strip()
            if ano_str_clean.isdigit():
                ano = int(ano_str_clean)
                if ano < 100:  # Se ano tem 2 dígitos, assumir 20xx
                    ano += 2000
            else:
                ano = converter_ano(ano_str_clean)
            
            if ano is None or ano < 1900 or ano > 2100:
                continue
            
            data_formatada = f"{dia:02d}/{mes}/{ano}"
            if data_formatada not in datas_encontradas:
                datas_encontradas.append(data_formatada)
        except Exception as e:
            pass
    
    return datas_encontradas


def converter_dia(dia_str):
    """Converte dia em extenso para número"""
    dia_str = dia_str.strip().lower()
    
    if dia_str in NUMEROS:
        return int(NUMEROS[dia_str])
    
    # Tenta processar números compostos (vinte e cinco = 25)
    partes = dia_str.split('e')
    if len(partes) == 2:
        parte1 = NUMEROS.get(partes[0].strip())
        parte2 = NUMEROS.get(partes[1].strip())
        if parte1 and parte2:
            return parte1 + parte2
    
    return None


def converter_ano(ano_str):
    """Converte ano em extenso para número"""
    ano_str = ano_str.strip().lower()
    
    # Trata "dois mil vinte e cinco" -> 2025
    if 'mil' in ano_str:
        partes = ano_str.split()
        numero_antes = 0
        numero_depois = 0
        
        # Processa partes antes de "mil"
        temp = []
        for i, parte in enumerate(partes):
            if parte == 'mil':
                temp_str = ' '.join(partes[:i])
                numero_antes = processar_numero_composto(temp_str)
                if numero_antes == 0:
                    numero_antes = 1
                numero_antes *= 1000
                
                # Processa partes depois de "mil"
                temp_str = ' '.join(partes[i+1:])
                numero_depois = processar_numero_composto(temp_str)
                break
        
        ano = numero_antes + numero_depois
        return ano if 1900 <= ano <= 2100 else None
    
    return None


def processar_numero_composto(texto):
    """Processa números compostos como 'vinte e cinco'"""
    texto = texto.strip().lower()
    if not texto:
        return 0
    
    partes = texto.split('e')
    resultado = 0
    
    for parte in partes:
        parte = parte.strip()
        if parte in NUMEROS:
            resultado += int(NUMEROS[parte])
    
    return resultado


def extrair_texto_pdf(caminho_pdf):
    """Extrai texto do PDF usando múltiplas estratégias"""
    texto = ""
    
    # Estratégia 1: pdfplumber
    try:
        import pdfplumber
        with pdfplumber.open(caminho_pdf) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    texto += page_text + "\n"
            if texto.strip():
                return texto
    except Exception as e:
        pass
    
    # Estratégia 2: PyPDF2
    try:
        from PyPDF2 import PdfReader
        with open(caminho_pdf, 'rb') as arquivo:
            leitor = PdfReader(arquivo)
            for pagina in leitor.pages:
                page_text = pagina.extract_text()
                if page_text:
                    texto += page_text + "\n"
            if texto.strip():
                return texto
    except Exception as e:
        pass
    
    # Estratégia 3: pdf2image + OCR com rotação automática
    try:
        from pdf2image import convert_from_path
        import pytesseract
        from PIL import Image
        
        print(f"      [OCR] Processando com OCR...")
        images = convert_from_path(caminho_pdf, first_page=1, last_page=5, dpi=200)
        
        for idx, img in enumerate(images):
            # Tentar diferentes rotações (0, 90, 180, 270 graus)
            melhor_texto = ""
            for rotacao in [0, 90, 180, 270]:
                try:
                    img_rotada = img.rotate(rotacao, expand=False) if rotacao != 0 else img
                    page_text = pytesseract.image_to_string(img_rotada, lang='por')
                    
                    # Preferir texto com "de" que é típico de datas
                    if page_text.count('de') > melhor_texto.count('de'):
                        melhor_texto = page_text
                    
                    if len(page_text.strip()) > len(melhor_texto.strip()) * 1.5:
                        melhor_texto = page_text
                except:
                    pass
            
            if melhor_texto.strip():
                texto += melhor_texto + "\n"
        
        if texto.strip():
            return texto
    except ImportError as e:
        pass
    except Exception as e:
        pass
    
    return texto


def organizar_pdfs_por_data(pasta_arquivos):
    """
    Processa todos os PDFs na pasta e os organiza em subpastas por data
    """
    caminho_base = Path(pasta_arquivos)
    
    if not caminho_base.exists():
        print(f"ERRO: A pasta '{pasta_arquivos}' nao existe!")
        return
    
    # Encontrar todos os PDFs
    pdfs = list(caminho_base.glob("*.pdf"))
    
    if not pdfs:
        print("Aviso: Nenhum arquivo PDF encontrado na pasta Arquivos/")
        return
    
    print(f"[INFO] Encontrados {len(pdfs)} arquivos PDF\n")
    
    stats = {
        'processados': 0,
        'com_data': 0,
        'sem_data': 0,
        'pasta_sem_data': 'SEM_DATA'
    }
    
    # Criar pasta para PDFs sem data
    pasta_sem_data = caminho_base / stats['pasta_sem_data']
    
    for pdf in pdfs:
        print(f"[PROCESSANDO] {pdf.name}")
        
        # Extrair texto do PDF
        texto = extrair_texto_pdf(str(pdf))
        
        if not texto:
            print(f"   [AVISO] Nao foi possivel extrair texto do PDF\n")
            stats['sem_data'] += 1
            continue
        
        # Procurar datas em extenso
        datas = extrair_datas_extenso(texto)
        
        if datas:
            # Usar a primeira data encontrada
            data = datas[0]
            print(f"   [SUCESSO] Data encontrada: {data}")
            
            # Criar pasta com a data (substitui barras por hífen para evitar subpastas)
            nome_pasta = data.replace('/', '-')  # 25/01/2025 -> 25-01-2025
            pasta_data = caminho_base / nome_pasta
            pasta_data.mkdir(exist_ok=True)
            
            # Mover PDF para a pasta
            novo_caminho = pasta_data / pdf.name
            shutil.move(str(pdf), str(novo_caminho))
            print(f"   [MOVIDO] {nome_pasta}/")
            
            stats['com_data'] += 1
        else:
            print(f"   [ERRO] Nenhuma data encontrada")
            
            # Mover para pasta SEM_DATA
            pasta_sem_data.mkdir(exist_ok=True)
            novo_caminho = pasta_sem_data / pdf.name
            shutil.move(str(pdf), str(novo_caminho))
            
            stats['sem_data'] += 1
        
        stats['processados'] += 1
        print()
    
    # Exibir resumo
    print("=" * 60)
    print("RESUMO DA OPERACAO")
    print("=" * 60)
    print(f"[OK] PDFs processados: {stats['processados']}")
    print(f"[OK] PDFs com data encontrada: {stats['com_data']}")
    print(f"[ERRO] PDFs sem data: {stats['sem_data']}")
    print("=" * 60)


if __name__ == "__main__":
    pasta = "Arquivos"
    print("\n[INICIO] Iniciando separacao de PDFs por data...\n")
    organizar_pdfs_por_data(pasta)
    print("\n[FIM] Processo finalizado!")
