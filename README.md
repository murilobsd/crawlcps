# crawlercps lab804

![](logo/logo.jpg)

## Introdução

Simples crawler para checar se existem novas vagas no Centro Paulo Souza.

O crawler foi desenvolvido na versão **2.7.11** do python.

## Instalando python

### Linux
```bash
$ sudo apt-get update
$ sudo apt-get install python-dev python-setuptools
```

### Windows
- [https://www.python.org/ftp/python/2.7.11/python-2.7.11.amd64.msi](Download)
- [http://stackoverflow.com/questions/3701646/how-to-add-to-the-pythonpath-in-windows-7](Adicionando ao Path)
- Abra o cmd e digite **python**


## Instalando as dependências


### Linux
```bash
# diretorio do projeto
$ pip install -r req.txt
```

### Windows
```bash
pip install -r req.txt
```

## Configuração
Existe o arquivo **conf.json** alguns dados são essenciais para notificação.

```json
{
  "periodo": 604800,
  "url": "http://cpssitevm.cloudapp.net/dgsdad/SelecaoPublica/ETEC/ConcursoDocente/Inscricoesabertas.aspx",
  "notificacao": "",
  "classtable": "table",
  "backup": "backup.txt",
  "email": "",
  "password": ""
}

- Periodo: está em segundo se corresponde uma checagem a cada 7 dias.
- notificacao: para qual email será enviado as notificacoes de novas vagas.
- email: conta de email no gmail para envio
- password: respectiva senha do email acima.
- backup: ficara uma copia na maquina local para comparar as alteracoes.
- classtable: para localizar a table no html
```

## Rodando

### Linux
```bash
$ python main.py -j conf.json
```

### Windows
```bash
python main.py -j conf.json
```

## Dúvidas
```bash
python main.py -h
```
