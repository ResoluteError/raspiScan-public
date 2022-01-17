### Neuer Host Name

`sudo nano /etc/hostname`

- Name des RPI eingeben (e.g. raspi-x) (speichern mit Ctrl+X und danach y und enter)

`sudo nano /etc/hosts`

- "localhost" mit name des RPI ersetzen (speichern mit Ctrl+X und danach y und enter)

`sudo reboot`

- neu per SSH login

### Pigpio Installieren

`sudo apt-get update`

`sudo apt-get -y install pigpio`

`sudo systemctl start pigpiod`

`sudo systemctl enable pigpiod`

### Git Setup

`sudo apt -y install git`

`mkdir .ssh `

`cd .ssh`

- Copy/Paste or generate github keys

`chmod 700 id_rsa`

`cd ..`

`git clone git@github.com:ResoluteError/raspiScan.git`

### Setup pip3

Verify if Pip3 is installed:

- `which pip3`

If pip3 is not found:

- `sudo apt -y install python3-pip`

### Raspi Config

`sudo raspi-config`

- Kamera aktivieren
- GPIO aktivieren

### Setup Auto-Update Daemon via SystemD

In raspiScan directory:
`cd /home/pi/raspiScan/`
`git reset --hard HEAD & git pull`
`sudo cp raspiScanAutostart.service /etc/systemd/system/`

Enable the Daemon:

`sudo systemctl daemon-reload`
`sudo systemctl enable raspiScanAutostart.service`
`sudo systemctl start raspiScanAutostart.service`

Verify the Daemon works as expected:

`sudo systemctl status raspiScanAutostart.service`

### Taking Picture & Checking Health

SSH into raspi-8

`cd /home/pi/raspiScan/actions`

To get health status:

- `python3 getHealth`

To take picture:

- `python3 getPicture`

### Viewing Raspi life stream

#### mplayer option

On Raspi: 
- `sudo systemctl stop raspiScanAutostart.service`
- `raspivid -t 0 -w 1280 -h 720 --nopreview -o - | nc -l 5000`

Client:
- `nc raspi-2.local 5000 | mplayer -nosound -framedrop -x 1280 -y 720 -fps 30 -demuxer +h264es -cache 1024 -`

#### VLC player option

On Raspi:
- `sudo systemctl stop raspiScanAutostart.service`
- `raspivid -t 0 -l -o tcp://0.0.0.0:3333`

Client:
- On mac: `alias vlc=/Applications/VLC.app/Contents/MacOS/VLC`
- `vlc tcp/h264://raspi-1.local:3333`