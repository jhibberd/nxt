# NOTE: Needs to be run as root.

#import nxt
#import time
#
#def callback(msg):
#    print 'IN: %s' % msg
#
#msg_channel = nxt.MsgChannel('bt')
#nxt.InboundMsgDispatch.start(msg_channel, callback)
#print 'Printing start'
#msg_channel.send('james')
#msg_channel.send('cake')
#print 'Printing end'
#
#time.sleep(10)

import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
    
# TODO(jhibberd) Implement HTTPMsgDispatch that forwards to localhost
# TODO(jhibberd) Create HTML UI that opens web socket.
# TODO(jhibberd) Server to push received messages to client over socket:
# https://github.com/facebook/tornado/blob/master/demos/websocket/chatdemo.py