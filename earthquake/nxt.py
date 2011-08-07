import subprocess

class NXT(object):
    """Functions for sending and receiving messages with an NXT brick.
    
    All communication with the NXT brick is made using the NeXTTool utility:
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
    
    def send_message(self, msg):        
        """Send a message string to an NXT brick."""
        return self._cmd(['/Inbox=%s' % self.OUT_QUEUE, '-msg='+msg])
    
    def read_message(self):
        """Read (pop) a message from an NXT brick.
        
        The message string is a list of ASCII character codes separated by
        newline characters. The message is decoded before being returned.
        """
        msg = self._cmd(['/Empty', '-readmsg=%s' % self.IN_QUEUE])
        chars = map(lambda x: chr(int(x)), msg.rstrip('\n').split('\n'))
        return ''.join(chars)
    
    def _cmd(self, args):
        args = ['nexttool', '/Com='+self.nxt_alias]+args
        pipe = subprocess.Popen(args, stdout=subprocess.PIPE)
        return pipe.stdout.read()    