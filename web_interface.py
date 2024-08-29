# -*- coding:utf-8 -*-

import bottle
import threading
import os
import errors_and_exceptions
import const

APP_DIR = os.path.dirname(os.path.realpath(__file__))

class WebApp(threading.Thread):
    def __init__(self, state, display, upload_mode, web_host, web_port):
        threading.Thread.__init__(self)

        self._state = state
        self._display = display
        self._upload_mode = upload_mode
        self._web_host = web_host
        self._web_port = web_port

    def _index(self):
        try:
            iso_list = self._state.iso_ls()
        except errors_and_exceptions.InvalidMode:
            iso_list = None
        mode = self._state.get_mode()
        inserted_iso = self._state.inserted_iso()

        return bottle.template(os.path.join(APP_DIR, "index.html"), iso_list, mode, inserted_iso)
    
    def _mode_change(self):
        mode = bottle.request.forms.get("mode")
        assert(mode in const.ALL_MODES)
        self._state.set_mode(mode)
        # refresh display
        self._display.refresh()
        bottle.redirect('/')

    def _insert_iso(self):
        iso = bottle.request.forms.get("iso")
        assert(iso)
        self._state.insert_iso(iso)
        # refresh display
        self._display.refresh()
        bottle.redirect('/')

    def run(self):
        app = bottle.Bottle()

        app.route('/', callback=self._index)
        app.route('/mode_change', method='POST', callback=self._mode_change)
        app.route('/insert_iso', method='POST', callback=self._insert_iso)

        app.run(host=self.web_host, port=self.web_port)

def start(state, display, web_host, web_port, upload_mode):
    web_app = WebApp(state, display, upload_mode)
    web_app.start()