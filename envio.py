import smtplib
import email.message
import env

def novos_clientes(destinatario):  
    corpo_email = """
    <h1>BEM VINDO!</h1>
    <p>Obrigado por se juntar a nós! Estamos muito felizes de ter você como cliente.</p>
    <p>Atenciosamente,</p>
    <p>SixConnect.</p>
    """
    msg = email.message.Message()
    msg['Subject'] = "SixConnect"
    msg['From'] = 'sixconnect.impacta@gmail.com'
    msg['To'] = f'{destinatario}'
    password = env.os.environ['password_gmail']
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))

def clientes_antigo(destinatario):  
    corpo_email = """
    <p>Olá caro cliente.</p>
    <p>Recebemos a informação que você não faz mais parte dos clientes da Sixconnect. É uma pena mas esperamos que você possa voltar a ser nosso cliente.</p>
    <p>Atenciosamente,</p>
    <p>SixConnect.</p>
    """
    msg = email.message.Message()
    msg['Subject'] = "SixConnect"
    msg['From'] = 'sixconnect.impacta@gmail.com'
    msg['To'] = f'{destinatario}'
    password = env.os.environ['password_gmail'] 
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))


def pagamento_servico(destinatario, link):  
    corpo_email = f"""
    <h1>OLÁ!</h1>
    <p>Segue o link para o pagamento referente ao serviço que será prestado.</p>
    <p>{link}</p>
    <p>Atenciosamente,</p>
    <p>SixConnect.</p>
    """
    msg = email.message.Message()
    msg['Subject'] = "SixConnect"
    msg['From'] = 'sixconnect.impacta@gmail.com'
    msg['To'] = f'{destinatario}'
    password = env.os.environ['password_gmail']
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))