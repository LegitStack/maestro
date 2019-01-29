'''
I'm not exactly sure how the protocol module should look yet. should I start by
building the actual infrastructure of communication? probably not, we may want
to simulate separate nodes with mere objects. We may just use different processes
or we might use an actor framework like rx or whatever it is or akka or something.
so we need to define here the rules about what to do with messages, not the actual
passing of messages themselves.

It basically comes down to 3 cases. I get a message from the master node and
start searching, or I get a message from fellow workers and collaborate or I
stop what I'm doing because the answer has been achieved.

During training I also want to do things such as record what the last state was
and so on, so training is a bit different. perhaps I should just work on the
training protocol first? I'll sleep on it.
'''
