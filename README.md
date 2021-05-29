# RaspiInvertedPendulum


# ADコンバーター導入方法
## 1. ADS1115ライブラリ導入
### 1-1. ライブラリのインストール
```
sudo apt-get update
sudo apt-get install build-essential python-dev python-smbus git
cd ~
git clone https://github.com/adafruit/Adafruit_Python_ADS1x15.git
cd Adafruit_Python_ADS1x15
sudo python setup.py install'''
```

<br>

### 1-2. pythonパッケージのインストール
```
sudo apt-get update
sudo apt-get install build-essential python-dev python-smbus python-pip
sudo pip install adafruit-ads1x15
```
<br><br>

## 2. I2C通信の導入
### 2-1. ライブラリのインストール
```
sudo apt-get update
sudo apt-get install i2c-tools
```
<br>



### 2-2. pythonパッケージのインストール
`sudo apt install libi2c-dev python-smbus read-edid`

<br>

### 2-3. 初期設定画面起動
`sudo raspi-config`を記入後、
"5 Interfacing Options"を選択してI2Cをenableにする。

<br>

### 2-4. シリアル通信baudrateの設定
`sudo vim /etc/modules`で'i2c'が記載されていることを確認。

`sudo vim /boot/config.txt`を実行し最終行に"dtparam=i2c_baudrate=50000"を追記

`sudo reboot`で再起動

`dmesg | grep i2c`で設定が反映されていることを確認。

実行結果例：
```
[    4.607918] i2c /dev entries driver
[   12.712102] bcm2708_i2c 20804000.i2c: BSC1 Controller at 0x20804000 (irq 79) (baudrate 50000)
```
<br>

### 2-5. I2Cコマンドの使用確認
"`sudo i2cdetect -l`"を実行しI2Cパス一覧を確認
実行結果例：
```
i2c-1   i2c    20804000.i2c         I2C adapter
```
"`200~sudo i2cdetect -y 1`"を実行し、I2Cデバイス一覧およびそれらのアドレスを確認。

実行結果例(成功)：
```
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- 48 -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
```
→ 初期設定終わり  
<br> 
 
実行結果例(失敗):
```
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- UU -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
```
→ [ばっくらっしゅの備忘録](http://koyama4284.blogspot.com/2016/11/orange-pi-pc-lm75a-2.html/)

