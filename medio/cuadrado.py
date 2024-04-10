#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import sys
import select
import termios
import tty


class TeleopTurtleSim:
    def __init__(self):
        rospy.init_node('turle', anonymous=False)
        self.pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=5)
        self.twist = Twist()
        self.rate = rospy.Rate(1)  # Reducido a 1Hz para facilitar la visualización
        self.key = None
        self.settings = termios.tcgetattr(sys.stdin)

    def getKey(self):
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            self.key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)

    def teleopLoop(self):
        rospy.loginfo("Presiona Ctrl-C para salir y observa cómo la tortuga forma un cuadrado.")

        for _ in range(5):
            # Avanzar hacia adelante
            self.twist.linear.x = 1.0
            self.twist.angular.z = 0.0
            self.pub.publish(self.twist)
            self.rate.sleep()

            # Detenerse
            self.twist.linear.x = 0.0
            self.twist.angular.z = 0.0
            self.pub.publish(self.twist)
            self.rate.sleep()

            # Girar 90 grados hacia la izquierda
            self.twist.linear.x = 0.0
            self.twist.angular.z = 2  # 1.57 radianes es aproximadamente 90 grados
            self.pub.publish(self.twist)
            self.rate.sleep()

            # Detenerse
            self.twist.linear.x = 0.0
            self.twist.angular.z = 0.0
            self.pub.publish(self.twist)
            self.rate.sleep()

        rospy.loginfo("Cuadrado completado. Saliendo del bucle.")


if __name__ == '__main__':
    teleop_turtlesim = TeleopTurtleSim()
    try:
        teleop_turtlesim.teleopLoop()
    except rospy.ROSInterruptException:
        pass
