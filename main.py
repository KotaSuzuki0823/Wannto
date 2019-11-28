import subprocess
import sys
import serial
import welcome as w
import os
import time
from PIL import Image

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
        self.REQUEST_SEND_IMAGE = b'cc'#1
        self.KEEP_ALIVE = b'50'#2

    '''
    def connectSmartphoneDeviceBluetooth(self)
    This function is connect Android device using bluetooth serial.
    You have to pairing bluetooth devices before use.
    '''
    def connectSmartphoneDeviceBluetooth(self):
        filepath = "/dev/rfcomm0"

        printOK("file checking....")
        while True:
            if os.path.exists(filepath):
                printOK("file ok.")
                break

        try:
            self.BTconn = serial.Serial(filepath, baudrate=115200, write_timeout=300, timeout=60)  # import Bluetooth connection infomation
            self.connection = True
            printOK("Success connecting Android device.")
        except Exception as e:
            printFATAL(str(e))
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
            printOK("Sent success.")
        except Exception as e:
            printFATAL("Oops! %s" % str(e))

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
    @property
    def getPhotoFromRasbpPiCamera(self):
        filename = "Blackboard"+".jpg"
        try:
            subprocess.run(["raspistill","-t","1000", "-o", filename])
            printOK('Get photo from camera module.')
            return filename
        except subprocess.CalledProcessError as e:
            printFATAL(" raspistill Call Error:%s" % str(e))
            sys.exit(1)

    '''
    def seeYouImage(self, imgfilepath)
    imgfilepath : String Target image file path or file name.
    seeYouImage is kill image from filepath.
    '''
    @staticmethod
    def seeYouImage(imgfilepath):
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
        req = b'50'
        if connection:
            printOK("Listen...")
            try:
                req = self.BTconn.read(2)
                printOK("Received:{},(str:{})".format(req,str(req)))
            except serial.SerialTimeoutException as te:
                printFATAL("TIMEOUT:{}".format(str(te)))
                return None
            except serial.SerialException as e:
                printFATAL("SerialException:{}".format(str(e)))
                sys.exit(1)

            if req == self.REQUEST_SEND_IMAGE:
                printOK("receive request send image")
                return True
            elif req == self.REQUEST_FINISH:
                printOK("receive request finish app")
                self.finish()
            elif req == self.KEEP_ALIVE:
                pass
            else:
                printFATAL('Request error')
                return False

        else:
            printFATAL("No connection.")
            return False

    def resize_image(self, imgpath, split):
        resultpath = "resized.jpg"
        with Image.open(imgpath) as img:
            img_resize = img.resize((int(img.width / split), int(img.height / split)))

            img_resize.save(resultpath)
            img_resize.close()

        printOK('Resized photo image. path:{} split:{}'.format(imgpath, split))
        return resultpath

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
        sys.exit("Oops!! %s" % str(e))

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
            img = app.getPhotoFromRasbpPiCamera  #take photo
            resize_img = app.resize_image(img, 2)
            app.seeYouImage(img)

            app.sendPhotoImage(resize_img)
            app.seeYouImage(resize_img)

def testRun():
    printOK("Running testRun()")
    test = AutoNoteRaspberryPi()
    test.connectSmartphoneDeviceBluetooth()

    while test.connection:

        req = test.listen(test.connection)
        if req:
            testpath = "./test.jpg"
            path = test.resize_image(testpath, 2)
            test.sendPhotoImage(path)
            printOK("sent!!")
            test.seeYouImage(path)

        else:
            pass

        time.sleep(1)

    test.BTconn.close()

def testRun2():
    printOK("Running testRun2()")
    test = AutoNoteRaspberryPi()
    test.connectSmartphoneDeviceBluetooth()

    while test.connection:

        req = test.listen(test.connection)
        if req:
            testpath = "./test.jpg"
            path = test.resize_image(testpath, 2)
            test.sendPhotoImage(path)
            eof = -1
            test.BTconn.write(eof)
            printOK("sent!!")
            test.seeYouImage(path)

        else:
            pass

        time.sleep(1)

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
    if len(args) == 1:
        run()
    elif "-p" in args:
        CheakCameraModule()
    elif "-t" in args:
        testRun()
    elif "-s" in args:
        testRun2()
    else:
        printFATAL("command line argument error.")
        sys.exit(1)
