# F01
Processamento dos dados coletados dos portais de transparência dos municípios do Estado de Minas Gerais

Este repositório apresenta códigos dos validadores e da API que disponibiliza os resultados

O repositório está dividido nos seguintes diretórios:

* src: contém implementações dos validaores, referentes as licitações públicas;
* service: contém o código da API REST JSON que disponibiliza os resultados obtidos para cada município;


## API

### Iniciar a API localmente 
A primeira etapa para poder instalar o sistema é realizar o donwload de seu código-fonte. Para isso, utilize as ferramentas do GitHub para baixar o repositório localmente. Em seguida, é necessário um virtualenv ou uma máquina apenas com Python 3.7+ com requirements descritos em "equirements.txt"

Dentro de /service

```
FLASK_APP=main.py flask run
```

Por padrão a porta sera a `5000` http://localhost:5000

## Consultas ao resultado dos validadores

Obs: Os itens estão listados em 'lista_exigencias.csv'

### Consulta de todos os itens de um municipio:

```
http://localhost:5000/{municipio}
```
- Método GET

- Entrada: Parâmetros: Nome do municipio. Obrigatório, do tipo string pelo cabeçalho.

- Resposta: Formato da resposta `JSON` com cada item (possívelmente de até 1 a 103) `true` ou `false` caso satisfeito.

### Consulta a um item específico de um municipio:

```
http://localhost:5000/{municipio}/{nº_do_item}
```
- Método GET

- Entrada: Parâmetros: Nome do municipio. Obrigatório, do tipo string pelo cabeçalho.

- Resposta: Formato da resposta `JSON` com `true` ou `false` caso satisfeito.
