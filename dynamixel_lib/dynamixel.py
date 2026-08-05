from dynamixel_lib.dynamixel_models import _DynamixelModel
from dynamixel_lib.dynamixel_models import _CtrlTableValue
from dynamixel_sdk import Protocol2PacketHandler, PortHandler
import threading

class U2D2():
    # This set ensures that new instances of the class do not have repeated device paths
    _instance_device_strings = set()
    # Lock is required to make sure other threads cannot change the device string set 
    _lock = threading.Lock() 
    # This lock is actually kind of wrong - makes it so that every instance of a u2d2 shares the lock 
    # only one motor can write across all u2d2 controllers on a per thread basis - this is fine for any 
    # reasonable use case of the library that will be encountered in this lab 


    def __init__(self, device_path: str, baudrate: int) -> None:

        with U2D2._lock:
            if device_path in U2D2._instance_device_strings:
                raise ValueError(f"The device path {device_path} is already in use {list(U2D2._instance_device_strings)}")

            self.port_handler = PortHandler(device_path)
            self.port_handler.openPort()
            self.port_handler.setBaudRate(baudrate)
            self.packet_handler = Protocol2PacketHandler()
            U2D2._instance_device_strings.add(device_path)


class Dynamixel():
    # This set ensures that new instances of the class do not have repeated ids
    _unique_ids_used = set()
    # Lock is required to make sure other threads cannot change the unique ids used string set
    _lock = threading.Lock()


    def __init__(self, model: _DynamixelModel, id: int, u2d2: U2D2):
        min_id = 0
        max_id = 253
    
        with Dynamixel._lock:

            if not(min_id <= id <= max_id):
                raise ValueError(f"The id {id} is not in the range of allowed values ({min_id} to {max_id}) (inclusive) ")

            if id in Dynamixel._unique_ids_used:
                raise ValueError(f"The id {id} is already in use {list(Dynamixel._unique_ids_used)}")
            
            if not issubclass(model, _DynamixelModel):
                raise ValueError(f"The provided model {model} is not an instance of a _DynamixelModel. Please use the provided model classes.")
            
            self._id: int = id
            self._u2d2: U2D2 = u2d2
            self.ctrl_table: _DynamixelModel = model

            Dynamixel._unique_ids_used.add(id)

    def _make_data(self, val):
        return [0xFF & val, (0xFF00 & val) >> 8, (0xFF0000 & val) >> 16, (0xFF000000 & val) >> 24]


    def write(self, location: _CtrlTableValue, written_data):

        #TODO need to add error checking for written_data later - not sure if need bytes, int, etc. check later.

        #TODO parse and give to user.

        with self._u2d2._lock:
            # if location.access in {"RW","R"}:
            #     raise ValueError(f"The location you have provided {location} is not able to be written to.")
            return self._u2d2.packet_handler.writeTxRx(self._u2d2.port_handler,self._id, location.address, location.length_bytes, self._make_data(written_data))
    
    def read(self, location: _CtrlTableValue, readTries: int):

        with self._u2d2._lock:
            result = -1
    
        tempReadStorage = self._u2d2.packet_handler.readTxRx(self._u2d2.port_handler,self._id, location.address, location.length_bytes)
        # print(tempReadStorage)

        positionList = tempReadStorage[0]
        
        if len(positionList) == 0:
            if readTries < 5:
                readTries = readTries + 1
                result = self.read(location, readTries)
            else:
                readTries = 0
                result = -1
        else: 
            result = (positionList[0]) + (positionList[1] * 256)

        return result
            

    def reboot(self, dxl_id):
        with self._u2d2._lock:
            return self._u2d2.packet_handler.reboot(self._u2d2.port_handler, dxl_id)