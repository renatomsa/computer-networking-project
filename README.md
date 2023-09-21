# computer-networking-project

## Segunda Etapa: Implementando chat com transferência confiável RDT 3.0

- A estrutura do projeto conta com 2 arquivos executaveis: ```clientUDP.py``` e  ```serverUDP.py```, sendo o arquivo de declaracao e inicializacao da classe client e server, respectivamente. Alem disso, há um arquivo ```utils.py``` que guarda variaveis que serao usadas ao longo do codigo => tamanho do buffer, ip local e a porta do servidor.

## Rodando o chat

- O primeiro passo é inicializar o servidor do chat. Para isso, no diretorio ```app```, execute o arquivo ```serverUDP.py```.
- Depois de iniciar o servidor, o chat ja esta pronto para receber os usuarios. Para se conectar ao servidor e começar a usar o chat, basta executar o arquivo ```clientUDP.py```, que se encontra no diretorio ```app``` e digitar ```hi, meu nome é <nome do usuario>```.

### Outras funcionalidades:

- Para o cliente se desconectar do chat, basta digitar ```bye``` e enviar. A socket será fechada e o cliente será desconectado da sala.
- Se o cliente quer ver quais usuarios estao conectados a sala, basta digitar ```list``` e enviar. O cliente que fez a requisição da lista receberá uma mensagem que lista os usuarios com seus respectivos nomes e endereços de ip e porta.

## Grupo:
- Rodrigo Rossiter Ladvocat Cintra <rrlc>
- Joao Henrique da Matta Lessa Ribeiro <jhmrl>
- Renato Moreira Serrano de Andrade <rmsa>
- Joao Pedro Cavalcanti Fernandes <jpcf2>
- Rafael Rios Cabral Victal <rrcv>
- Beatriz Freire Pimenta Cavalcante <bfpc>
- Nicolas Veiga Gomes Bezerra <nvgb>