class CreditCard:
    def pay(self, amount):
        return f"Card charged: {amount}€"

class PayPal:
    def pay(self, amount):
        return f"PayPal sent: {amount}€"

class Crypto:
    def pay(self, amount):
        return f"Crypto transferred: {amount}€"

def checkout(payments, total):
    # divide el total entre len(payments)
    share = total / len(payments)
    # llama a pay() de cada uno
    for p in payments:  
        print(p.pay(share))
    
methods = [CreditCard(), PayPal(), Crypto()]
checkout(methods, 90)