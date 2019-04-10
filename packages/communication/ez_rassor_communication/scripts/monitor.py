#!/usr/bin/env python
import rospy
import psutil
from std_msgs.msg import Float64

class Monitor(object):
    def __init__(self):
        self.cpu_pub = rospy.Publisher("/ez_rassor/cpuUsage", Float64, queue_size=100)
        self.vm_pub = rospy.Publisher("/ez_rassor/virtualMemoryUsage", Float64, queue_size=100)
        self.sm_pub = rospy.Publisher("/ez_rassor/swapMemoryUsage", Float64, queue_size=100)
        self.disk_pub = rospy.Publisher("/ez_rassor/diskUsage", Float64, queue_size=100)
        self.battery_pub = rospy.Publisher("/ez_rassor/batteryLeft", Float64, queue_size=100)

def main():
    rospy.init_node('monitor_node', anonymous = True)

    monitor_object = Monitor()
    rate = rospy.Rate(30)
    close = False

    def shutdownhook():
        close = True

    rospy.on_shutdown(shutdownhook)

    while not close:
        monitor_object.cpu_pub.publish(psutil.cpu_percent(interval=1))
        monitor_object.vm_pub.publish(psutil.virtual_memory().percent)
        monitor_object.sm_pub.publish(psutil.swap_memory().percent)
        monitor_object.disk_pub.publish(psutil.disk_usage('/').percent)
        monitor_object.battery_pub.publish(psutil.sensors_battery().percent)

if __name__ == "__main__":
    main()