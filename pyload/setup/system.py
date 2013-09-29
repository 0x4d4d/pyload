# -*- coding: utf-8 -*-

import sys
import os

# gettext decorator, translated only when needed
_ = lambda x: x

# platform usually don't change at runtime
info = None


def get_system_info():
    """ Returns system information as dict """
    global info

    if info is None:
        import platform

        info = {
            _("Platform"): platform.platform(),
            _("Version"): sys.version,
            _("Path"): os.path.abspath(""),
            _("Encoding"): sys.getdefaultencoding(),
            _("FS-Encoding"): sys.getfilesystemencoding()
        }

    return info