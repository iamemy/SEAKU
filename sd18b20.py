import os

def get_sd18b20_temperature() -> float:
    """
    Retrieve the temperature read by the
    sd18b20 sensor through the 1-Wire interface.
    
    :returns: The floating temperature in Celcius °C.
    :rtype: float
    """
    
    # Read the content of the file containing
    # the temperature through the 1-Wire interface.
    filedir: str = next((e for e in os.listdir("/sys/bus/w1/devices/") if e.startswith("28-")))
    with open(os.path.join("/sys/bus/w1/devices/", filedir, "w1_slave")) as file:
        return int(file.read().split("t=")[1].split(' ')[0])/1000
                     