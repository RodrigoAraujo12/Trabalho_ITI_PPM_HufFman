# Compressor-Descompressor PPM-Huffman

Este projeto implementa um compressor e descompressor baseado no algoritmo **PPM-Huffman**. Ele é projetado para processar textos compostos apenas pelas 26 letras do alfabeto português (minúsculas) e espaços, removendo acentos, cedilha, pontuação, números e outros símbolos.

## 📌 Funcionalidades

- **Pré-processamento do texto**: Converte todas as letras para minúsculas, remove acentos e caracteres indesejados.
- **Treinamento com PPM**: Armazena a frequência de caracteres com base no contexto para melhorar a compressão.
- **Compressão com Huffman**: Constrói uma árvore de Huffman para gerar códigos compactos para os caracteres do texto processado.
- **Descompressão**: Restaura o texto original a partir dos códigos de Huffman gerados.
- **Armazenamento dos resultados**:
  - `saida.txt`: Texto pré-processado.
  - `comprimido.txt`: Texto comprimido usando Huffman.
  - `descomprimido.txt`: Texto restaurado após a descompressão.

## 📂 Estrutura do Código

- `limpar_texto()`: Lê um arquivo de entrada, remove caracteres indesejados e salva o resultado.
- `PPMHuffman`: Classe que implementa o modelo de previsão de caracteres baseado em contextos.
- `Huffman`: Implementação do algoritmo de compressão de Huffman.
- `comprimir()`: Realiza a compressão do texto utilizando PPM-Huffman.
- `descomprimir()`: Reconstrói o texto original a partir do código comprimido.

## 🔧 Como Usar

1. Coloque o texto de entrada em um arquivo chamado `entrada.txt`.
2. Execute o script Python:
   ```bash
   python script.py
