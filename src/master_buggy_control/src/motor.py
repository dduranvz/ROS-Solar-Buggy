#!/usr/bin/env python

import rospy
from smbus2 import SMBus
from std_msgs.msg import Int16
from std_msgs.msg import Byte

m_address = 10
bus = SMBus(0)


def write_number(value):
    bus.write_i2c_block_data(m_address, 0, value)
    return -1


def read_number():
    return bus.read_i2c_block_data(m_address, 0, 2)


def rpm(data):
    rospy.loginfo(rospy.get_caller_id() + ' RPM = %d', data.data)
    array = list()  # Creates a list (I think)
    array.append(1)
    array.append((data.data >> 8) & 0xFF)
    array.append(data.data & 0xFF)

    write_number(array)

    
def dir(data):
    rospy.loginfo(rospy.get_caller_id() + ' DIR = %d', data.data)
    array = list()  # Creates a list (I think)
    array.append(0)
    array.append(data.data)
    write_number(array)


def motor():
    # The anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('motor', anonymous=True)

    rospy.Subscriber('rpm', Int16, rpm)
    rospy.Subscriber('dir', Int16, dir)
    
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    motor()
