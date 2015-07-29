from __future__ import print_function, unicode_literals
from collections import defaultdict
from flask import render_template, url_for, request, flash, redirect

from weblab.core.webclient.helpers import _get_gravatar_url, _get_experiment
from weblab.core.wl import weblab_api
from weblab.core.exc import SessionNotFoundError
from weblab.core.webclient import login_required

@weblab_api.route_webclient('/labs/')
def slash_labs():
    return redirect(url_for('.labs', code=301))

@weblab_api.route_webclient('/labs/<category_name>/')
def slash_labs_category(category_name):
    return redirect(url_for('.labs', category=category_name, code=301))

# Not @login_required since we want to skip the next= in this case. This way, the /demo link will be available, and by default
# loging sends back to this location.
@weblab_api.route_webclient('/')
def labs():
    """
    Renders the Laboratories List.
    """
    try:
        weblab_api.api.check_user_session()
    except SessionNotFoundError:
        return redirect(url_for('.login'))

    experiments_raw = weblab_api.api.list_experiments()
    experiments = [ _get_experiment(raw_exp) for raw_exp in experiments_raw ]

    # TODO: Remove me whenever we implement gravatar properly
    weblab_api.context.gravatar_url = _get_gravatar_url()

    return weblab_api.make_response(render_template("webclient/labs.html", experiments=experiments))






