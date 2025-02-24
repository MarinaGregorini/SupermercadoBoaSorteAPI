# Documentação Base de Dados FlyUpSkill

## Visão Geral
Esta base de dados fictícia gerencia operações relacionadas à uma companhia aérea. 

Contém 06 tabelas com os temas: Aeroportos, aeronavez, voos, crew, passageiros e tickets.

## Instalação do MySQL:

Para Windows:
* Baixar o MySQL Installer for Windows em https://dev.mysql.com/downloads/installer/ 
* Executar o arquivo baixado e seguir as instruções para instalar o MySQL.
* Durante a instalação, definir a senha do root (user) e configurar a porta de rede (por padrão, é 3306).

## Backup:
* No prompt de comando (CMD), acessar a pasta onde encontra-se a pasta mysql e, dentro dela, acessar a pasta bin. Utilizar sempre o comando cd <NOME_DA_PASTA> até alcançar o diretório especificado.
* Utilizar os comandos abaixo para realizar diferentes tipos de backup:
    * Backup completo do banco de dados:
        mysqldump -u <USER> -p <DBNAME> > <DESTFILE.SQL>
    * Backup apenas da estrutura do banco de dados:
        mysqldump --no-data -u <USER> -p <DBNAME> > <DESTFILE.SQL>
    * Backup apenas dos dados contidos no banco de dados:
        mysqldump --no-create-info -u <USER> -p <DBNAME> > <DESTFILE.SQL>

## Restauro:
* Sempre no CMD, se a base de dados ainda não existir, cria-la com o comando:
    mysql -u <USER> -p –e ”CREATE DATABASE destination_db”
* Caso a base de dados já exista ou tenha apenas sido criada, importá-la com o comando:
    mysql -u <USER> -p < <SOURCEFILE.SQL>


