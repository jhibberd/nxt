import nxt
import time

n = nxt.NXT('bt')
n.send_message('james')
n.send_message('cake')
print n.read_message()
print n.read_message()
print 'Done.'