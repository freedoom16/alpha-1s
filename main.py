import bluetooth

def to_byte(value):
    return value.to_bytes(1, 'big')


def parameter(servoID, servoAngle, runTime, frameDelay):
    return message(b'\x22', [to_byte(servoID), to_byte(servoAngle), to_byte(runTime), to_byte(frameDelay)])

def main():
    msg4 = parameter(4,0, 0, 0)
    multipleServo = [  # 123
        to_byte(111), to_byte(0), to_byte(0),
        # 456
        to_byte(180), to_byte(180), to_byte(180),
        # 7891011
        to_byte(90), to_byte(60), to_byte(74), to_byte(110), to_byte(90),
        # 1213141516
        to_byte(0), to_byte(120), to_byte(184), to_byte(70), to_byte(90),

        to_byte(157), to_byte(50), to_byte(50),
        to_byte(152), to_byte(50), to_byte(50),

        to_byte(255), to_byte(255), to_byte(255), to_byte(255), to_byte(0),
        to_byte(0), to_byte(0), to_byte(0), to_byte(0), to_byte(0)]
    msg5 = message(b'\x23', multipleServo)
    bd_addr = discover()
    if bd_addr:
        port = 6
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((bd_addr, port))
        print('Connected')
        sock.settimeout(60.0)
        sock.send(msg4)
        sock.send(msg5)
        print('Sent data')
        sock.close()


def message(command, parameters):
    header = b'\xFB\xBF'
    end = b'\xED'
    parameter = b''.join(parameters)
    # len(header + length + command +parameters + check)
    length = bytearray([len(parameters) + 5])
    data = [command, length]
    data.extend(parameters)
    total = 0;
    for x in data:
        total += ord(x)
        total %= 256
    check = bytes([total])
    return header + length + command + parameter + check + end


def discover():
    print("searching ...")
    nearby_devices = bluetooth.discover_devices(lookup_names=True)
    print("found %d devices" % len(nearby_devices))
    print(nearby_devices)

    for addr, name in nearby_devices:
        if name == "Alpha1_C5C4":
            print(addr)
            return addr



if __name__ == '__main__':
    main()