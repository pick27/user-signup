#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re

def buildform(name, email, uerror, perror, eerror):
    form = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="utf-8">
        </head>
        <body>
        <h1>Signup</h1>
        <form method="POST" action="/">"""
    form += """
        <table>
        <tr>
        <th>Username</th>
        <td><input name="username" value="%(name)s"/></td>
        <td class="error" style="color:red;">%(uerror)s</td>
        </tr>
        <tr>
        <th>Password</th>
        <td><input name="password" /></td>
        <td class="error" style="color:red;"></td>
        </tr>
        <tr>
        <th>Verify Password</th>
        <td><input name="verify" /></td>
        <td class="error" style="color:red;">%(perror)s</td>
        </tr>
        <tr>
        <th>Email (optional)</th>
        <td><input name="email" value="%(email)s"/></td>
        <td class="error" style="color:red;">%(eerror)s</td>
        </tr>
        </table>
        <input type="submit" value="Submit" />
        </form></body></html>""" % {'name': cgi.escape(name, quote=True), 'uerror': uerror,
        'perror': perror, 'email': cgi.escape(email, quote=True),
        'eerror': eerror}
    return form

class MainHandler(webapp2.RequestHandler):
    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
        username_error = ""
        user_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        if username == "":
            username_error = "Username is a required field."
        elif " " in username:
            username_error = "Username may not contain a space."
        elif not user_re.match(username):
            username_error = "That's not a valid username."
        password_error = ""
        password_re = re.compile(r"^.{3,20}$")
        if password != verify:
            password_error = "Your passwords didn't match."
        elif password == "":
            password_error = "Password is a required field."
        elif " " in password:
            password_error = "Password may not contain a space."
        elif not password_re.match(password):
            password_error = "That wasn't a valid password"
        email_error = ""
        email_re = re.compile(r"^[\S]+@[\S]+.[\S]+$")
        email = email.strip()
        if " " in email:
            email_error = "Email may not contain a space."
        elif email != "" and not email_re.match(email):
            email_error = "That's not a valid email address."
        if password_error + username_error + email_error == "":
            self.redirect("/welcome?username=%s" % username)
        content = buildform(username, email, username_error, password_error, email_error)
        self.response.write(content)

    def get(self):
        username = ""
        email = ""
        username_error = ""
        password_error = ""
        email_error = ""
        content = buildform(username, email, username_error, password_error, email_error)
        self.response.write(content)

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        content = "<h2>Welcome, %s!</h2>" % cgi.escape(username)
        self.response.write(content)
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
