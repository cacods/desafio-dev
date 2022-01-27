# Instruções para instalação do sistema para testes (localhost com runserver)

O sistema foi escrito em linguagem Python 3.9 usando framework MVC Django 4.0.1 com banco de dados PostgreSQL 13.5.
Bootstrap 4.6.1 foi usado para o Frontend. 

## Pré-requisitos
1. Sistema desenvolvido em ambiente Debian GNU/Linux 11 (bullseye).


2. PostgreSQL foi usado, mas deve funcionar com PostgreSQL 9+.

   Criar banco de dados de nome "cnab" e senha "cnab123" (a _role_ postgres é cnab). Estes dados podem ser alterados no settings.py


3. Python 3.9 foi usado, mas deve rodar sem problemas com Python 3.6+. É recomendado criar um ambiente virtual do Python 3 para isolar os pacotes 
   e configurações para a execução do sistema (https://docs.python.org/3/library/venv.html).

   Rodar `pip install -r requirements.txt` para instalar os pacotes necessários. 


4. Para rodar os testes funcionais foi usado geckodriver 0.30.0 (https://github.com/mozilla/geckodriver/releases).

   Rodar os testes funcionais e unitários: `python manage.py test`.


5. Rodar o sistema em ambiente local:

   ```
   python manage.py runserver
   ```
   Acessar na aba do navegador: "localhost:8000".


## Funcionamento
Verificar os pré-requisitos acima e fazer o clone do projeto no Github.

O sistema apresenta uma tela para selecionar o arquivo CNAB.

Em caso de erro de formatação do arquivo a página exibe uma mensagem.

Caso o arquivo tenha formatação correta o arquivo é parseado, normalizado e salvo no banco de dados e, posteriormente, a tabela com os dados da 
transação é mostrada ao usuário.

Obs.: a formatação do arquivo será válida para linha de 80 caracteres e primeiro caracter entre os números 1 e 9.

A API consiste de um único ponto de entrada que é o acesso à página inicial que chama a função `home_page` da view do Django (Controller).