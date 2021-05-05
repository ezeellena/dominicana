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
        print(request.json["message"]["chat"]["id"])
        text = request.json["message"]["text"]
        print(request.json["message"]["text"])
        print(request.json["message"])
        if text == "/start":
            text = 'alebotsalud'
            resp = requests.post(url="http://167.86.120.98:5006/webhooks/rest/webhook",
                                      data='{ "sender":"'+ str(chat_id) +'", "message":"' + text + '"}')
            try:
                txt2 = resp.json()[0]["text"]
                mytext2 = "\n".join(txt2.split("<br>"))
            except Exception as e:
                print(e)
            mi_bot.send_message(chat_id, mytext2)
        else:
            respuesta = requests.post(url="http://167.86.120.98:5006/webhooks/rest/webhook",
                                          data='{ "sender":"' + str(chat_id) + '", "message":"' + text + '"}')
            try:
                txt = respuesta.json()[0]["text"]
                print("------------")
                print("------------")
                print(txt)
                print("------------")
                print("------------")
                mytext = "\n".join(txt.split("<br>"))
            except Exception as e:
                print(e)
            text = "/restart"
            respuesta2 = requests.post(url="http://167.86.120.98:5006/webhooks/rest/webhook",
                                      data='{ "sender":"' + str(chat_id) + '", "message":"' + text + '"}')

            try:
                txt2 = respuesta2.json()[0]["text"]
                print("------------")
                print("------------")
                print(txt2)
                print("------------")
                print("------------")
            except Exception as e:
                print(e)

            text = 'alebotsalud'
            respuesta3 = requests.post(url="http://167.86.120.98:5006/webhooks/rest/webhook",
                                       data='{ "sender":"' + str(chat_id) + '", "message":"' + text + '"}')
            try:
                txt3 = respuesta3.json()[0]["text"]
                print("------------")
                print("------------")
                print(txt3)
                print("------------")
                print("------------")
                mytext3 = "\n".join(txt.split("<br>"))
            except Exception as e:
                print(e)

            textofinal = mytext + '\n' + mytext3
            mi_bot.send_message(chat_id, textofinal)
    except Exception as e:
        print(e)
        return "error"
    return "OK"
def main():
	app.run(host='0.0.0.0', debug=True, port="8080")

if __name__=='__main__':
	main()





