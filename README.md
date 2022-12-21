# FSE-Trabalho-1-2022-2
Trabalho 1 da disciplina de Fundamentos de Sistemas Embarcados 2022-2

 
## Descrição

Este trabalho tem por objetivo a criação de um sistema distribuído de automação predial para monitoramento e acionamento de sensores e dispositivos de um prédio com múltiplas salas. O sistema deve ser desenvolvido para funcionar em um conjunto de placas Raspberry Pi com um servidor central responsável pelo controle e interface com o usuário e servidores distribuídos para leitura e acionamento dos dispositivos. Dentre os dispositivos envolvidos estão o monitoramento de temperatura e umidade, sensores de presença, sensores de fumaça, sensores de contagem de pessoas, sensores de abertura e fechamento de portas e janelas, acionamento de lâmpadas, aparelhos de ar-condicionado, alarme e aspersores de água em caso de incêndio. Para mais detalhes e informações consulte o [link](https://gitlab.com/fse_fga/trabalhos-2022_2/trabalho-1-2022-2).

## Para rodar os passos são: 

### Passo 1: Configurar arquivos de comunicação entre servidores

Configurar os arquivos de comunicação entre os servidores com base em qual placas os servidores irão rodar. (servidor central e distribuido)

Modifique os arquivos config-s0X.json de acordo com a sua escolha,sendo X a configuração da sala presente no respectivo arquivo Json.
O servidor central de todas as configurações  de salas está por padrão com o mesmo ip e o distribuido está configurado para sala 04 conforme o exemplo abaixo.

### Para Servidor Central

O mesmo se encontra no diretório  e arquivo **src/ cent/ cent.py**  dentro da função principal conforme apresentado abaixo:

```python
if __name__ == "__main__":
    
        conf= readFileConfigCent('../jsons/config-s04.json')
```

### Para Servidor Distribuido

O mesmo se encontra no diretório  e arquivo **src/ dist/ dist.py** entro da função principal conforme apresentado abaixo:

```python

if __name__ == "__main__":
     
    conf= readFileConfigDist('../jsons/config-s04.json')
```

## Passo 2: Executar Servidor Central
Após configurar os arquivos dos dois servidores, coloque o servidor central em execução primeiro com o comando abaixo não esquecendo de verificar se está no diretório do respectivo arquivo. 
```terminal
python3 cent.py
```
## Passo 3: Executar Servidor Distribuido
Após iniciar o servidor central entre na pasta **dist** e execute o comando abaixo para rodar o servidor distribuido.
```terminal
python3 dist.py
```





