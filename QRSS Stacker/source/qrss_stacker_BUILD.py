from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')

setup(
    options = {
        'py2exe': {
            #'bundle_files': 1,
            'packages':'encodings',
            'includes': 'cairo, pango, pangocairo, atk, gobject',
        }
    },
	windows = [{
        'script': "qrss_stacker.py",
        "icon_resources": [(1, "icon.ico")]
               }],
    data_files=['vd_stacker.glade','logo_vdstacker.jpg'],
    zipfile = None,
)


