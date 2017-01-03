import time

from ant.core import driver
from ant.core import node

from PowerMeterTx import PowerMeterTx
from SpeedCadenceSensorRx import SpeedCadenceSensorRx
from config import DEBUG, LOG, NETKEY, POWER_CALCULATOR

try:
    stick = driver.USB2Driver(None, log=LOG, debug=DEBUG)
    antnode = node.Node(stick)
    print "Starting ANT node"
    antnode.start()
    key = node.NetworkKey('N:ANT+', NETKEY)
    antnode.setNetworkKey(0, key)

    print "Starting speed sensor"
    try:
        # Create the speed sensor object and open it
        speed_sensor = SpeedCadenceSensorRx(antnode)
        speed_sensor.open()
    except Exception as e:
        print"speed_sensor  error: " + e.message
        speed_sensor = None

    # Notify the power calculator every time we get a speed event
    print "Using " + POWER_CALCULATOR.__class__.__name__
    speed_sensor.notify_change(POWER_CALCULATOR)

    print "Starting power meter"
    try:
        # Create the power meter object and open it
        power_meter = PowerMeterTx(antnode)
        power_meter.open()
    except Exception as e:
        print "power_meter error: " + e.message
        power_meter = None

    # Notify the power meter every time we get a calculated power value
    POWER_CALCULATOR.notify_change(power_meter)

    print "Main wait loop"
    while True:
        try:
            time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            break

finally:
    if speed_sensor:
        print "Closing speed sensor"
        speed_sensor.close()
        speed_sensor.unassign()
    if power_meter:
        print "Closing power meter"
        power_meter.close()
        power_meter.unassign()
    print "Stopping ANT node"
    antnode.stop()