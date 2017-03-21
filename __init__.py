#!/usr/bin/env python

''' An simple embedded IPython shell for an easy code inspection

Usage
-----

To add a single breakpoint in your code, use:

    import eipy.here

this will open an embedded IPython shell where you can examine any object.

You may add multiple breakpoints:
    
    import eipy
    eipy.sh() # breakpoint 1
    do_something()
    eipy.sh() # breakpoint 2

From any embedded shell, hit Ctrl-D to resume execution. Type %kill_embedded to
deactivate future breakpoints.


Dependencies
------------

[ansi_codes](https://git.pelouze.net/gabriel/ansi_codes) may *optionally* be
installed to get nicely-formatted messages in Python 3.


TODO
----

- Load configuration from ~/.ipython/profile_default/ipython_config.py.
- Display full traceback when catching exception, and coloured traceback when
  not catching exception.
- Limit traceback when using inside an IPython session and not catching an
  exception.


References and credit
---------------------

- [Step-by-step debugging with IPython][1]
- [Embedding IPython][2]

[1]: http://stackoverflow.com/a/23388116/4352108
[2]: http://ipython.readthedocs.io/en/stable/interactive/reference.html#embedding-ipython

License
-------

eipy

Copyright (C) 2017  Gabriel Pelouze

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

See <http://www.gnu.org/licenses/>.
'''

from .eipy import create_shell
from .eipy import open_shell

ipshell = create_shell()
def sh():
    open_shell(ipshell, stack_depth=3)
