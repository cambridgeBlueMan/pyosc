#!/usr/bin/env python
"""
The following type tags are supported inbound:

"i" (32-bit signed integer) becomes Integer
"f" (32-bit float) becomes Float
"s" (string) becomes Symbol
"b" (blob) and "m" (4-byte MIDI message) becomes Int8Array
"d" (64-bit float) becomes Float
"T" (true) and "F" (false) become Booleans
"I" (infinity/impulse) becomes +inf
"N" (nil) becomes nil
"t" (64-bit big-endian fixed-point time tag) becomes Float
"c" (character) becomes Char

"""
import liblo, sys
import time
from sense_hat import SenseHat

sense = SenseHat()

def translate(value, leftMin=-1, leftMax=1, rightMin=0, rightMax=1):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)
# send all messages to port 1234 on the local machine
try:
    target = liblo.Address('192.168.0.29', 57120)
except:
    err = liblo.AddressError
    print (str(err))
    sys.exit()

print(target)
# send message "/foo/message1" with int, float and string arguments
liblo.send(target, "/foo/message1", 123, 456.789, "test")

# send double, int64 and char
liblo.send(target, "/foo/message2", ('d', 3.1415))
liblo.send(target, "/foo/message3", ('h', 3.987654321))
#liblo.send(target, "/foo/message4", ('c', 'x'))
liblo.send(target, "/foo/message5", ('t',time.time()))


# we can also build a message object first...
msg = liblo.Message("/foo/blah")
# ... append arguments later...
msg.add(123, "foo")
# ... and then send it
liblo.send(target, msg)

# send a list of bytes as a blob
blob = [4, 8, 15, 16, 23, 42]
liblo.send(target, "/foo/blob", blob)

# wrap a message in a bundle, to be dispatched after 2 seconds
bundle = liblo.Bundle(liblo.time() + 2.0, liblo.Message("/blubb", 123))
liblo.send(target, bundle)
acceleration = sense.get_accelerometer_raw()
x = acceleration['x']
print(type(x))
liblo.send(target, "/pithree/xaccel/", ('f', x))

while True:
    acceleration = sense.get_accelerometer_raw()
    
    liblo.send(target, "/pithree/xaccel/", ('f', translate(acceleration['x'])))
    liblo.send(target, "/pithree/yaccel/", ('f', translate(acceleration['y'])))
    liblo.send(target, "/pithree/zaccel/", ('f', translate(acceleration['z'])))


