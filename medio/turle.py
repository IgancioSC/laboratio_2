#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import sys
import select
import termios
import tty

KEYS= ["w", "a", "s", "d"]

class TeleopTurtleSim:
    def _init_(self):
        rospy.init_node('little_turle', anonymous=False)
        self.pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=5)
        self.twist = Twist()
        self.rate = rospy.Rate(10)  # 10Hz
        self.key = None
        self.settings = termios.tcgetattr(sys.stdin)

    def getKey(self):
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            self.key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)

    def teleopLoop(self):
        rospy.loginfo("Usa las teclas de flecha para controlar el turtle. Presiona Ctrl-C para salir.")

        while not rospy.is_shutdown():
            self.getKey()
            rospy.loginfo("Tecla presionada: {}".format(self.key))  # Mensaje de depuración
            if self.key == '\x03':  # Ctrl-C
                break
            self.processKey()
            self.pub.publish(self.twist)
            self.rate.sleep()

    def processKey(self):
        if self.key == 'w':
            self.twist.linear.x = 1.0
            self.twist.angular.z = 0.0
        elif self.key == 's':
            self.twist.linear.x = -1.0
            self.twist.angular.z = 0.0
        elif self.key == 'a':
            self.twist.linear.x = 0.0
            self.twist.angular.z = 1.0
        elif self.key == 'd':
            self.twist.linear.x = 0.0
            self.twist.angular.z = -1.0
        else:
            self.twist.linear.x = 0.0
            self.twist.angular.z = 0.0


if __name__ == '__main__':
    teleop_turtlesim = TeleopTurtleSim()
    try:
        teleop_turtlesim.teleopLoop()
    except rospy.ROSInterruptException:
        pass