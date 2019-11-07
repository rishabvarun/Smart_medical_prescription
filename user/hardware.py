import serial
11
def give3(id=None):
    arduino=serial.Serial("COM4",9600)
    print()
    a=(str(arduino.readline()))
    print(a[-43:-5])
        
    x=input()
    y=x.encode('raw_unicode_escape')
    arduino.write(y)
    if x=='1':
        for i in range(7):
            a=str(arduino.readline())
            print(a[2:-5])
        x=input()
        y=x.encode('raw_unicode_escape')
        arduino.write(y)
        a=str(arduino.readline())
        print(a[2:-5])
        while True:
            a=str(arduino.readline())
            x=a[12:13]
            
            print(a[12:13])
            
            if a[12:13]==id:
                arduino.close()
                return True
            print('Wrong Fingerprint')
            

    else:
        for i in range(3):
            a=str(arduino.readline())
            print(a[2:-5])
        x=input()
        y=x.encode('raw_unicode_escape')
        arduino.write(y)
        for i in range(1):
            a=str(arduino.readline())
            print(a[2:-5])
        a=str(arduino.readline())
        print(a[2:-5])
        arduino.close()
        return(a[2:-5])

