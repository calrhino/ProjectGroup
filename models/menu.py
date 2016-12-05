# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# Customize your APP title, subtitle and menus here
# ----------------------------------------------------------------------------------------------------------------------

response.logo = A(B('Project ', SPAN(4), ' Groups'), XML('&trade;&nbsp;'),
                  _class="navbar-brand", _href="https://theprojectgroup.pythonanywhere.com/init/default/index")

response.title = request.application.replace('_', ' ').title()
response.subtitle = ''

# ----------------------------------------------------------------------------------------------------------------------
# read more at http://dev.w3.org/html5/markup/meta.name.html
# ----------------------------------------------------------------------------------------------------------------------
response.meta.author = myconf.get('app.author')
response.meta.description = myconf.get('app.description')
response.meta.keywords = myconf.get('app.keywords')
response.meta.generator = myconf.get('app.generator')

# ----------------------------------------------------------------------------------------------------------------------
# your http://google.com/analytics id
# ----------------------------------------------------------------------------------------------------------------------
response.google_analytics_id = None

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
    (T('Home'), False, URL('default', 'welcome'), [])
]

DEVELOPMENT_MENU = True


# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. remove in production
# ----------------------------------------------------------------------------------------------------------------------

def _():
    # ------------------------------------------------------------------------------------------------------------------
    # shortcuts
    # ------------------------------------------------------------------------------------------------------------------
    app = request.application
    ctr = request.controller
    # ------------------------------------------------------------------------------------------------------------------
    # useful links to internal and external resources
    # ------------------------------------------------------------------------------------------------------------------
    response.menu += [
        # (T('My Sites'), False, URL('admin', 'default', 'site')),
        (T('Help'), False, '#', [
            (T('Contact Us'), False,'mailto:cohau@ucsc.edu'),
            LI(_class="divider"),
        ]),
        (T('Documentation'), False, '#', [
            (T('Online book'), False, 'http://www.web2py.com/book'),
            LI(_class="divider"),
            (T('Preface'), False,
             'http://www.web2py.com/book/default/chapter/00'),
            (T('Introduction'), False,
             'http://www.web2py.com/book/default/chapter/01'),
            (T('Python'), False,
             'http://www.web2py.com/book/default/chapter/02'),
            (T('Overview'), False,
             'http://www.web2py.com/book/default/chapter/03'),
            (T('The Core'), False,
             'http://www.web2py.com/book/default/chapter/04'),
            (T('The Views'), False,
             'http://www.web2py.com/book/default/chapter/05'),
            (T('Database'), False,
             'http://www.web2py.com/book/default/chapter/06'),
            (T('Forms and Validators'), False,
             'http://www.web2py.com/book/default/chapter/07'),
            (T('Email and SMS'), False,
             'http://www.web2py.com/book/default/chapter/08'),
            (T('Access Control'), False,
             'http://www.web2py.com/book/default/chapter/09'),
            (T('Services'), False,
             'http://www.web2py.com/book/default/chapter/10'),
            (T('Ajax Recipes'), False,
             'http://www.web2py.com/book/default/chapter/11'),
            (T('Components and Plugins'), False,
             'http://www.web2py.com/book/default/chapter/12'),
            (T('Deployment Recipes'), False,
             'http://www.web2py.com/book/default/chapter/13'),
            (T('Other Recipes'), False,
             'http://www.web2py.com/book/default/chapter/14'),
            (T('Helping web2py'), False,
             'http://www.web2py.com/book/default/chapter/15'),
            (T("Buy web2py's book"), False,
             'http://stores.lulu.com/web2py'),
        ]),
    ]


if DEVELOPMENT_MENU:
    _()

if "auth" in locals():
    auth.wikimenu()
