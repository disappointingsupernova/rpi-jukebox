import struct
import time
import sys
import threading

class RemoteListener(threading.Thread):
  def __init__(self, bus):
    super(RemoteListener, self).__init__()
    self.bus = bus
    self.setDaemon(True)

  def run(self):
    infile_path = "/dev/input/by-id/usb-Sycreader_RFID_Technology_Co.__Ltd_SYC_ID_IC_USB_Reader_08FF20140315-event-kbd"
    
    #long int, long int, unsigned short, unsigned short, unsigned int
    FORMAT = 'llHHI'
    EVENT_SIZE = struct.calcsize(FORMAT)

    in_file = open(infile_path, "rb")

    event = in_file.read(EVENT_SIZE)
    id = ""

    while event:
      (tv_sec, tv_usec, type, code, value) = struct.unpack(FORMAT, event)

      if type == 1 and value == 1:
        if code == KEY_ENTER:
          self.bus.put(["card_read", id])
          id = ""

        elif code == 11:
          id += `0`

        else:
          id += `code - 1`

      event = in_file.read(EVENT_SIZE)

    in_file.close()
