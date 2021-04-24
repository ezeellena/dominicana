import telebot
import requests
if __name__ == "__main__":

    TOKEN = '1722558802:AAEIR7zKm3Hku0kgBHHpnE5wVwSB8StBLnU'  # Ponemos nuestro TOKEN generado con el @BotFather
    mi_bot = telebot.TeleBot(TOKEN)  # Creamos nuestra instancia "mi_bot" a partir de ese TOKEN


    def listener(*mensajes):  ##Cuando llega un mensaje se ejecuta esta función
        try:
         for m in mensajes:
            chat_id = m[0].chat.id
            if m[0].content_type == 'text':
                text = m[0].text
                respuesta = requests.post(url="http://167.86.120.98:5006/webhooks/rest/webhook",data='{ "sender":"Me", "message":"'+text+'"}')
                try:
                    txt = respuesta.json()[0]["text"]
                except:
                    #mi_bot.send_message(chat_id, "Muchas Gracias, Para volver a realizar la encuesta envie la palabra 'Hola' ")
                    mi_bot.send_message(chat_id, "envie /restart , luego del msjs Reiniciando envie la palabra Hola para empezar nuevamente la encuesta")
                mi_bot.send_message(chat_id, txt)
                #mi_bot.send_message(chat_id, text)
        except:
            print("no hay mas preguntas")

    mi_bot.set_update_listener(listener)  # registrar la funcion listener
    mi_bot.polling()

    while True:  # No terminamos nuestro programa
        pass