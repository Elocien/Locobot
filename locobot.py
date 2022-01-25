from pyrobot import Robot
import argparse
from dwm1001_apiCommands import DWM1001_API_COMMANDS
import rospy
import time
import serial
import os
import numpy as np
import threading
from time import sleep


class dwm1001:
    
    def __init__(self):
        """
        Initialize the node, open serial port
        """
        # Init node
        rospy.init_node('DWM1001_Listener_Mode', anonymous=False)
        
        # Set a ROS rate
        self.rate = rospy.Rate(1)
        
        
        
        # Serial port settings
        self.verbose = rospy.get_param('~verbose', True)
        self.serialPortDWM1001 = serial.Serial(
            port="/dev/ttyACM0",
            baudrate=115200,
            parity=serial.PARITY_ODD,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.SEVENBITS
        )
        
        
    def initializeDWM1001API(self):
        """
        Initialize dwm1001 api, by sending sending bytes
        :param:
        :returns: none
        """
        # reset incase previuos run didn't close properly
        self.serialPortDWM1001.write(DWM1001_API_COMMANDS.RESET)
        # send ENTER two times in order to access api
        self.serialPortDWM1001.write(DWM1001_API_COMMANDS.SINGLE_ENTER)
        # sleep for half a second
        time.sleep(0.5)
        self.serialPortDWM1001.write(DWM1001_API_COMMANDS.SINGLE_ENTER)
        # sleep for half second
        time.sleep(0.5)
        # send a third one - just in case
        self.serialPortDWM1001.write(DWM1001_API_COMMANDS.SINGLE_ENTER)   


    def main(self):
        
        # close the serial port in case the previous run didn't closed it properly
        self.serialPortDWM1001.close()
        # sleep for one sec
        time.sleep(1)
        # open serial port
        self.serialPortDWM1001.open()
        
        # check if the serial port is opened
        if(self.serialPortDWM1001.isOpen()):
            rospy.loginfo("Port opened: " + str(self.serialPortDWM1001.name))
            # start sending commands to the board so we can initialize the board
            self.initializeDWM1001API()
            # give some time to DWM1001 to wake up
            time.sleep(2)
            # send command lec, so we can get positions is CSV format
            self.serialPortDWM1001.write(DWM1001_API_COMMANDS.LEC)
            self.serialPortDWM1001.write(DWM1001_API_COMMANDS.SINGLE_ENTER)
            rospy.loginfo("Reading DWM1001 coordinates and process them!")
        else:
            rospy.loginfo("Can't open port: " +
                          str(self.serialPortDWM1001.name))
    
        # Args
        parser = argparse.ArgumentParser()
        parser.add_argument("-s", "--speed", metavar="SPEED",
                            type=float, help="linear velocity")
        parser.add_argument("-r", "--rotation", metavar="ROTATION",
                            type=float, help="rotational velocity")
        parser.add_argument("-t", "--time", metavar="TIME",
                            type=int, help="execution time")
        args = parser.parse_args()

        # Drive
        self.robot = Robot('locobot')

        
        print("Robot Params: \n")
        print("Speed: " + str(args.speed))
        print("Rotation: " + str(args.rotation))
        print("Time : " + str(args.time))
        print("ODOM Start state: " + str(self.robot.base.get_state('odom')))
        
        
        # create new threads
        self.drive_thread = threading.Thread(target=self.drive, args=(args.speed, args.rotation, args.time))
        uwb_location_thread = threading.Thread(target=self.uwb_location, args=(args.time, args.rotation))

        # start threads
        uwb_location_thread.start()
        
        # wait for threads to terminate, then continue
        uwb_location_thread.join()
        self.drive_thread.join()

        print("ODOM End state: " + str(self.robot.base.get_state('odom')))


    def drive(self, speed, rotation, time):
        self.robot.base.set_vel(fwd_speed=speed,
                           turn_speed=rotation,
                           exe_time=time)
        
    def uwb_location(self, zeit, rotation):
        while True:
            if "lec" in self.serialPortDWM1001.read_until():
                self.drive_thread.start()
                break


        for x in range(zeit*10):
            pos = self.serialPortDWM1001.read_until()
            try:
                print(pos.split("POS")[1])
            except Exception as e:
                print(pos)
            time.sleep(0.1)        


def start():
    dwm = dwm1001()
    dwm.main()

if __name__ == '__main__':
    start()
    