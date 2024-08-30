# -*- coding:utf-8 -*-

import bottle
import threading
import os
import errors_and_exceptions
import const

APP_DIR = os.path.dirname(os.path.realpath(__file__))

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
            filebrowser_enable = self._config.get("FILEBROWSER_ENABLE", False)
            filebrowser_url = self._config.get("FILEBROWSER_URL", None)
            browse_modes = mode in const.BROWSE_MODES
            upload_mode = mode == const.MODE_UPLOAD

            return bottle.template(os.path.join(APP_DIR, "index.html.template"), 
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

    def _filebrowser_redirect(self):
        upload_mode_enable = self._config.get("UPLOAD_MODE_ENABLE", False)
        assert(upload_mode_enable)
        filebrowser_url = self._config.get("FILEBROWSER_URL", None)
        assert(filebrowser_url)
        bottle.redirect(filebrowser_url)

    def run(self):
        app = bottle.Bottle()

        app.route('/', callback=self._index)
        app.route('/mode_change', method='POST', callback=self._mode_change)
        app.route('/insert_iso', method='POST', callback=self._insert_iso)
        app.route('/remove_iso', method='POST', callback=self._remove_iso)
        app.route('/filebrowser_redirect', callback=self._filebrowser_redirect)
        # style.css
        app.route('/style.css', 'GET', lambda: bottle.static_file('style.css', root=APP_DIR))

        host = self._config.get("WEB_INTERFACE_HOST", "::")
        port = self._config.get("WEB_INTERFACE_PORT", 9000)
        app.run(host=host, port=port)

def start(state, display, config):
    web_app = WebApp(state,
                     display,
                     config)
    web_app.start()
