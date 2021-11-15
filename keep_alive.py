from flask import Flask
from threading import Thread

app = Flask('__name__')

@app.route('/')
def index():
    return "Hello world!"

if __name__ == 'bot':
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
  t = Thread(target=run)
  t.start() 
