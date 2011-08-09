import subprocess
import threading
import time

# TODO(jhibberd) Add a mutex to send/read calls.

class MsgChannel(object):
    """Functions for sending and receiving messages with an NXT brick.
    
    All communication with the NXT brick is made over Bluetooth using the 
    NeXTTool utility:
    http://wiki.zenerves.net/index.php/NexTTool_manual
    """
    
    # Each NXT brick had 10 available mailboxes (queues). Sent messages sit in
    # a mailbox until they are read and cleared. Any mailbox can be written to
    # or read (typically popped) by either the local NXT brick or a remote
    # host. For this reason duplex communication between NXT brick and host is
    # best achieved by designating one mail box for inbound message and another
    # for outbound messages.
    OUT_QUEUE = 0
    IN_QUEUE = 1
        
    def __init__(self, nxt_alias):
        # NXT brick aliases are stored in ~/nxt.dat and used for bluetooth
        # communication.
        self.nxt_alias = nxt_alias
    
    def send(self, msg):        
        """Send a message string to an NXT brick."""
        return self._cmd(['/Inbox=%s' % self.OUT_QUEUE, '-msg='+msg])
    
    def read(self):
        """Read (pop) a message from an NXT brick.
        
        The message string is a list of ASCII character codes separated by
        newline characters. The message is decoded before being returned.
        """
        msg = self._cmd(['/Empty', '-readmsg=%s' % self.IN_QUEUE])
        if not msg:
            return None
        chars = map(lambda x: chr(int(x)), msg.rstrip('\n').split('\n'))
        return ''.join(chars)
    
    def _cmd(self, args):
        args = ['nexttool', '/Com='+self.nxt_alias]+args
        pipe = subprocess.Popen(args, stdout=subprocess.PIPE)
        return pipe.stdout.read() 
    
    
class InboundMsgDispatch(object):
    """Class that repeatedly and indefinitely polls the NXT brick for inbound
    messages destined for the host. On receiving a msg a user supplied callback
    function is called with the message as an argument.
    """
    
    POLL_WAIT = 1
            
    @classmethod
    def start(cls, msg_channel, callback):
        def f(msg_channel, callback):
            while True:
                msg = msg_channel.read()
                if msg:
                    callback(msg)
                time.sleep(cls.POLL_WAIT)
        threading.Thread(target=f, args=(msg_channel, callback)).start()
