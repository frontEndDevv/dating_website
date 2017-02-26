@auth.requires_login()
def show_post():
    feed_form = SQLFORM(db.feed,fields=['feed_post'])
    this_post = db.feed(request.args(0,cast=int))
    db.feed_comment.feed_id.default = this_post.id
    comm_form = SQLFORM(db.feed_comment).process() if auth.user else None
    feedcomments = db(db.feed_comment.feed_id==this_post.id).select(orderby=~db.feed_comment.created_on)
    return locals()

@auth.requires_login()
def index():
    users = db(db.auth_user.bank>0).select(orderby=~db.auth_user.created_on)
    self = db(db.auth_user.id==auth.user.id).select()
    feed_form = SQLFORM(db.feed,fields=['feed_post'])
    db.feed.feed_poster.default = auth.user.id
    db.feed.feed_poster.readable=db.feed.feed_poster.writable=False
    if feed_form.accepts(request.vars):
        response.flash='Update Successful'
    else:
        None
    db(db.auth_user.username==db.auth_user.email).delete()
    if not request.vars.page:
        redirect(URL(vars={'page':1}))
    else:
        page = int(request.vars.page)
    start = (page-1)*100
    end = page*100
    messages = db().select(db.feed.ALL,orderby=~db.feed.created_on,limitby=(start,end))
    user = auth.user_id
    return locals()
