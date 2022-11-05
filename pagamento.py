
import mercadopago
import env

sdk = mercadopago.SDK(env.os.environ["SDK"])

def pagamento(valor, servico, email, nome):
    payment_data = {
        "transaction_amount": valor,
        "description": f"{servico}",
        "payment_method_id": "pix",
        "payer": {
            "email": f"{email}",
            "first_name": f"{nome}",
            "identification": {
                "type": "CPF",
                "number": "191191191-00"
            },
        }
    }

    try:
        payment_response = sdk.payment().create(payment_data)
        payment = payment_response["response"]
        
        return payment

    except:
        return print('Erro na hora de gerar o pagamento. Por favor, tente novamente.')

teste = pagamento(1, 'teste', 'teste@teste.com', 'teste')

print(teste['status'])