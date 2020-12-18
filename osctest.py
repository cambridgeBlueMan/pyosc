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

while True:
    acceleration = sense.get_accelerometer_raw()
    x = acceleration['x']
    y = acceleration['y']
    z = acceleration['z']
    
try:
    target = liblo.Address('192.168.0.29',57120)
except:
    err = liblo.AddressError
    print (str(err))
    sys.exit()

liblo.send(target, "/foo/message", 123, 456.789, "smatter")
#while True:
#    acceleration = sense.get_accelerometer_raw()
#    x = acceleration['x']
#    y = acceleration['y']
#    z = acceleration['z']
#    liblo.send(target, "/pithree/xaccel", x)
#    liblo.send(target, "/pithree/yaccel", y)
#    liblo.send(target, "/pithree/zaccel", z)


liblo.send(target, "/foo/message1", 123, 456.789, "test")
# send all messages to port 1234 on the local machine



# send message "/foo/message1" with int, float and string arguments
#liblo.send(target, "/foo/message1", 123, 456.789, "test")

# send double, int64 and char
#liblo.send(target, "/foo/message2", ('d', 3.1415))
#liblo.send(target, "/foo/message3", ('h', 3.987654321))
# CHAR Doesnt work????liblo.send(target, "/foo/message4", ('c', 'x'))
#liblo.send(target, "/foo/message5", ('t',time.time()))


# we can also build a message object first...
#msg = liblo.Message("/foo/blah")
# ... append arguments later...
#msg.add(123, "foo")
# ... and then send it
#liblo.send(target, msg)

# send a list of bytes as a blob
#blob = [4, 8, 15, 16, 23, 42]
#liblo.send(target, "/foo/blob", blob)

# wrap a message in a bundle, to be dispatched after 2 seconds
#bundle = liblo.Bundle(liblo.time() + 2.0, liblo.Message("/blubb", 123))
#liblo.send(target, bundle)

