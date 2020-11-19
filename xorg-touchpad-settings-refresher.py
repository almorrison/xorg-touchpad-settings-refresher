#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0+
# License-Filename: LICENSES/GPL-3.0
# Uses code by Denilson Sá Maia on unix.stackexchange.com and Jeremy Bicha on github.com
import functools
import os
import pyudev
import subprocess
import gi
from gi.repository import Gio

def on_activate(app):
    if app._inhibitor:
        return

    app.hold()
    FNULL = open(os.devnull, 'w')
    BASE_PATH = os.path.abspath(os.path.dirname(__file__))
    path = functools.partial(os.path.join, BASE_PATH)
    call = lambda x, *args: subprocess.call([path(x)] + list(args))
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.start()

    for device in iter(monitor.poll, None):
        #add more commands here as needed
        subprocess.Popen(["nohup", "/usr/bin/xinput", "set-prop", "Microsoft Surface Type Cover Touchpad", "libinput Tapping Enabled", "1"], stdout=FNULL, stderr=subprocess.STDOUT)
        subprocess.Popen(["nohup", "/usr/bin/xinput", "set-prop", "Microsoft Surface Type Cover Touchpad", "libinput Accel Speed", "0.6"], stdout=FNULL, stderr=subprocess.STDOUT)
        subprocess.Popen(["nohup", "/usr/bin/xinput", "set-prop", "Microsoft Surface Type Cover Touchpad", "libinput Natural Scrolling Enabled", "1"], stdout=FNULL, stderr=subprocess.STDOUT)
        subprocess.Popen(["nohup", "/usr/bin/xinput", "set-prop", "Microsoft Surface Type Cover Touchpad", "libinput Click Method Enabled", "0", "1"], stdout=FNULL, stderr=subprocess.STDOUT)

def on_quit_action(action, param, app):
    app.quit()

if __name__ == '__main__':
    app = Gio.Application(application_id='xorg.touchpad-refresher', flags=0)
    app.connect('activate', on_activate)
    app._inhibitor = None

    action = Gio.SimpleAction(name='quit')
    app.add_action(action)
    action.connect('activate', on_quit_action, app)

    app.run([])
