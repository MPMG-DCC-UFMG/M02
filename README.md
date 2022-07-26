# M02
## Segmentação e Classificação Semântica de Textos

Este repositório é sobre dois aspectos críticos que envolvem documentos governamentais oficiais: segmentação e classificação semântica. O primeiro consiste em separar o texto de um Diário Oficial (DO) em trechos que nos permitam identificar o ente federado associado, o título e o conteúdo dos atos governamentais ali publicados, bem como o(s) responsável(eis) por sua criação. Entretanto, esse não é um problema trivial, visto que cada documento possui uma estrutura de apresentação específica que inclui diferentes componentes gráficos (e.g., separadores visuais). Em relação à classificação semântica do texto extraído, o intuito é prever corretamente a qual classe uma nova observação pertence dado um conjunto pré-determinado de categorias como, por exemplo, se um trecho extraído pertence à classe Leis ou Licitações.

## Instalação

A primeira etapa para poder instalar o sistema é realizar o donwload de seu código-fonte. Para isso, utilize as ferramentas do GitHub para baixar o repositório localmente (https://github.com/MPMG-DCC-UFMG/M02.git).

Em seguida, é importante notar que para usar o programa é necessário um virtualenv ou uma máquina apenas com Python 3.8, de maneira que os comandos "python" referencie o Python 3.8, e "pip" procure a instalação de pacotes também do Python 3.8.

### Instalação do Módulo de Segmentação 

```
Entrar na pasta com o módulo de segmentação:
cd Segmentacao

Informações sobre o módulo:
python3.8 main.py --help

Execute o comando para segmentar um Diário Oficial (PDF):
python3.8 main.py --pdf <arquivo.pdf>

Execute o comando para segmentar todos Diários Oficiais (PDFs) em uma pasta:
python3.8 main.py --dir <diretório>

Redirecionar os arquivos de saída
python3.8 main.py -o <diretório>

```

### Instalação do Módulo de Classificação

```
Entrar na pasta com o módulo de classificação:**
cd Classificacao

Informações sobre o módulo:
python3.8 main.py --help

Replicar a avaliação experimental:
python3.8 main.py --test

Treinar um novo modelo preditivo:
python3.8 main.py --train

Classificar um segmento textual:
python3.8 main.py --segmento <texto>

Classificar um conjunto de arquivos JSONs em um diretório:
python3.8 main.py

```
