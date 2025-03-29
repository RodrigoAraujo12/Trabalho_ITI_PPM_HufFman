import re
import heapq
import time
import math
from collections import defaultdict

def limpar_texto(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        texto = arquivo.read().lower()
    
    texto = re.sub(r'á|à|â|ã', 'a', texto)
    texto = re.sub(r'é|è|ê', 'e', texto)
    texto = re.sub(r'í|ì|î', 'i', texto)
    texto = re.sub(r'ó|ò|ô|õ', 'o', texto)
    texto = re.sub(r'ú|ù|û', 'u', texto)
    texto = re.sub(r'ç', 'c', texto)
    texto = re.sub(r'[^a-z ]', '', texto)

    return texto

class PPMHuffman:
    def __init__(self, max_context=4):
        self.max_context = max_context
        self.contexts = defaultdict(lambda: defaultdict(int))
    
    def treinar(self, texto):
        for i in range(len(texto)):
            for k in range(min(i, self.max_context) + 1):
                contexto = texto[i-k:i]
                self.contexts[contexto][texto[i]] += 1
    
    def prever(self, contexto):
        for k in range(len(contexto), -1, -1):
            subcontexto = contexto[-k:]
            if subcontexto in self.contexts and self.contexts[subcontexto]:
                total = sum(self.contexts[subcontexto].values())
                return {char: freq / total for char, freq in self.contexts[subcontexto].items()}
        return None

def calcular_entropia(probabilidades):
    return sum(p * math.log2(1/p) for p in probabilidades.values()) if probabilidades else 0

class NoHuffman:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.esquerda = None
        self.direita = None
    
    def __lt__(self, outro):
        return self.freq < outro.freq

class Huffman:
    def __init__(self):
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}
    
    def construir_heap(self, frequencias):
        for char, freq in frequencias.items():
            heapq.heappush(self.heap, NoHuffman(char, freq))
    
    def construir_codigos(self):
        while len(self.heap) > 1:
            no1 = heapq.heappop(self.heap)
            no2 = heapq.heappop(self.heap)
            novo_no = NoHuffman(None, no1.freq + no2.freq)
            novo_no.esquerda = no1
            novo_no.direita = no2
            heapq.heappush(self.heap, novo_no)
        
        def gerar_codigo(no, codigo=""):
            if no is None:
                return
            if no.char is not None:
                self.codes[no.char] = codigo
                self.reverse_mapping[codigo] = no.char
            gerar_codigo(no.esquerda, codigo + "0")
            gerar_codigo(no.direita, codigo + "1")
        
        if self.heap:
            raiz = heapq.heappop(self.heap)
            gerar_codigo(raiz)
    
    def codificar(self, texto):
        return "".join(self.codes[char] for char in texto if char in self.codes)
    
    def decodificar(self, codigo):
        resultado = ""
        buffer = ""
        for bit in codigo:
            buffer += bit
            if buffer in self.reverse_mapping:
                resultado += self.reverse_mapping[buffer]
                buffer = ""
        return resultado

def comprimir(texto, max_context):
    ppm = PPMHuffman(max_context)
    ppm.treinar(texto)
    
    frequencias = defaultdict(float)
    entropia_total = 0
    for i in range(len(texto)):
        contexto = texto[max(0, i - max_context):i]
        probabilidades = ppm.prever(contexto)
        if probabilidades:
            for char, prob in probabilidades.items():
                frequencias[char] += prob
            entropia_total += calcular_entropia(probabilidades)
    
    huffman = Huffman()
    huffman.construir_heap(frequencias)
    huffman.construir_codigos()
    
    codificado = huffman.codificar(texto)
    entropia_media = entropia_total / len(texto) if texto else 0
    return codificado, huffman.codes, entropia_media

def descomprimir(codigo, codigos):
    huffman = Huffman()
    huffman.codes = codigos
    huffman.reverse_mapping = {v: k for k, v in codigos.items()}
    return huffman.decodificar(codigo)

def avaliar_compressao(caminho_arquivo):
    texto = limpar_texto(caminho_arquivo)
    resultados = []
    
    for k in range(6):
        inicio_comp = time.time()
        texto_comprimido, codigos, entropia = comprimir(texto, k)
        fim_comp = time.time()
        
        inicio_desc = time.time()
        texto_descomprimido = descomprimir(texto_comprimido, codigos)
        fim_desc = time.time()
        
        comprimento_medio = len(texto_comprimido) / len(texto) if len(texto) > 0 else 0
        tempo_compressao = fim_comp - inicio_comp
        tempo_descompressao = fim_desc - inicio_desc
        
        resultados.append((k, comprimento_medio, entropia, tempo_compressao, tempo_descompressao))
    
    print("| K | Comprimento Médio | Entropia | Tempo Compressão (s) | Tempo Descompressão (s) |")
    print("|---|-------------------|----------|----------------------|-------------------------|")
    for r in resultados:
        print(f"| {r[0]} | {r[1]:.5f} | {r[2]:.5f} | {r[3]:.5f} | {r[4]:.5f} |")


# Executar a análise
documento = "saida.txt"  # Substitua pelo nome real do arquivo
avaliar_compressao(documento)
