from commands.device import register as device_register
from flask import Flask, request, send_from_directory
import threading
import sys, os
# from gevent.pywsgi import WSGIServer
import logging

module_logger = logging.getLogger("wrt.http")
http_server = Flask(__name__, static_url_path='')

wl = logging.getLogger('werkzeug')
wl.setLevel(logging.NOTSET)
wl.disabled = True
logFormatStr = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# logging.basicConfig(format=logFormatStr, filename='wrt.log', level=logging.NOTSET)
formatter = logging.Formatter(logFormatStr, '%m-%d %H:%M:%S')
fileHandler = logging.FileHandler('wrt.log')
fileHandler.setLevel(logging.NOTSET)
fileHandler.setFormatter(formatter)
wl.addHandler(fileHandler)
http_server.logger.disabled = True

class HttpServerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # thread = threading.Thread(target=self.run, args=())
        # thread.daemon = False                            # Daemonize thread
        wl = logging.getLogger('werkzeug')
        wl.disabled = True
        self.start()

    def run(self):
        os.environ["WERKZEUG_RUN_MAIN"] = "true"
        # self.wsgi_server = WSGIServer(('0.0.0.0', 5000), http_server, )
        # self.wsgi_server.serve_forever()
        http_server.run('0.0.0.0')

    def join(self):
        try:
            return threading.Thread.join(self)
        except KeyboardInterrupt:
            sys.exit()
        # self.wsgi_server.stop()
        # threading.Thread.join(self)


@http_server.route('/fw/<path:path>')
def send_fw(path):
    return send_from_directory('', path)


@http_server.route("/register", methods=['POST'])
def register():
    params = dict(request.form)
    params['ip'] = request.remote_addr
    # print (dict(request.form))
    device_register(**params)
    return "OK\n"


if __name__ == "__main__":
    try:
        http_thread = HttpServerThread()
        # http_thread.start()
        # http_thread.join()
    except KeyboardInterrupt:
        print('sdf')
        http_thread.join()
        sys.exit()
