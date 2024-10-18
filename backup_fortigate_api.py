import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

# Desativar avisos de SSL
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Função para enviar email com o resumo dos backups em HTML
def enviar_email(resultados_backup, destinatarios):
    server_smtp = 'smtp.office365.com'
    port = 587
    sender_email = 'email_remente@gmail.com'  # Use variáveis de ambiente para o email do remetente
    password = 'sua_senha'      # Use variáveis de ambiente para a senha

    subject = 'Resumo dos Backups de Firewalls Accerte'

    # Corpo do email em HTML
    html_body = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
            }}
            h2 {{
                color: #4CAF50;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
            }}
            th, td {{
                padding: 8px 12px;
                border: 1px solid #ddd;
                text-align: left;
            }}
            th {{
                background-color: #4CAF50;
                color: white;
            }}
            tr:nth-child(even) {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>
    <body>
        <h2>Resumo dos Backups Semanais de Firewalls</h2>
        <p>Olá,</p>
        <p>Aqui está o resumo dos backups de firewalls realizados:</p>
        <table>
            <tr>
                <th>Firewall</th>
                <th>Status</th>
            </tr>
            {resultados_backup}
        </table>
        <p>Atenciosamente,<br>Equipe Redes e Segurança - Accerte</p>
    </body>
    </html>
    """

    # Configurações do email
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = ', '.join(destinatarios) # Armazena uma lista de emails que serão disparados os alertas
    message['Subject'] = subject
    message.attach(MIMEText(html_body, 'html'))  # Definir o corpo como HTML

    # Conectando ao servidor SMTP e enviando email
    try:
        server = smtplib.SMTP(server_smtp, port)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, destinatarios, message.as_string())
        print(f"E-mail enviado para {', '.join(destinatarios)}")
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
    finally:
        server.quit()

# Função para realizar o backup de um firewall usando token
def backup_firewall(firewall_url, token):
    backup_url = f'https://{firewall_url}/api/v2/monitor/system/config/backup?scope=global' #Caso o firewall utilize portas, adicione na url

    # Headers da requisição
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    # Iniciar sessão
    session = requests.Session()
    try:
        backup_response = session.get(backup_url, headers=headers, verify=False, stream=True, timeout=600)
        content_type = backup_response.headers.get('Content-Type')

        if backup_response.status_code == 200 and 'application/octet-stream' in content_type:

            # Identifica a localização do script e define onde o backup será armazenado
            script_directory = os.path.dirname(os.path.realpath(__file__))
            backup_filename = os.path.join(script_directory, f'backup_{firewall_url.replace(".", "_").replace(":", "_")}.conf')

            with open(backup_filename, 'wb') as backup_file:
                for chunk in backup_response.iter_content(chunk_size=8192): # 8KB por chunk
                    if chunk:
                        backup_file.write(chunk)
            print(f"Backup realizado com sucesso para {firewall_url}! Salvo em '{backup_filename}'.")
            return f"<tr><td>{firewall_url}</td><td style='color:green;'>Sucesso</td></tr>\n"
        else:
            print(f"Falha ao acessar {backup_url}. Status code: {backup_response.status_code}, Content-Type: {content_type}")
            return f"<tr><td>{firewall_url}</td><td style='color:red;'>Falha - Status {backup_response.status_code}</td></tr>\n"
    except Exception as e:
        print(f"Erro ao realizar o backup para {firewall_url}: {e}")
        return f"<tr><td>{firewall_url}</td><td style='color:red;'>Erro: {e}</td></tr>\n"

# Função principal para processar os backups e enviar o relatório
def processar_backups(firewalls):
    resultados_backup = ""  # Armazenar resultados dos backups

    for firewall in firewalls:
        firewall_url = firewall['url']
        token = firewall['token']
        resultado = backup_firewall(firewall_url, token)
        resultados_backup += resultado

    # Definir destinatários do resumo de backups de firewalls
    destinatarios = ['seu_email@gmail.com']  # Pode adicionar mais emails

    # Enviar email com o resumo dos backups em formato HTML
    enviar_email(resultados_backup, destinatarios)

# Lista de URLs/IPs dos firewalls
firewalls = [
    {'url':'IP_DO_FIREWALL_1', 'token': 'TOKEN_DO_FIREWALL_1'},
    {'url':'IP_DO_FIREWALL_2', 'token': 'TOKEN_DO_FIREWALL_2'}, # Adicione quantos firewall e tokens forem necessários
]

# Executar o processo de backups
processar_backups(firewalls)
