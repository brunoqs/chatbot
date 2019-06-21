from chatterbot.trainers import UbuntuCorpusTrainer
from chatterbot import ChatBot

import pickle


bot = ChatBot('Chat Bot')

trainer = UbuntuCorpusTrainer(bot)
# trainer.train()

# with open('BotTrained', 'wb') as fp:
#     pickle.dump(bot, fp)

while True:
    pergunta = input("Usuário: ")
    resposta = bot.get_response(pergunta)
    if float(resposta.confidence) > 0.5:
        print('Bot: ', resposta)
    else:
        print('Bot: Ainda não sei responder esta pergunta')
