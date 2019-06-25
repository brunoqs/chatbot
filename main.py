import time

from chatbot import Chatbot


def main():
    chatbot = Chatbot()

    print('BOT: Olá querido usuário!')
    print('BOT: Fico a disposição para responder perguntas sobre mercado, saúde, tecnologia e telefonia.')
    print('BOT: Diga tchau quando encerrar!')
    
    stop = False

    while not stop:
        user_request = input('Pergunta: ')
        user_request = user_request.lower()

        if user_request != 'tchau':
            if user_request == 'obrigado' or user_request == 'muito obrigado':
                stop = True
                print("BOT: Não há de quê!")
            else:
                if chatbot.greeting(user_request) != '':
                    print("BOT:", chatbot.greeting(user_request))
                else:
                    print("BOT: Pensando...")
                    start_time = time.perf_counter()
                    response = chatbot.response(user_request)
                    end_time = time.perf_counter()
                    print("BOT:", response)
                    print('[{:.1f} segundos]'.format(end_time - start_time))
        else:
            stop = True
            print("BOT: Até mais!")


if __name__ == '__main__':
    main()
