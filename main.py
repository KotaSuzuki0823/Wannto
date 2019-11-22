import subprocess
import sys
import serial
import welcome as w
import os

#command-line arguments
args = sys.argv
w.ShowName()
def printOK(text):
    print("[" + w.Color.GREEN + "   OK   " + w.Color.END + "]" + text)

def printFATAL(text):
    print("[" + w.Color.RED + "  FATAL " + w.Color.END + "]" + text)

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
            self.BTconn = serial.Serial("/dev/rfcomm0", baudrate=9600)  # import Bluetooth connection infomation
            self.connection = True
            printOK("Success connecting Android device.")
        except Exception as e:
            printFATAL(e)
            sys.exit(1)

    '''
    def sendImage(self, imgfilepath)
    imgfilepath:target image filepath(name)
    This function is send image data.
    '''
    def sendPhotoImage(self, imgfilepath):
        #self.port.write(self.translateBit(image))
        with open(imgfilepath, "rb") as fp:
            imgfiledata = fp.read()

        printOK("image file sending...")
        try:
            self.BTconn.write(imgfiledata)
        except Exception as e:
            printFATAL("Oops! %s\n" % str(e))
            return None

        printOK("Sent success.\n")
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
        filename = "Blackboard"+".jpg"
        try:
            subprocess.run(["raspistill","-t","1000", "-o", filename])
            printOK('Get photo from camera module.')
            return filename
        except subprocess.CalledProcessError as e:
            printFATAL("\n raspistill Call Error:%s" % str(e))
            sys.exit(1)

    '''
    def seeYouImage(self, imgfilepath)
    imgfilepath : String Target image file path or file name.
    seeYouImage is kill image from filepath.
    '''
    def seeYouImage(self, imgfilepath):
        try:
            os.remove(imgfilepath)
            printOK('image file is deleted.')
        except Exception as e:
            printFATAL("delete error:%s" % str(e))

    '''
    def listen(self, connection)
    listen() is waiting order message from Android device and recognition order message.
    '''
    def listen(self, connection):
        req = self.BTconn.read(2)
        printOK("Received request:{}".format(req))

        if connection:
            if (req == self.REQUEST_SEND_IMAGE):
                printOK("receive request send image\n")
                return True
            elif (req == self.REQUEST_FINISH):
                printOK("receive request finish app\n")
                self.finish()
            else:
                printFATAL('Request error\n')
                return False

        else:
            printFATAL("No connection.\n")
            return False

    '''
    def finish(self)
    finish is kill this process.
    '''
    def finish(self):
        self.BTconn.close()
        printOK("Bluetooth connection is closed.")
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
    printOK("Running testRun()")
    test = AutoNoteRaspberryPi()
    test.connectSmartphoneDeviceBluetooth()

    while True:
        test.connectSmartphoneDeviceBluetooth()
        req = test.listen(test.connection)
        if req:
            testpath = "./test.jpg"
            test.sendPhotoImage(testpath)
            printOK("sent!!")
        else:
            pass
        test.BTconn.close()

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
