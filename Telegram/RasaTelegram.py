from urllib import request

import telebot
import requests
from flask import Flask, jsonify, request
app = Flask(__name__)


@app.route('/Comentarios_bot',methods=["POST"])
def postComentarios_bot():

    data_comentarios_bot = request.json["data_comentarios_bot"]
    TOKEN = '1722558802:AAEIR7zKm3Hku0kgBHHpnE5wVwSB8StBLnU'  # Ponemos nuestro TOKEN generado con el @BotFather
    mi_bot = telebot.TeleBot(TOKEN)  # Creamos nuestra instancia "mi_bot" a partir de ese TOKEN
    token = requests.get(url="http://167.86.120.98:7676/tokenrasa").text
    chat_id = data_comentarios_bot["message"]["chat"]["id"]
    text = data_comentarios_bot["message"]["text"]
    respuesta = requests.post(url="http://167.86.120.98:5006/webhooks/rest/webhook",
                                  data='{ "sender":"'+ token +'", "message":"' + text + '"}')
    try:
        txt = respuesta.json()[0]["text"]
    except:
        # mi_bot.send_message(chat_id, "Muchas Gracias, Para volver a realizar la encuesta envie la palabra 'Hola' ")
        mi_bot.send_message(chat_id,
                            "envie /restart , luego del msjs Reiniciando envie la palabra Hola para empezar nuevamente la encuesta")
    mi_bot.send_message(chat_id, txt)
def main():
	app.run(host='0.0.0.0', debug=True, port="8080")

if __name__=='__main__':
	main()





