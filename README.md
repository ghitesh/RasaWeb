# Rasa_bot_hack

Rasa chatbot hack script

###Terminal 1
1. cd app
1. python3 -m flask run --port 8000

### Terminal 2
cd app/bot/
rasa run actions

### Terminal 3
cd app/bot/
rasa train
rasa run -m models --enable-api --cors "*" --debug

##In broswer open http://localhost:8000