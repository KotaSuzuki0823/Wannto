# AuteNote RaspberryPi
## なにこれ
個人的メモ

## Bluetooth
/dev/rfcomm0の情報を利用してBluetooth通信を行います．
なので事前にペアリングしておく必要あり．

`python3 main.py -b`
で実行するとBluetoothデバイスとRFCOMMでバインドできます．

## 実行方法
シンプルな実行方法

`python3 main.py`

Python2.Xでは動きません．

## コマンドライン引数
### -p
を実行時の引数で指定するとカメラモジュールのチェックを行います．

### -t
メインのRun()を実行せずに，testRun()を実行します．
各関数の単体テストができます．



## 写真の撮らせ方
受信待機中に10進数の1を受信すると写真を撮影します．約1秒後に撮影されます．

10進数の０を受信した場合，このプロセスが終了します．

それ以外の値を受信した場合，エラー表示後再び受信待機します．


## Bluetooth設定(to macOS)
テスト時にmacとラズパイで通信するときに．
2回目以降は接続からでOKです．
###  準備
macOSのシステム環境設定のBluetoothの項目からraspberrypiを接続します．
この段階では，接続してもすぐに未接続になるorエラーが出ます．

### シリアルポート登録
シリアルポート登録にはsdptoolというものを使います．
ラズパイ側で以下のコマンドを実行してみます．

`sudo sdptool browse local | grep -i serial`<br>
空欄が出力されると思います．（まだ登録していないので）

登録する前に設定を変更します．

`sudo nano /etc/systemd/system/dbus-org.bluez.service`<br>
vimみたいなものが開くので，9行目付近の<br>
ExecStart=/usr/lib/bluetooth/bluetoothd<br>
を<br>
ExecStart=/usr/lib/bluetooth/bluetoothd --compat<br>
に変更し保存します．
bluetoothdの再起動します．<br>
`pi@raspberrypi:/ $ sudo systemctl daemon-reload`

`pi@raspberrypi:/ $ sudo systemctl restart bluetooth`

さらにSDPを通常ユーザ（pi）でも使えるようにパーミッションを変更します．<br>
`sudo chmod 777 /var/run/sdp`

`sdptool browse local`を実行していっぱい表示されたら設定は成功です．

シリアルポートの登録は，<br>
`sudo sdptool add SP`<br>
で行います．「Serial Port service registered」が出たら勝ちです．

[参考文献][http://blog.robotakao.jp/blog-entry-135.html]

### RFCOMMセットアップ
ラズパイ側でrfcommをlistenにします．

`sudo rfcomm listen /dev/rfcomm0 1`

「Waiting for connection on channel 1」と表示されます．

### 接続
まずはmac側でポートの確認<br>
`ls -l /dev/tty.*`<br>
/dev/tty.raspberrypi-SerialPortがあるか確認します．（これがラズパイのポート情報）

macで以下のコマンドを実行して接続します．<br>
`sudo screen /dev/tty.raspberrypi-SerialPort`

Raspberry Pi側で

Connention from XX:XX:XX:XX:XX:XX to /dev/rfcomm0<br>
Press CTRL-C for hangup<br>
がでたら接続完了です．<br>
[参考文献][http://blog.robotakao.jp/blog-entry-142.html]

#### Can't create RFCOMM TTY: Address already in use
ラズパイ側で`sudo rfcomm release 0`を実行．

### 
### 
### 

##



[http://blog.robotakao.jp/blog-entry-135.html]: http://blog.robotakao.jp/blog-entry-135.html
[http://blog.robotakao.jp/blog-entry-142.html]: http://blog.robotakao.jp/blog-entry-142.html