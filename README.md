[![pyLoad](/docs/resources/banner.png "pyLoad")](http://pyload.org/)
=============================

[![Translation Status](http://translate.pyload.org/badges/pyload/localized.png "Translation Status")](http://translate.pyload.org/project/pyload/)

**pyLoad** is a Free and Open Source download manager written entirely in Python and designed to be extremely lightweight.

pyLoad is available for all kind of operating systems and devices:
You could install it on a computer, but also on a headless servers, a router, a smart usb-stick running linux... almost whatever you want!

You can control it entirely by web.
Its web user interface allows full managing and easily remote access to your download from anywhere, online, or in your personal network..

All common video-sites, one-click-hosters, container formats and well known web standards are supported to allow you to download files.
Additionaly, pyLoad has a great variety of plugins to automate common tasks and make unattended running possible.

pyLoad has a fully featured and well documented API, it's easily extendable and accessible by external tools, cross-platform apps or other softwares.


Dependencies
------------

 - **You need at least python 2.5 or at most python 2.7 to run pyLoad and its required software libraries**
 - **Python 3 and PyPy are not yet supported**

### Required ###

 - **beaker**
 - **jinja2**
 - **pycurl** (python-curl)
 - **simplejson** (only for python 2.5)
 - **thrift**

Some plugins want additional packages, install them only when needed.

### Optional ###

 - **BeautifulSoup**
 - **bjoern** (<https://github.com/jonashaag/bjoern>) for a better webapp experience
 - **feedparser**
 - **jsengine** (spidermonkey, ossp-js, pyv8, rhino, node.js) needed by several hosters (ex.: ClickNLoad)
 - **pycrypto** for RSDF/CCF/DLC support
 - **pyOpenSSL** for SSL connection support
 - **tesseract**, **python-pil** (python-imaging) for automatic captcha recognition support

You can install them using the Python Package Index:

    pip install <package-name>

Indeed, pre-built pyLoad packages have all yet included, so manual install is required only when you get pyLoad source code.


Usage
-----------

### First start ###

Run:

    python pyload.py

and follow the setup assistant instructions.

> **Note:**
If you installed pyLoad by package-manager, command `python pyload.py` is probably equivalent to `pyload`.

Additionally, you can whenever restart the setup assistant typing:

    python pyload.py -s

Or you can even edit configuration files located in your pyLoad home directory (default to `~/.pyload`)
with your favorite editor.
For a short description of all the configuration options available visit <http://pyload.org/configuration>.


### Web User Interface ###

Run:

    python pyload.py

So, to retrieve it point your web browser to the socket address configured by setup (default to `http://localhost:8000`).

You can get the list of accepted arguments typing:

    python pyload.py -h


### Command Line Interface ###

Run:

    python pyload-cli.py -l

You can get the list of accepted arguments typing:

    python pyload-cli.py -h


Notes
-----

For news, downloads, wiki, forum and further information visit <http://pyload.org/>.

To report bugs, suggest features, ask a question, get the developer version
or help us out, visit <https://github.com/pyload/pyload>.

Documentation about extending pyLoad can be found at <http://docs.pyload.org> or joining us at `#pyload` on `irc.freenode.net`.


------------------------------
###### pyLoad Team 2008-2014 ######
