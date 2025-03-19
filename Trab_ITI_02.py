import re
import heapq
from collections import defaultdict

# Função para limpar o texto
def limpar_texto(caminho_arquivo, caminho_saida):
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        texto = arquivo.read().lower()
    
    texto = re.sub(r'á|à|â|ã', 'a', texto)
    texto = re.sub(r'é|è|ê', 'e', texto)
    texto = re.sub(r'í|ì|î', 'i', texto)
    texto = re.sub(r'ó|ò|ô|õ', 'o', texto)
    texto = re.sub(r'ú|ù|û', 'u', texto)
    texto = re.sub(r'ç', 'c', texto)
    texto = re.sub(r'[^a-z ]', '', texto)
    
    with open(caminho_saida, 'w', encoding='utf-8') as arquivo_saida:
        arquivo_saida.write(texto)
    
    return texto

# Implementação do PPM-Huffman
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
        if contexto in self.contexts:
            return self.contexts[contexto]
        return None

# Implementação da Codificação Huffman
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

# Função principal para compressão e descompressão
def comprimir(texto):
    ppm = PPMHuffman()
    ppm.treinar(texto)
    frequencias = defaultdict(int)
    for char in texto:
        frequencias[char] += 1
    
    huffman = Huffman()
    huffman.construir_heap(frequencias)
    huffman.construir_codigos()
    return huffman.codificar(texto), huffman.codes

def descomprimir(codigo, codigos):
    huffman = Huffman()
    huffman.codes = codigos
    huffman.reverse_mapping = {v: k for k, v in codigos.items()}
    return huffman.decodificar(codigo)

# Exemplo de uso
caminho_arquivo = "saida.txt"
caminho_saida = "saida_tratada.txt"
texto_limpo = limpar_texto(caminho_arquivo, caminho_saida)
print("Texto limpo salvo em", caminho_saida)

texto_comprimido, codigos = comprimir(texto_limpo)
with open("comprimido.txt", "w", encoding="utf-8") as arquivo_comprimido:
    arquivo_comprimido.write(texto_comprimido)
print("Texto comprimido salvo em comprimido.txt")

texto_descomprimido = descomprimir(texto_comprimido, codigos)
with open("descomprimido.txt", "w", encoding="utf-8") as arquivo_descomprimido:
    arquivo_descomprimido.write(texto_descomprimido)
print("Texto descomprimido salvo em descomprimido.txt")
