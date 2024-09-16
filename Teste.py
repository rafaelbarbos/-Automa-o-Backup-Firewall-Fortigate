import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Desativar avisos de SSL
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Função para autenticar e realizar o backup de um firewall
def backup_firewall(firewall_url, username, password):
    login_url = f'https://{firewall_url}/logincheck'
    backup_url = f'https://{firewall_url}/api/v2/monitor/system/config/backup?scope=global'

    # Dados para login
    data = {
        'username': username,
        'secretkey': password,  # Pode ser 'password' dependendo do sistema
    }

    # Headers da requisição
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    # Iniciar sessão
    session = requests.Session()
    login_response = session.post(login_url, headers=headers, data=data, verify=False)

    # Verificar se a autenticação foi bem-sucedida
    if login_response.status_code == 200:
        print(f"Autenticado com sucesso no firewall: {firewall_url}")

        # Realizar o backup
        backup_response = session.get(backup_url, verify=False, stream=True)

        content_type = backup_response.headers.get('Content-Type')
        print(f"Content-Type recebido: {content_type}")

        if backup_response.status_code == 200:
            if 'application/octet-stream' in content_type:
                # Nome do arquivo de backup baseado no firewall URL
                backup_filename = f'backup_{firewall_url.replace(".", "_").replace(":", "_")}.conf'
                with open(backup_filename, 'wb') as backup_file:
                    for chunk in backup_response.iter_content(chunk_size=1024):
                        if chunk:
                            backup_file.write(chunk)
                print(f"Backup realizado com sucesso para {firewall_url}! Salvo como '{backup_filename}'.")
            else:
                print(f"Conteúdo inesperado recebido do firewall {firewall_url}: {backup_response.text}")
        else:
            print(f"Erro ao realizar backup: {backup_response.status_code}")
    else:
        print(f"Falha na autenticação no firewall {firewall_url}: {login_response.status_code}")
        print(login_response.text)  # Exibe o conteúdo da resposta de login para ajudar no diagnóstico

# Lista de URLs dos firewalls
firewalls = [
      # Adicione quantas URLs de firewalls forem necessárias
]

# Nome de usuário e senha para todos os firewalls
username = 'usuario'  # Certifique-se de que o usuário tem permissões adequadas
password = 'senha'

# Iterar sobre a lista de firewalls e fazer o backup de cada um
for firewall_url in firewalls:
    try:
        backup_firewall(firewall_url, username, password)
    except Exception as e:
        print(f"Erro ao realizar backup do firewall {firewall_url}: {e}")
