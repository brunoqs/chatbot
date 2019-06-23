from chatbot import Chatbot

chatbot = Chatbot()

flag = True
print("BOT: Olá querido usuário, fico a disposição para responder perguntas sobre mercado, saúde, tecnologia e telefonia. Diga tchau quando encerrar!")
while(flag == True):
    user_request = input('Pergunta: ')
    user_request = user_request.lower()
    if(user_request != 'tchau'):
        if(user_request == 'obrigado' or user_request == 'muito obrigado' ):
            flag=False
            print("BOT: Não há de que...")
        else:
            if(chatbot.greeting(user_request) != None):
                print("BOT: " + chatbot.greeting(user_request))
            else:
                print("BOT: Pensando...")
                print("BOT: " + chatbot.response(user_request))
                chatbot.sent_tokens.remove(user_request)
    else:
        flag=False
        print("BOT: Até mais...")    