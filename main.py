import subprocess
import sys
import serial
import welcome
import os
import threading

#command-line arguments
args = sys.argv
welcome.ShowName()

class AutoNoteRaspberryPi:
    def __init__(self):
        self.connection = False
        self.BTconn = None  # Bluetooth connection infomation

        self.REQUEST_FINISH = b'48'#0
        self.REQUEST_SEND_IMAGE = b'49'#1

    '''
    def connectSmartphoneDeviceBluetooth(self)
    This function is connect Android device using bluetooth serial.
    You have to pairing bluetooth devices before use.
    '''
    def connectSmartphoneDeviceBluetooth(self):
        try:
            self.BTconn = serial.Serial("/dev/rfcomm0", baudrate=9600, timeout=1)  # import Bluetooth connection infomation
            self.connection = True
            print("Success connecting Android device.")
        except Exception as e:
            sys.exit("\n%s" % str(e))

    '''
    def sendImage(self, imgfilepath)
    imgfilepath:target image filepath(name)
    This function is send image data.
    '''
    def sendPhotoImage(self, imgfilepath):
        #self.port.write(self.translateBit(image))
        with open(imgfilepath, "rb") as fp:
            imgfiledata = fp.read()

        print("image file sending...")
        try:
            self.BTconn.write(imgfiledata)
        except Exception as e:
            print("Oops! %s\n" % str(e))
            return None

        print("Success!!\n")
    '''
    def translateBit(self, imgfilepath)
    translate image to bit.
    '''
    def translateBit(self, imgfilepath):
        pass

    '''
    def getPhotoFromRasbpPiCamera(self)
    getPhotoFromRasbpPiCamera is order take photo and import photo from Raspberry Pi camera.
    '''
    def getPhotoFromRasbpPiCamera(self):
        print('Getting photo from camera module.....')
        filename = "Blackboard"+".jpg"
        try:
            subprocess.run(["raspistill","-t","1000", "-o", filename])
            return filename
        except subprocess.CalledProcessError as e:
            sys.exit("\n raspistill Call Error:%s" % str(e))

    '''
    def seeYouImage(self, imgfilepath)
    imgfilepath : String Target image file path or file name.
    seeYouImage is kill image from filepath.
    '''
    def seeYouImage(self, imgfilepath):
        os.remove(imgfilepath)

    '''
    def listen(self, connection)
    listen() is waiting order message from Android device and recognition order message.
    '''
    def listen(self, connection):
        print("Listening request...")
        req = self.BTconn.read(1)

        if connection:
            if (req == self.REQUEST_SEND_IMAGE):
                print("receive request send image\n")
                return True
            elif (req == self.REQUEST_FINISH):
                print("receive request finish app\n")
                self.finish()
            else:
                print('Request error\n')
                return False

        else:
            print("No connection.\n")
            return False

    '''
    def checkOrderType(self, message)
    message : String
    return : bool,int
    checkOrderType is decide next action, send image or finish.
    '''
    #Not use
    def checkOrderType(self, message):
        if (message == self.REQUEST_SEND_IMAGE):
            print("receive request send image\n")
            return b'11'
        elif (message == self.REQUEST_FINISH):
            print("receive request finish app\n")
            return b'01'
        else:
            print('Request error\n')
            return b'00'


    def finish(self):
        print("finish...\n")
        self.connection = False
        sys.exit(0)

'''
def cheakCameraModule()
This function is check camera module.
if you are getting error despite connected camera module, Please check settings enabled camera module.
'''
def CheakCameraModule():
    cmd = 'vcgencmd get_camera'#shell command
    try:
        cmdResult = (subprocess.Popen(cmd, stdout=subprocess.PIPE,shell=True).communicate()[0]).decode('utf-8')
    except subprocess.CalledProcessError as e:
        sys.exit("\n Oops!! %s" % str(e))

    print(cmdResult)
    sys.exit(0)

'''
    main
'''
def run():
    app = AutoNoteRaspberryPi()
    app.connectSmartphoneDeviceBluetooth()
    while app.connection:#loop at connection true
        requestsendimage = app.listen(app.connection)
        if requestsendimage:
            img = app.getPhotoFromRasbpPiCamera()#take photo
            app.sendPhotoImage(img)
            app.seeYouImage(img)

def testRun():
    print("Running testRun()")
    test = AutoNoteRaspberryPi()
    test.connectSmartphoneDeviceBluetooth()

    req = test.listen(test.connection)
    if req:
        testpath = "./test.jpg"
        test.sendPhotoImage(testpath)
        print("sent!!")
    else:
        test.finish()

#not use
def bindRfcomm():
    while True:
        print('[RFCOMM BIND]enter target Bluetooth addoress')
        address = input()
        cmd = 'sudo rfcomm bind 0 ' + address
        try:
            cmdResult = (subprocess.Popen(cmd, stdout=subprocess.PIPE,shell=True).communicate()[0]).decode('utf-8')
        except subprocess.CalledProcessError as e:
            sys.exit("\n Oops!! %s" % str(e))

        if os.path.isfile('/dev/rfcomm0'):
            print("Success!!\n")
            return
        else:
            print(cmdResult)


if __name__ == "__main__":
    if "-p" in args:
        CheakCameraModule()
    if "-t" in args:
        testRun()
    else:
        run()
