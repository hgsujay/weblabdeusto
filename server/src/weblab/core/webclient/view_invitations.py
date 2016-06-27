import datetime
from flask import render_template, request, url_for, redirect, flash
from flask.ext.wtf import validators

from weblab.core.wl import weblab_api
from weblab.core.exc import SessionNotFoundError
from weblab.core.i18n import gettext

@weblab_api.route_webclient("/invitation/<id>/register", methods=["GET", "POST"])
def invitation_register(id):
    # If this was a POST then we must try to create the user.
    if request.method == "POST":

        login = request.values.get("login")
        password = request.values.get("password")
        full_name = request.values.get('full_name')
        verification = request.values.get("verification")
        email = request.values.get("email")

        # TODO: Check if username is in use and if password and verification are equal
        print "Username: {}".format(login)
        print "Full name: {}".format(full_name)
        print "Password: {}".format(password)
        print "Verification: {}".format(verification)
        print "email: {}".format(email)


        # Validate: Check that the user does not exist.

        # Validate: Check that the passwords meets minimum (very minimum) criteria.

        # Validate: Check that the passwords are the same.

        # Validate: Check that the e-mail is valid.


        # Create the new user
        registered = True
        weblab_api.db.create_db_user(login, full_name, email, password, 'student')

        # Get the invitation to check that it is valid.
        invitation = weblab_api.db.get_invitation(id)


        # TODO: Accept invitation.

        weblab_api.db.accept_invitation(login, invitation.unique_id, invitation.group.name, registered)

        flash(gettext('Registration done'))

        print("USER CREATED")


        return redirect(url_for(".invitation_register", id=id,_external=True, _scheme=request.scheme))

    return render_template("webclient/registration_form.html")

@weblab_api.route_webclient("/invitation/<id>", methods=["GET"])
def invitation(id):
    try:
        weblab_api.api.check_user_session()
        user_session = True
        login = None
    except SessionNotFoundError:
        login = url_for('.login', next=url_for('.invitation',id=id, _external=True, scheme=request.scheme), _external=True, scheme=request.scheme)
        print login
        user_session = False

    return render_template("webclient/invitation.html", id=id, user_session=user_session, login_url = login)

@weblab_api.route_webclient("/joingroup/<id>", methods=["GET"])
def joingroup(id):

    print 'joining group'

    #Add user to the corresponding group

    return weblab_api.make_response(render_template("webclient/labs.html"))