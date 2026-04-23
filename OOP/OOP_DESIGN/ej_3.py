class EmailSender:
    def send(self, msg):
        return f"Email: {msg}"

class SMSSender:
    def send(self, msg):
        return f"SMS: {msg}"

class MultiChannelSender(EmailSender, SMSSender):
    def send(self, msg):
        e = EmailSender.send(self, msg)
        s = SMSSender.send(self, msg)
        return f"{e} | {s}"
    
    
sen = MultiChannelSender()
print(sen.send("hola")) 

# resultado esperado al llamar MultiChannelSender().send("Hola"):
# Email: Hola
# SMS: Hola