# Projeto de Coleta de Dados: Personagens do Universo Resident Evil
## Descrição do Projeto

O objetivo desde projeto é realizar a raspagem de dados dos personagens do universo Resident Evil a partir de páginas do site Resident Evil Database. O projeto foi inspirado pelas aulas do [@TeoCalvo](https://github.com/TeoCalvo) no canal [Teo Me Why](https://www.youtube.com/@teomewhy).

## Objetivos

- Coletar dados detalhados sobre personagens do universo Resident Evil.
- Estruturar os dados coletados em um formato acessível e utilizável para análises posteriores.
- Demonstrar técnicas de raspagem de dados e manipulação de dados em Python.

## Estrutura do Projeto

    scripts/: Contém os scripts de raspagem  de dados.
        collect.py: Script principal de raspagem de dados.
        
    data/: Diretório onde os dados coletados serão armazenados.
        raw/: Dados brutos raspados do site.

    README.md: Este arquivo.

## Requisitos

Para executar este projeto, você precisará dos seguintes pacotes Python:

- requests
- beautifulsoup4
- pandas
- tqdm
- pyarrow
- fastparquet
- jupyter (opcional)

Você pode instalar os pacotes necessários executando o seguinte comando:

```bash
pip install -r requirements.txt
```

Como Executar

Clone o repositório para sua máquina local:

```bash

git clone https://github.com/BrunoOlivei/data-collect
cd data-collect
```

Instale os pacotes necessários:

```bash
pip install -r requirements.txt
```

Execute o script de raspagem de dados:

```bash
python ResidentEvil/scripts/scraper.py
```

Explore os dados utilizando os notebooks disponíveis em notebooks/.

## Estrutura dos Dados

Os dados coletados e limpos incluirão informações como:

- Ano de Nascimento
- Tipo Sanguíneo
- Altura
- Peso
- Aparições
- link
- name

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e enviar pull requests.
Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo LICENSE para obter mais detalhes.
Agradecimentos

Agradeço ao [@TeoCalvo](https://github.com/TeoCalvo) pelas aulas inspiradoras no canal [Teo Me Why](https://www.youtube.com/@teomewhy), que motivaram a criação deste projeto.
