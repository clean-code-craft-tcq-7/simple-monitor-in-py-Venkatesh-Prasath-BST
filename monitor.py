
from time import sleep
import sys


def __display_vital_alert(val, msg):
  print(msg)
  for _ in range(val):
      print('\r* ', end='')
      sys.stdout.flush()
      sleep(1)
      print('\r *', end='')
      sys.stdout.flush()
      sleep(1)


def __is_vital_ok(name, value, min_val, max_val):
  if value < min_val or value > max_val:
    __display_vital_alert(6, f'{name} is out of range!')
    return False
  return True


def is_temperature_ok(temperature):
  return __is_vital_ok('Temperature', temperature, 95, 102)


def is_pulse_rate_ok(pulse_rate):
  return __is_vital_ok('Pulse Rate', pulse_rate, 60, 100)


def is_spo2_ok(spo2):
  return __is_vital_ok('Oxygen Saturation', spo2, 90, float('inf'))


def vitals_ok(temperature, pulse_rate, spo2):
  return (
    is_temperature_ok(temperature) and
    is_pulse_rate_ok(pulse_rate) and
    is_spo2_ok(spo2)
  )
