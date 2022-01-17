from flask import Flask, request
from time import sleep
from picamera import PiCamera
from datetime import datetime
import pysftp


def create_app():
    flask_app = Flask(__name__)
    flask_app.config.from_envvar("APP_SETTINGS")
    camera = PiCamera()
    file_path = "./images/"
    hostname = flask_app.config.get("HOSTNAME")

    def setup_camera(resolution=(3280, 2464),
                     iso=100):
        camera.resolution = resolution
        camera.iso = iso
        camera.led = False
        camera.start_preview()
        sleep(2)
        camera.exposure_mode = 'off'

    def create_full_filename(iso, shutter_speed, img_format="png"):
        name = '{}{}-{}-shutter-{}-iso-{}'.format(file_path,
                                                         hostname,
                                                         datetime.now().isoformat(timespec='seconds'),
                                                         shutter_speed,
                                                         iso).replace(':', '-')
        return '{}.{}'.format(name, img_format)

    def upload_file(full_file_name):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None

        with pysftp.Connection('sftp.hidrive.ionos.com',
                               username='[USER]',
                               password='[PASS]',
                               cnopts=cnopts) as sftp:
            with sftp.cd('/raspi_Scan/Uploads'):
                sftp.put(full_file_name)

    @flask_app.route('/picture')
    def get_picture():
        try:
            camera.awb_mode = 'off'
            shutter_speed = request.args.get('shutter_speed', 33000, int)
            iso = request.args.get('iso', 100, int)
            awb_r = request.args.get('awb_r', 1.65, float)
            awb_b = request.args.get('awb_b', 1.65, float)
            camera.awb_gains = (awb_r, awb_b)
            camera.shutter_speed = shutter_speed
            camera.iso = iso
            full_file_name = create_full_filename(iso, shutter_speed)
            camera.capture(full_file_name, 'png')
            upload_file(full_file_name)
            return '{}: success'.format(hostname)
        except Exception as err:
            return hostname + ': ' + str(err)

    @flask_app.route('/health')
    def get_health():
        try:
            return '{}: UP'.format(hostname)
        except Exception as err:
            return hostname + ': ' + str(err)

    @flask_app.route('/awb')
    def get_awb():
        try:
            camera.awb_mode = 'auto'
            sleep(2)
            gains = camera.awb_gains
            return 'AWB {}: {}'.format(hostname, gains)
        except Exception as err:
            return hostname + ': ' + str(err)

    setup_camera()
    return flask_app
