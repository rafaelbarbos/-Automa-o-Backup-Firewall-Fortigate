# Firewall Backup Script

Este projeto é um script em Python que permite automatizar o processo de backup de configurações de múltiplos firewalls FortiGate. O script autentica-se em cada firewall, realiza o backup e salva o arquivo localmente.

## Funcionalidades

- Autenticação em firewalls FortiGate.
- Realiza backup de configurações de múltiplos firewalls em sequência.
- Salva os arquivos de backup localmente com nomes baseados no IP do firewall.
- Ignora avisos de SSL para conexões não seguras.

## Pré-requisitos

- **Python 3.x** instalado.
- A biblioteca **requests** instalada. Para instalar, execute o seguinte comando:

``bash
pip install requests

## Como usar
- 1 Clone este repositório:
  git clone https://github.com/seu-usuario/firewall-backup.git

- 2 Navegue até o diretório do projeto:
  cd firewall-backup

- 3 Edite o arquivo `backup_script.py` e insira as URLs dos firewalls, o nome de usuário e a senha

- 4 Execute o `backup_script.py`

## Exemplo de configuração

```
firewalls = [
    '100.100.1.100',
    '100.100.1.101',
    # Adicione quantos firewalls forem necessários
]

username = 'admin'
password = 'sua-senha'

```





## Exemplo de saída
Para cada firewall, o script gera um arquivo de backup com o nome `backup_<ip_do_firewall>.conf`.
Exemplo de saída:

```
Backup realizado com sucesso para 192.168.1.99! Salvo como 'backup_192_168_1_99.conf'.
```

## Possíveis Erros
- Falha de autenticação: Verifique o nome de usuário e a senha
- Conteúdo inesperado recebido: Pode ocorrer se o firewall não tiver permissões adequadas para realizar o backup via API
