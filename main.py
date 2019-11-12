import subprocess
import sys
import serial
import welcome

#command-line arguments
args = sys.argv
welcome.ShowName()

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
        print("\n%s" % str(e))
        sys.exit('commandline error')

    comp = (cmdResult == "supported=1 detected=1")#compear result
    if comp:
        return
    else:
        print(cmdResult)
        sys.exit('camera module is not found.\ncamera module is enabled?')

class AutoNoteRaspberryPi:
    def __init__(self):
        self.connection = False
        self.BTconn = None  # Bluetooth connection infomation
        self.PORT = 1

        self.REQUEST_FINISH = 0
        self.REQUEST_SEND_IMAGE = 1

    '''
    def connectSmartphoneDeviceBluetooth
    This function is connect Android device using bluetooth socket.
    You have to pairing bluetooth devices before use.
    '''
    def connectSmartphoneDeviceBluetooth(self):
        try:
            self.BTconn = serial.Serial("/dev/rfcomm0", baudrate=9600, timeout=1)  # import Bluetooth connection infomation
            self.connection = True
        except:
            sys.exit("Bluetooth connection error.")

    '''
    def sendImage(self, imgfilepass)
    imgfilepass:target image filepass(name)
    This function is send image data.
    '''
    def sendDataBit(self, imgfilepass):
        #self.port.write(self.translateBit(image))
        img = open(imgfilepass, "rb")
        print("image file sending...")
        self.BTconn.write(img)
        print("Success!!")
        img.close()
        self.seeYouImage(imgfilepass)

    '''
    def translateBit(self, imgfilepass)
    translate image to bit.
    '''
    def translateBit(self, imgfilepass):
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
            print("\n%s" % str(e))
            sys.exit(1)

    '''
    def seeYouImage(self, imgfilepass)
    imgfilepass : String Target image file pass or file name.
    seeYouImage is kill image from filepass.
    '''
    def seeYouImage(self, imgfilepass):
        subprocess.run(["rm","-f", imgfilepass])

    '''
    def listen(self, connection)
    
    '''
    def listen(self, connection):
        print("Listening request...")
        res = self.BTconn.read(16)
        request = self.checkOrderType(res)

        if connection:
            if request == b'11':
                return True
            elif request == b'01':
                self.finish()
            else:
                print('error')
                return None
        else:
            print("No connection.")

    '''
    def checkOrderType(self, message)
    message : String
    return : bool,int
    checkOrderType is decide next action, send image or finish.
    '''
    def checkOrderType(self, message):
        if (message == self.REQUEST_SEND_IMAGE):
            print("receive request send image")
            return b'11'
        elif (message == self.REQUEST_FINISH):
            print("receive request finish app")
            return b'01'
        else:
            print('Request error')
            return b'00'

    def finish(self):
        print("finish...")
        sys.exit(0)

def run():
    app = AutoNoteRaspberryPi()
    app.connectSmartphoneDeviceBluetooth()
    requestsendimage = False
    while not requestsendimage:
        requestsendimage = app.listen(app.connection)


def testRun():
    test = AutoNoteRaspberryPi()
    img = test.getPhotoFromRasbpPiCamera()
    test.sendDataBit(img)

if __name__ == "__main__":
    if args in "-p":
        CheakCameraModule()
    run()

