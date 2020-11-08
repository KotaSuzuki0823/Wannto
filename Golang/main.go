package main

import (
	"flag"
	"io/ioutil"
	"log"
	"os"
	"os/exec"
	"time"

	"github.com/tarm/serial"
)

type AutoNoteRaspberryPi interface {
	init()
	connectSmartphoneDeviceBluetooth()
	sendPhotoImage(string)
	getPhotoFromRasbpPiCamera() string
	seeYouImage(string)
	listen() bool
}

type AutoNoteRaspberryPiStruct struct {
	connection    bool
	BluetoothConn *serial.Port
}

func (T *AutoNoteRaspberryPiStruct) init() {
	T.connection = false
	log.Println("initialized")
}

func (T *AutoNoteRaspberryPiStruct) connectSmartphoneDeviceBluetooth() {
	conf := &serial.Config{Name: "/dev/rfcomm0", Baud: 9600, ReadTimeout: time.Millisecond * 500}
	serialConn, err := serial.OpenPort(conf)
	if err != nil {
		log.Fatal(err)
	}
	T.BluetoothConn = serialConn
	T.connection = true
	log.Println("Bluetooth connected!")
}

func (T *AutoNoteRaspberryPiStruct) sendPhotoImage(ImgFilePath string) {
	log.Println("image file sending...")
	ImgBinaly, err := ioutil.ReadFile(ImgFilePath) //読み込み
	if err != nil {
		log.Fatal(err)
	}
	_, err = T.BluetoothConn.Write(ImgBinaly)
	if err != nil {
		log.Fatal(err)
	}
	log.Println("Success!!")
	T.seeYouImage(ImgFilePath)
}
func (T *AutoNoteRaspberryPiStruct) getPhotoFromRasbpPiCamera() string {
	log.Println("Getting photo from camera module.....")
	filename := "Blackboard" + ".jpg"
	err := exec.Command("raspistill", "-t", "1000", "-o", filename).Run()
	if err != nil {
		log.Fatal(err)
	}
	return filename
}
func (T *AutoNoteRaspberryPiStruct) seeYouImage(ImgFilePath string) {
	if err := os.Remove(ImgFilePath); err != nil {
		log.Printf("We cammot remove Image file:%v \n", err)
	}
}
func (T *AutoNoteRaspberryPiStruct) listen() bool {
	RequestSendImage := []byte{49} //DEC 1
	RequestFinish := []byte{48}    //DEC 0

	log.Println("Listening request...")
	buf := make([]byte, 8) //8byte
	if _, err := T.BluetoothConn.Read(buf); err != nil {
		log.Println(err)
	}

	switch buf[0] {
	case RequestSendImage[0]:
		log.Print("receive request send image\n")
		return true
	case RequestFinish[0]:
		log.Println("Finish")
		os.Exit(0)
	default:
		log.Println()
		return false
	}
	return false
}

func bindRfcomm(addr string) {
	log.Print("[RFCOMM BIND]enter target Bluetooth addoress...")
	err := exec.Command("sudo", "rfcomm", "bind", "0", addr).Run()
	if err != nil {
		log.Panicln(err)
	}
	print("done!")
}

func main() {
	var BTaddr = flag.String("addr", "", "serial connect rfcomm0")
	flag.Parse()

	if &BTaddr != nil {
		bindRfcomm(*BTaddr)
	}

	var app AutoNoteRaspberryPi
	app.init()

	app.connectSmartphoneDeviceBluetooth()
	for {
		result := app.listen()

		if result {
			app.sendPhotoImage(app.getPhotoFromRasbpPiCamera())
		}
	}
}
