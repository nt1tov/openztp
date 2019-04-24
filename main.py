from commands.device import register as device_register
from flask import Flask, request, send_from_directory
app = Flask(__name__, static_url_path='')

#@app.route("/")
def hello():
    res = ("update=openwrt-18.06.2-x86-64-combined-squashfs.img\n"
            """exec=opkg install mc\n""")
    print (res)
    return res 

@app.route('/fw/<path:path>')
def send_fw(path):
    return send_from_directory('', path)
    
@app.route("/register", methods=['POST'])
def register():
    params = dict(request.form)
    params['ip'] = request.remote_addr
    print (dict(request.form))
    device_register(**params)
    return "OK\n"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
