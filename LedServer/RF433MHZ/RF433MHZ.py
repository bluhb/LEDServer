import time
# import RPi.GPIO as GPIO

Delay = [0,0]
Delay[0] = 0.01
Delay[1] = 0.02

def convertIntToByte(Int):
    if Int > 255:
        return None
    Byte = bytearray(8)
    ConvertedInt = format(Int, 'b')
    for i in range(0,len(ConvertedInt)):
        Byte[8 - len(ConvertedInt) + i] = int(ConvertedInt[i])
    return Byte

def sendByte(Byte):
    for i in range(0,8,1):
        if int(Byte[i]) == 1:
            print("High")
            #set gpio high
        elif int(Byte[i]) == 0:
            print("Low")
            #set gpio low
        time.sleep(Delay[int(Byte[i])])
    #set gpio low
    print("--------------")
    return None

def checksum(ByteArray1, ByteArray2):
    #XOR the two bytearrays with eachother
    return([a ^ b for (a,b) in zip(ByteArray1, ByteArray2)])

def sendToArduino(Address, Color_RGB, Attempts = 4):
    for i in range(0, Attempts):
        Checksum = checksum(convertIntToByte(Address), convertIntToByte(Color_RGB[0]))
        sendByte(convertIntToByte(Address))
        for Color in Color_RGB:
            sendByte(convertIntToByte(Color))
        sendByte(Checksum)
    return None

def main():
    sendToArduino(5, [125], 1)
    return None

if __name__ == "__main__":
    main()
