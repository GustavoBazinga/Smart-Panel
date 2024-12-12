# Smart Panel
Esta é uma aplicação de uso interno.
O Smart Panel, tem o intuito de gerenciar um Video Wall e o som ambiente dedicado ao Gastrobar Tabajaras, localizado no Clube dos Funcionarios - Volta Redonda.

## Funcionalidades

- [x] Download de ativos em nuvem.
- [x] Instancia de media player com os arquivos locais.
- [x] Spotify web iniciando playlist automaticamente
- [x] Api de gerenciamento de funções:
-  - [x] Reiniciar o dispositivo em que a aplicação esteja rodando
-  - [x] Reiniciar a instancia do navegador onde se encontra o Spotify Web Player
-  - [x] Realizar a atualização do diretório de ativos da aplicação

## Dados a serem preenchidos nos arquivos gerados pela função `create_file` do `check_config_file`

Alguns arquivos são gerados pelo programa em sua primeira execução, dentre eles o `_internal\config.txt`, nele existem variaveis que devem ser preenchidas manualmente com os seguintes dados:
- `SPOTIFY_PLAYLIST`: O URL de login do spotify com redirect apontado para a playlist que deseja executar quando iniciar o programa.
- `LINK_DRIVE`: O URL de compartilhamento do diretório no Google_Drive onde devem estar os ativos a serem geridos pelo sistema.
- `ACCOUNT_USERNAME`: Conta de usuário para acessar o Spotify
- `SPOTIFY_PASSWORD`: Senha do usuário criptografada pela key gerada no arquivo _'secret.key'_

## Tutorial: Gerando uma Senha Criptografada - Executavel

Para gerar uma senha criptografada utilizando a chave de criptografia localizada em `/default/secret.key`, siga os passos abaixo:

1. **Execute o programa `Encrypt The Pass.exe`**:
    Navegue até o diretório onde o arquivo `Encrypt The Pass.exe` está localizado e execute-o. Por padrão estará localizado no diretório principal.

2. **Insira a senha a ser criptografada**:
    A aplicação solicitará que você insira a senha que deseja criptografar. Digite a senha e clique em `Generate Encrypted Password`.

3. **Senha criptografada**:
    O script utilizará a chave de criptografia localizada em `default\secret.key` para criptografar a senha fornecida e exibirá a senha criptografada no terminal.

Exemplo de execução:
![hippo](https://media3.giphy.com/media/aUovxH8Vf9qDu/giphy.gif)

## Tutorial: Gerando uma Senha Criptografada - Script

1. **Execute o script `password_encrypt.py`**:
    No diretório raiz execute o arquivo `password_encrypt.py`. Lembre-se de instalar todas as dependencias descritas no arquivo `requirements.txt`, elas são necessárias para o funcionamento do programa.

2. **Insira a senha a ser criptografada**:
    A aplicação solicitará que você insira a senha que deseja criptografar. Digite a senha e clique em `Generate Encrypted Password`.

Certifique-se de copiar a senha criptografada e utilizá-la no campo `SPOTIFY_PASSWORD` no arquivo de configuração gerado.

Certifique-se de preencher todos os campos corretamente para garantir o funcionamento adequado do sistema.
