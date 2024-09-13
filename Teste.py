import requests
import json

# URL de autenticação e backup
login_url = 'https://192.168.1.99/logincheck'  # Endpoint de login padrão para FortiGate
backup_url = 'https://192.168.1.99/api/v2/monitor/system/config/backup?scope=global'  # Possível endpoint correto para backup

# Dados para login
username = 'admin'
password = 'teste01'

# Headers da requisição
headers = {'Content-Type': 'application/x-www-form-urlencoded'}  # Mudança para 'application/x-www-form-urlencoded'

# Dados para a requisição de login
data = {
    'username': username,
    'secretkey': password,  # 'secretkey' pode ser necessário dependendo do sistema FortiGate
}

# Desativar avisos de SSL
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Autenticação
session = requests.Session()
login_response = session.post(login_url, headers=headers, data=data, verify=False)

# Verificar se a autenticação foi bem-sucedida
if login_response.status_code == 200:
    print("Autenticado com sucesso!")

    # Realizar o backup da configuração
    backup_response = session.get(backup_url, verify=False, stream=True)

    # Verifica se a resposta do backup foi bem-sucedida
    if backup_response.status_code == 200:
        # Verificar se o conteúdo retornado é HTML ou o backup real
        content_type = backup_response.headers.get('Content-Type')

        if 'application/octet-stream' in content_type:
            # Salvar o conteúdo do backup em um arquivo .conf
            with open('backup_fortigate.conf', 'wb') as backup_file:
                for chunk in backup_response.iter_content(chunk_size=1024):  # Lê o arquivo em pedaços de 1KB
                    if chunk:  # Se houver dados, escreve no arquivo
                        backup_file.write(chunk)
            print("Backup realizado com sucesso! Foi salvo como 'backup_fortigate.conf'.")
        else:
            # Se o conteúdo não for o esperado (talvez HTML), mostre a resposta
            print("Ocorreu um erro: o servidor retornou HTML em vez de um arquivo de backup.")
            print(backup_response.text)  # Exibe o HTML ou mensagem de erro
    else:
        print(f"Erro ao realizar backup: {backup_response.status_code}")
else:
    print(f"Falha na autenticação! Status: {login_response.status_code}")
    print(login_response.text)  # Exibe o conteúdo da resposta de login para ajudar no diagnóstico
