"""Some helper functions"""
from flask import abort, session
from maproulette.models import Challenge, Task, challenge_types
from functools import wraps
import random

def get_challenge_or_404(id, instance_type=None):
    """Return a challenge by its id or return 404.

    If instance_type is True, return the correct Challenge Type
    """
    c = Challenge.query.filter(Challenge.id==id).first_or_404()
    if not c.active:
        abort(503)
    if instance_type:
        return challenge_types[c.type].query.get(c.id)
    else:
        return c

def get_task_or_404(challenge_id, task_identifier):
    """Return a task based on its challenge slug and task identifier"""
    c = get_challenge_or_404(challenge_id)
    t = Task.query.filter(Task.identifier==task_identifier).\
        filter(Task.challenge_id==c.id).first_or_404()
    return t

def osmlogin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'osm_token' in session and not app.debug:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def get_random_task(challenge):
    rn = random.random()
    t = Task.query.filter(Task.challenge_id == challenge.id,
                          Task.random <= rn).first()
    if not t:
        t = Task.query.filter(Task.challenge_id == challenge.id,
                              Task.random > rn).first()
    return t
