# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

if auth.user:
    response.menu = [
        (T('Home'), False, URL('acs_empresa', 'index'), [])
    ]
else:
    response.menu = [
        (T('Home'), False, URL('default', 'index'), [])
    ]
