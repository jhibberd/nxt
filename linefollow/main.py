#!/usr/bin/python

import nxt
import os.path
import tornado.ioloop
import tornado.web
import tornado.websocket        
    
class StreamSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()

    def open(self):
        StreamSocketHandler.waiters.add(self)
        StreamSocketHandler.send_msg('Web socket open.')

    def on_close(self):
        StreamSocketHandler.waiters.remove(self)

    @classmethod
    def send_msg(cls, msg):
        for waiter in cls.waiters:
            waiter.write_message(msg)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("main.html")

        
class StartHandler(tornado.web.RequestHandler):
    
    def post(self):
        msg_channel = nxt.MsgChannel('bt')
        nxt.InboundMsgDispatch.start(msg_channel, StreamSocketHandler.send_msg)
        StreamSocketHandler.send_msg('NXT channel open.')        
       
        
class StopHandler(tornado.web.RequestHandler):
    
    def post(self):
        nxt.InboundMsgDispatch.stop()
        StreamSocketHandler.send_msg('NXT channel closed.') 
       
       
app_dir = os.path.dirname(os.path.abspath(__file__)) 
settings = {
    'static_path': app_dir
    }
application = tornado.web.Application([
    (r"/",          MainHandler),
    (r"/start",     StartHandler),
    (r"/stop",      StopHandler),
    (r"/stream",    StreamSocketHandler),
], **settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

