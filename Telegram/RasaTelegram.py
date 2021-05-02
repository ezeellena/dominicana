from urllib import request

import telebot
import requests
from flask import Flask, jsonify, request
app = Flask(__name__)


@app.route('/Comentarios_bot',methods=["POST"])
def postComentarios_bot():
    try:
        TOKEN = '1722558802:AAEIR7zKm3Hku0kgBHHpnE5wVwSB8StBLnU'  # Ponemos nuestro TOKEN generado con el @BotFather
        mi_bot = telebot.TeleBot(TOKEN)  # Creamos nuestra instancia "mi_bot" a partir de ese TOKEN
        chat_id =  request.json["message"]["chat"]["id"]
        text = request.json["message"]["text"]
        respuesta = requests.post(url="http://167.86.120.98:5006/webhooks/rest/webhook",
                                      data='{ "sender":"'+ str(chat_id) +'", "message":"' + text + '"}')
        try:
            txt = respuesta.json()[0]["text"]
        except:
            mi_bot.send_message(chat_id,
                                "envie /restart , luego del msjs Reiniciando envie la palabra Hola para empezar nuevamente la encuesta")
        mi_bot.send_message(chat_id, txt)
    except Exception as e:
        print(e)
        return "error"
    return "OK"
def main():
	app.run(host='0.0.0.0', debug=True, port="8080")

if __name__=='__main__':
	main()





