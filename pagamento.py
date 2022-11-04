
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

    payment_response = sdk.payment().create(payment_data)
    payment = payment_response["response"]

    return payment["point_of_interaction"]["transaction_data"]["ticket_url"]
    #return payment

#print(pagamento(2.0, "Serviço 10", "adalto.santos@aluno.faculdadeimpacta.com", "linhares"))