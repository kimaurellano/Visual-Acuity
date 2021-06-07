libs:
Pillow
SpeechRecognition
escpos
PyAudio

PyAudio:
sudo apt-get install portaudio19-dev python-pyaudio
then
pip3 install PyAudio

usb access denied:
sudo groupadd usbusers
sudo usermod -a -G usbusers <username>

create text in etc/udev/rules.d/99-usbusers.rules
add entries:
SUBSYSTEM=="usb", GROUP="usbusers", MODE="0666"
SUBSYSTEMS=="usb", GROUP="usbusers", MODE="0666"

getting vendorid productid xprinter:
lsusb
lsusb -vvv -d 0483:070b | grep bEndpointAddress | grep IN
lsusb -vvv -d 0483:070b | grep bEndpointAddress | grep OUT
lsusb -vvv -d 0483:070b | grep iInterface
