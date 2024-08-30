# -*- coding:utf-8 -*-

import yaml

class Config:
    def __init__(self):
        self._config = {}
    
    def _load(self):
        with open(os.path.join(APP_DIR, "config.yaml"), "r") as f:
            self._config = yaml.safe_load(f)
        # disable upload mode if web interface is disabled
        if not self.get("WEB_INTERFACE_ENABLED", False):
            self.set("UPLOAD_MODE_ENABLED", False)
        # set filebrowser to true if upload is disabled
        if not self.get("UPLOAD_MODE_ENABLED", False):
            self.set("FILEBROWSER_BIN", True)
        # disable UPLOAD_MODE_DISPLAY_TOOGLE if upload mode is disabled
        if not self.get("UPLOAD_MODE_ENABLED", False):
            self.set("UPLOAD_MODE_DISPLAY_TOOGLE", False)

    """def _save(self):
        with open(os.path.join(APP_DIR, "config.yaml"), "w") as f:
            yaml.safe_dump(self._config, f)"""

    def get(self, key, default=None):
        return self._config.get(key, default)
    
    def set(self, key, value):
        self._config[key] = value