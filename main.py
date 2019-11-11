#########################
#                       #
#   you must run sudo.  #
#                       #
#########################

import subprocess
import sys
import serial

#shell coler
class Color:
    BLACK     = '\033[30m'
    RED       = '\033[31m'
    GREEN     = '\033[32m'
    YELLOW    = '\033[33m'
    BLUE      = '\033[34m'
    PURPLE    = '\033[35m'
    CYAN      = '\033[36m'
    WHITE     = '\033[37m'
    END       = '\033[0m'
    BOLD      = '\038[1m'
    UNDERLINE = '\033[4m'
    INVISIBLE = '\033[08m'
    REVERCE   = '\033[07m'

#command-line arguments
args = sys.argv

def welcomeName():
    print('welcome to' + Color.CYAN + '       __                              __           ' + Color.END)
    print(Color.CYAN + '.---.-. .--.--. |  |_  .-----.  .-----. .-----. |  |_  .-----.' + Color.END)
    print(Color.CYAN + '|  _  | |  |  | |   _| |  -__|  |     | |  -  | |   _| |  -__|' + Color.END)
    print(Color.CYAN + '|___._| |_____| |____| |_____|  |__|__| |_____| |____| |_____|' + Color.END)
    print('                                                    By ' + Color.GREEN + 'Wantto \n' + Color.END)

welcomeName()

'''
def cheakCameraModule()
This function is check camera module.
if you are getting error despite connected camera module, Please check settings enabled camera module.
'''
def cheakCameraModule():
    cmd = 'vcgencmd get_camera'#shell command
    try:
        cmdresultstring = (subprocess.Popen(cmd, stdout=subprocess.PIPE,shell=True).communicate()[0]).decode('utf-8')
    except subprocess.CalledProcessError as e:
        print("\n%s" % str(e))
        sys.exit('commandline error')

    comp = (cmdresultstring == "supported=1 detected=1")#compear result
    if comp:
        print('camera module is found')
    else:
        sys.exit('camera module is not found.\ncamera module is enabled?')


class AutoNoteRaspberryPi:
    def __init__(self):
        self.socket = None # the listening sockets
        self.client_socket = None
        self.listed_devs = []
        self.connection = False

        self.PORT = 1

        self.REQUEST_FINISH = 0
        self.REQUEST_SEND_IMAGE = 1

        self.BTconn = None#Bluetooth connection infomation

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
            print("Bluetooth connection error.")

    '''
    def sendImage(self, image)
    This function is send data.
    '''
    def sendDataBit(self, image):
        #self.port.write(self.translateBit(image))
        self.port.write(image)

    '''
    def translateBit(self, imgfilepass)
    translate image to bit.
    '''
    def translateBit(self, imgfilepass):
        pass

    '''
    def getPhotoFromRasbpPiCamera(self)
    getPhotoFromRasbpPiCamera is order take photo and import photo from Raspberry Pi camera.
    Using shellCommand 'raspistill -o Blackboard.jpg'.
    '''
    def getPhotoFromRasbpPiCamera(self):
        print('Getting photo from camera module.....')
        filename = "Blackboard"+".jpg"
        try:
            subprocess.run(["raspistill","-t","1000", "-o", filename])
            return filename
        except subprocess.CalledProcessError as e:
            print("\n%s" % str(e))
            print("camera module is enabled?")

    '''
    def seeYouImage(self, imgfilepass)
    imgfilepass : String Target image file pass or file name.
    seeYouImage is kill image from filepass.
    '''
    def seeYouImage(self, imgfilepass):
        pass

    '''
    def listen(self, connection)
    
    '''
    def listen(self, connection):
        print("Listening request...")
        res = self.port.read(16)
        request = self.checkOrderType(res)

        if connection:
            if request == b'11':
                return self.getPhotoFromRasbpPiCamera()
            elif request == b'01':
                sys.exit(0)
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
        self.socket.close()
        self.client_socket.close()
        sys.exit(0)

def run():
    app = AutoNoteRaspberryPi()
    app.connectSmartphoneDeviceBluetooth()
    app.listen(app.connection)


if __name__ == "__main__":
    if args not in '-p':
        cheakCameraModule()

    run()

