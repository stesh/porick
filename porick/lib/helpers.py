import random

from webhelpers.html import literal
from pylons import url
from pylons import tmpl_context as c

from porick.model import db, Quote, Tag, User

def cgi_unescape(s):
    s = s.replace('&quot;', '"')
    s = s.replace('&gt;', '>')
    s = s.replace('&lt;', '<')
    s = s.replace('&amp;', '&')
    return s

def create_or_get_tag(tagname):
    tag = db.query(Tag).filter(Tag.tag == tagname).first()
    if not tag:
        tag = Tag()
        tag.tag = tagname
        db.add(tag)
        db.commit()
    return tag

def get_score_mouseover(quote, direction):
    if direction == 'up':
        count = quote.votes
    else:
        count = quote.votes - quote.rating
    retval = '%s %svote' % (count, direction)
    if count != 1:
        retval += 's'
    return retval

def add_message(msg, level):
    c.messages.append({'msg': msg, 'level': level})

def get_current_user():
    return db.query(User).filter(User.username == c.username).first()

def check_if_voted(quote):
    for assoc in quote.voters:
        if assoc.user.username == c.username:
            return assoc.direction
