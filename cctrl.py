import json
import re
import subprocess

#
# $ v4l2-ctl -d /dev/video3 --list-ctrls
#
# User Controls
#
#                      brightness 0x00980900 (int)    : min=0 max=100 step=1 default=50 value=50
#                        contrast 0x00980901 (int)    : min=0 max=100 step=1 default=50 value=50
#                      saturation 0x00980902 (int)    : min=0 max=100 step=1 default=50 value=50
#                             hue 0x00980903 (int)    : min=-15 max=15 step=1 default=0 value=0
#         white_balance_automatic 0x0098090c (bool)   : default=1 value=1
#            power_line_frequency 0x00980918 (menu)   : min=0 max=2 default=3 value=0 (Disabled)
#       white_balance_temperature 0x0098091a (int)    : min=2000 max=10000 step=1 default=6400 value=4754 flags=inactive
#                       sharpness 0x0098091b (int)    : min=0 max=100 step=1 default=50 value=50
#
# Camera Controls
#
#                    pan_absolute 0x009a0908 (int)    : min=-648000 max=648000 step=3600 default=0 value=-72000
#                   tilt_absolute 0x009a0909 (int)    : min=-648000 max=648000 step=3600 default=0 value=-57600
#                  focus_absolute 0x009a090a (int)    : min=0 max=100 step=1 default=50 value=0 flags=inactive
#      focus_automatic_continuous 0x009a090c (bool)   : default=0 value=1
#                   zoom_absolute 0x009a090d (int)    : min=100 max=400 step=1 default=100 value=252
#


#
#
def read_preset():
    with open('camera-example.json') as jf:
        data = json.load(jf)

    return data

#
#
def read_device():
    camera = {
        'device': '/dev/video3',
        'controls': {},
    }

    cmd = ['v4l2-ctl', '-d', camera['device'], '--list-ctrls']
    result = subprocess.run(cmd, stdout=subprocess.PIPE, check=True)
    stdout = result.stdout.decode('utf-8')

    for line in stdout.split("\n"):
        #if re.match(r"^\s.*", line):
        if line.startswith(' '):
            control_name = line.strip().split(' ')[0]
            camera['controls'][control_name] = {}

            attrs = line.strip().split(':')[1].strip().split(' ')
            for pair in attrs:
                if '=' in pair:
                    key, value = pair.split('=')
                    camera['controls'][control_name][key] = value

    return camera

#
#
def write():
    camera = read_preset()
    ctrls = []

    for c in camera['controls']:
        if 'absolute' in c:
            if 'flags' in camera['controls'][c].keys():
                if camera['controls'][c]['flags'] == 'inactive':
                    # skip inactive controls
                    continue

            ctrls.append('{}={}'.format(c, camera['controls'][c]['value']))

    cmd = ['v4l2-ctl', '-d', camera['device'], '--set-ctrl', ",".join(ctrls)]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, check=True)
    stdout = result.stdout.decode('utf-8')
    #print(stdout)
    return


#print(json.dumps(read_preset(), indent=2))
write()
