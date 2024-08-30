# -*- coding:utf-8 -*-

import bottle
import threading
import os
import errors_and_exceptions
import const
from common import get_app_dir, get_file_path


class WebApp(threading.Thread):
    def __init__(self, state, display, config):
        threading.Thread.__init__(self)

        self.daemon = True

        self._state = state
        self._display = display
        self._config = config

    def _index(self):
        error = bottle.request.query.get("error", None)

        with self._state:
            try:
                iso_list = self._state.iso_ls(paths=False)
            except errors_and_exceptions.InvalidMode:
                iso_list = None
            mode = self._state.get_mode()
            inserted_iso = self._state.inserted_iso()
            filebrowser_enable = self._config.get("UPLOAD_MODE_ENABLED", False)
            filebrowser_url = self._config.get("FILEBROWSER_URL", None)
            browse_modes = mode in const.BROWSE_MODES
            upload_mode = mode == const.MODE_UPLOAD

            return bottle.template(get_file_path("static/index.html.template"), 
                               iso_list=iso_list, 
                               mode=mode, 
                               all_modes=const.ALL_MODES,
                               inserted_iso=inserted_iso, 
                               filebrowser_enable=filebrowser_enable,
                               filebrowser_url=filebrowser_url,
                               browse_modes=browse_modes,
                               upload_mode=upload_mode,
                               error=error)
    
    def _mode_change(self):
        with self._state:
            mode = bottle.request.forms.get("mode")
            if mode not in const.ALL_MODES:
                bottle.redirect('/?error=Invalid mode')
            try:
                self._state.set_mode(mode)
            except errors_and_exceptions.InvalidMode as e:
                bottle.redirect('/?error=%s' % e)
            # refresh display
            self._display.refresh(self._state)
            bottle.redirect('/')

    def _insert_iso(self):
        with self._state:
            mode = self._state.get_mode()
            if mode not in const.BROWSE_MODES:
                bottle.redirect('/?error=Invalid mode')
            iso = bottle.request.forms.get("iso")
            if not iso:
                bottle.redirect('/?error=Invalid ISO')
            self._state.insert_iso(iso)
            # refresh display
            self._display.refresh(self._state)
            bottle.redirect('/')

    def _remove_iso(self):
        with self._state:
            mode = self._state.get_mode()
            if mode not in const.BROWSE_MODES:
                bottle.redirect('/?error=Invalid mode')
            self._state.remove_iso()
            # refresh display
            self._display.refresh(self._state)
            bottle.redirect('/')

    def run(self):
        app = bottle.Bottle()

        app.route('/', callback=self._index)
        app.route('/mode_change', method='POST', callback=self._mode_change)
        app.route('/insert_iso', method='POST', callback=self._insert_iso)
        app.route('/remove_iso', method='POST', callback=self._remove_iso)
        app.route('/static/water-css/light.css', 'GET', lambda: bottle.static_file('static/water-css/light.css', root=get_app_dir()))
        app.route('/static/style.css', 'GET', lambda: bottle.static_file('static/style.css', root=get_app_dir()))


        host = self._config.get("WEB_INTERFACE_HOST", "::")
        port = self._config.get("WEB_INTERFACE_PORT", 9000)
        app.run(host=host, port=port)

def start(state, display, config):
    web_app = WebApp(state,
                     display,
                     config)
    web_app.start()


# manual tests
if __name__ == "__main__":
    print("Running test server")
    class State:
        def __init__(self):
            self._mode = const.MODE_CD
            self._inserted_iso = "x.iso"

        def get_mode(self):
            return self._mode

        def set_mode(self, mode):
            self._mode = mode

        def insert_iso(self, iso):
            self._inserted_iso = iso

        def inserted_iso(self):
            return self._inserted_iso
        
        def iso_ls(self, paths=False):
            return ["a.iso", "b.iso", "c.iso", "x.iso"]
        
        # fake with
        def __enter__(self):
            pass

        def __exit__(self, type, value, traceback):
            pass
    
    class Display:
        def refresh(self, state):
            print("Display refreshed")

    from config import Config
    import time
    config = Config()
    config.set("UPLOAD_MODE_ENABLED", True)
    config.set("FILEBROWSER_URL", "http://localhost:8000")
    state = State()
    display = Display()
    web_app = WebApp(state, display, config)
    web_app.start()
    time.sleep(10000)
