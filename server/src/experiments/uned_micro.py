#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005 onwards University of Deusto
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#
# This software consists of contributions made by many individuals,
# listed below:
#
# Author: Pablo Orduña <pablo@ordunya.com>
#

import urllib
import urllib2
import cookielib


ACCOUNT_URL = 'MC68KLab/Account/' 

class UnedMicroClient(object):

    def __init__(self, domain, admin_username, admin_password):
        self.domain         = domain
        self.admin_username = admin_username
        self.admin_password = admin_password
        self.base_url       = "http://%s" % domain
        self.redirector_url = "%s/MC68KLab/redirect.html" % self.base_url
        self.logon_url      = "%s/MC68KLab/Account/LogOn" % self.base_url
        self.regular_url    = "%s/MC68KLab/" % self.base_url
        self.logoff_url     = "%s/MC68KLab/Account/LogOff" % self.base_url
        self.register_url   = "%s/MC68KLab/Account/Register" % self.base_url

    def login(self, username, password):
        cp = urllib2.HTTPCookieProcessor()
        o = urllib2.build_opener( cp )

        request_data = urllib.urlencode({ "UserName" : username, "Password" : password, "RememberMe" : "false"})

        req = o.open(self.logon_url, request_data)

        req.close()

        cookies = [ cookie for cookie in cp.cookiejar ]

        self._check_logged(cookies)

        return cookies

    def _check_logged(self, session_id):
        cj = cookielib.CookieJar()
        cp = urllib2.HTTPCookieProcessor(cj)

        for cookie in session_id:
            cj.set_cookie(cookie)

        o = urllib2.build_opener( cp )
        req = o.open(self.regular_url)
        account_line = [ line for line in req.readlines() if ACCOUNT_URL in line ]
        if len(account_line) == 0:
            raise Exception("No account line found")
        account_token = account_line[0].split(ACCOUNT_URL)[1].split('"')[0]
        if account_token == 'LogOn':
            raise Exception("User did not log in correctly. Wrong password?")
        elif account_token != 'LogOff':
            raise Exception("User did not log in correctly. Unexpected response!")

    def create_url(self, session_id):
        for cookie in session_id:
            if cookie.name == '.ASPXAUTH':
                return self.redirector_url + "#aspxauth=" + cookie.value
        raise Exception("Cookie .ASPXAUTH not found in session_id")

    def is_still_logged(self, session_id):
        cj = cookielib.CookieJar()
        cp = urllib2.HTTPCookieProcessor(cj)

        for cookie in session_id:
            cj.set_cookie(cookie)

        o = urllib2.build_opener( cp )
        req = o.open(self.regular_url)
        account_line = [ line for line in req.readlines() if ACCOUNT_URL in line ]
        if len(account_line) == 0:
            raise Exception("No account line found")
        account_token = account_line[0].split(ACCOUNT_URL)[1].split('"')[0]
        if account_token == 'LogOn':
            return False
        elif account_token == 'LogOff':
            return True

        raise Exception("User did not log in correctly. Unexpected response!")

    def logout(self, session_id):
        cj = cookielib.CookieJar()
        cp = urllib2.HTTPCookieProcessor(cj)

        for cookie in session_id:
            cj.set_cookie(cookie)

        o = urllib2.build_opener( cp )
        req = o.open(self.logoff_url)
        req.read()
        req.close()

    def register_student(self, username, email, password):
        
        request_data = urllib.urlencode({
            "Center"          : "5", # Centro1
            "Rol"             : "Estudiante",
            "UserName"        : username,
            "Email"           : email,
            "Password"        : password,
            "ConfirmPassword" : password,
        })

        session_id = self.login(self.admin_username, self.admin_password)

        cj = cookielib.CookieJar()
        cp = urllib2.HTTPCookieProcessor(cj)

        for cookie in session_id:
            cj.set_cookie(cookie)

        o = urllib2.build_opener( cp )
        req = o.open(self.register_url, request_data)
        req.read()
        req.close()

        """
        <form action="/MC68KLab/Account/Register" method="post">
        <select id="Center" name="Center"><option value="5">Centro1</option></select>
        <select id="Rol" name="Rol"><option value="Administrador">Administrador</option>
        <option selected="selected" value="Estudiante">Estudiante</option>
        </select>
        <input id="UserName" name="UserName" type="text" value="" />
        <input id="Email" name="Email" type="text" value="" />
        <input id="Password" name="Password" type="password" />
        <input id="ConfirmPassword" name="ConfirmPassword" type="password" />
        <input type="submit" value="Añadir" style="float: left" class="optionBoardColors" />
        """

if __name__ == '__main__':
    import getpass

    username = "pablo.orduna@deusto.es"
    password = "pablo.orduna@deusto.es"

    admin_username = raw_input("admin username:")
    admin_password = getpass.getpass("admin password:")

    client = UnedMicroClient("62.204.201.32:90", admin_username, admin_password)

    client.register_student("porduna2", "porduna2", "porduna2")
    username = "porduna2"
    password = "porduna2"
    session_id = client.login(username, password)
    print client.is_still_logged(session_id)
    print client.create_url(session_id)
    # client.logout(session_id)
    # print client.is_still_logged(session_id)
