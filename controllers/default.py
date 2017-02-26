# block
# push notifications
# ads
# delete messages every 30 days
# randomly pick three users to make featured every month
# clear forum every thirty days
# clear group chats every day at 6 am
# web spider to promote website


# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

# change background in web2py bootstrap css folder

@auth.requires_login()
def auth_user():
    from gluon.contrib.stripe import StripeForm
    form = StripeForm(
        pk="stripe key",
        sk="stripe key",
        amount=3999, # amount is in cents
        description="Monthly Subscription").process()
    if form.accepted:
        db.auth_user.update_or_insert(db.auth_user.id == auth.user.id,
                           bank=3999)
        payment_id = form.response['id']
        response.flash= T("Payment Accepted. You are Now a Featured User")
        # redirect(URL('index'))
    elif form.errors:
        response.flash= T("ERROR! Please try again")
    return locals()

@auth.requires_login()
def forum():
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
    start = (page-1)*25
    end = page*25
    pages = db().select(db.the_page.id,db.the_page.title,db.the_page.created_by,orderby=~db.the_page.created_on,limitby=(start,end))
    return locals()

@auth.requires_login()
def create():
    form = SQLFORM(db.the_page).process(next=URL('forum'))
    return locals()

@auth.requires_login()
def show():
    this_page = db.the_page(request.args(0,cast=int)) or redirect(URL('forum'))
    db.post.page_id.default = this_page.id
    form = SQLFORM(db.post).process() if auth.user else None
    pagecomments = db(db.post.page_id==this_page.id).select()
    return dict(page=this_page, comments=pagecomments, form=form)

@auth.requires_login()
def documents():
    page = db.the_page(request.args(0,cast=int)) or redirect(URL('forum'))
    db.documents.page_id.default = page.id
    db.documents.page_id.writable = False
    grid = SQLFORM.grid(db.documents.page_id==page.id,args=[page.id])
    return locals()

@auth.requires_login()
def search():
    return dict(form=FORM(INPUT(_id='keyword',_name='keyword',_onkeyup="ajax('callack',['keyword'],'target');")),
                target_div=DIV(_id='target'))

@auth.requires_login()
def callback():
    query = db.the_page.title.contains(request.vars.keyword)
    pages = db(query).select(orderby=db.the_page.title)
    links = [A(p.title,_href=URL('show',args=p.id)) for p in pages]
    return UL(*links)

@auth.requires_login()
def group_chat():
    feed_form = SQLFORM(db.feed,fields=['feed_post'])
    db.feed.feed_poster.default = auth.user.id
    db.feed.feed_poster.readable=db.feed.feed_poster.writable=False
    if feed_form.accepts(request.vars):
        response.flash='Update Successful'
    else:
        None
    db(db.auth_user.username==db.auth_user.email).delete()
    self = db(db.auth_user.id==auth.user.id).select()
    users = db(db.auth_user.bank>0).select(orderby=~db.auth_user.created_on)
    return locals()

@auth.requires_login()
def bi_group():
    feed_form = SQLFORM(db.feed,fields=['feed_post'])
    db.feed.feed_poster.default = auth.user.id
    db.feed.feed_poster.readable=db.feed.feed_poster.writable=False
    if feed_form.accepts(request.vars):
        response.flash='Update Successful'
    else:
        None
    db(db.auth_user.username==db.auth_user.email).delete()
    form = SQLFORM(db.bi_chat,fields=['bi_message'])
    db.bi_chat.bi_poster.default = auth.user.id
    db.bi_chat.bi_poster.readable=db.bi_chat.bi_poster.writable=False
    if form.accepts(request.vars):
        response.flash='Message posted'
    else:
        None
    db(db.auth_user.username==db.auth_user.email).delete()
    if not request.vars.page:
        redirect(URL(vars={'page':1}))
    else:
        page = int(request.vars.page)
    start = (page-1)*30
    end = page*30
    messages = db().select(db.bi_chat.ALL,orderby=~db.bi_chat.created_on,limitby=(start,end))
    user = auth.user_id
    return locals()

@auth.requires_login()
def gay_group():
    feed_form = SQLFORM(db.feed,fields=['feed_post'])
    db.feed.feed_poster.default = auth.user.id
    db.feed.feed_poster.readable=db.feed.feed_poster.writable=False
    if feed_form.accepts(request.vars):
        response.flash='Update Successful'
    else:
        None
    db(db.auth_user.username==db.auth_user.email).delete()
    form = SQLFORM(db.gay_chat,fields=['gay_message'])
    db.gay_chat.gay_poster.default = auth.user.id
    db.gay_chat.gay_poster.readable=db.gay_chat.gay_poster.writable=False
    if form.accepts(request.vars):
        response.flash='Message posted'
    else:
        None
    db(db.auth_user.username==db.auth_user.email).delete()
    if not request.vars.page:
        redirect(URL(vars={'page':1}))
    else:
        page = int(request.vars.page)
    start = (page-1)*30
    end = page*30
    messages = db().select(db.gay_chat.ALL,orderby=~db.gay_chat.created_on,limitby=(start,end))
    user = auth.user_id
    return locals()

@auth.requires_login()
def straight_group():
    feed_form = SQLFORM(db.feed,fields=['feed_post'])
    db.feed.feed_poster.default = auth.user.id
    db.feed.feed_poster.readable=db.feed.feed_poster.writable=False
    if feed_form.accepts(request.vars):
        response.flash='Update Successful'
    else:
        None
    db(db.auth_user.username==db.auth_user.email).delete()
    form = SQLFORM(db.straight_chat,fields=['straight_message'])
    db.straight_chat.straight_poster.default = auth.user.id
    db.straight_chat.straight_poster.readable=db.straight_chat.straight_poster.writable=False
    if form.accepts(request.vars):
        response.flash='Message posted'
    else:
        None
    db(db.auth_user.username==db.auth_user.email).delete()
    if not request.vars.page:
        redirect(URL(vars={'page':1}))
    else:
        page = int(request.vars.page)
    start = (page-1)*30
    end = page*30
    messages = db().select(db.straight_chat.ALL,orderby=~db.straight_chat.created_on,limitby=(start,end))
    user = auth.user_id
    return locals()

@auth.requires_login()
def get_file():
    users = db(db.auth_user.bank>0).select(orderby=~db.auth_user.created_on)
    self = db(db.auth_user.id==auth.user.id).select()
    return locals()

@auth.requires_login()
def tips():
    return locals()

@auth.requires_login()
def delete():
    self = db(db.auth_user.id==auth.user.id).select()
    response.flash= T("Hope you've enjoyed your stay!")
    return locals()

@auth.requires_login()
def delete_self():
    delete = db(db.auth_user.id==auth.user.id).delete()
    db.commit()
    session.clear()
    redirect(URL('index'))
    return locals()

@auth.requires_login()
def about():
    return locals()

@auth.requires_login()
def disclaimer():
    return locals()

@auth.requires_login()
def contact():
    return locals()

@auth.requires_login()
def upgrade():
    response.flash= T("Each month, 3 random users will be featured for free.")
    from gluon.contrib.stripe import StripeForm
    form = StripeForm(
        pk="stripe key",
        sk="stripe key",
        amount=799, # amount is in cents
        description="Monthly Subscription").process()
    if form.accepted:
        db.auth_user.update_or_insert(db.auth_user.id == auth.user.id,
                           bank=2999)
        payment_id = form.response['id']
        response.flash= T("Payment Accepted. You are Now a Featured User")
        # redirect(URL('index'))
    elif form.errors:
        response.flash= T("Payment Error. Please try again")
    return locals()

@auth.requires_login()
def post_message():
    user_id = request.args(0)
    db.inbox.for_user.default = user_id # for user is request
    db.inbox.for_user.writable=False
    db.inbox.from_user.default = auth.user.id
    db.inbox.from_user.readable=db.inbox.from_user.writable=False
    form = SQLFORM(db.inbox).process()
    if form.accepted:
        session.flash = T("Message Sent")
    return locals()

@auth.requires_login()
def to_who():
    # my_input = request.vars.to_who
    db.inbox.for_user.readable=True
    db.inbox.for_user.writable=True
    db.inbox.from_user.default = auth.user.id
    db.inbox.from_user.readable=True
    db.inbox.from_user.writable=False
    form = SQLFORM(db.inbox).process()
    return locals()

@auth.requires_login()
def block():
    user_id = request.args(0)
    db.inbox.blocked.default = user_id
    db.inbox.blocked_by.default = auth.user.id
    query = db((db.inbox.blocked_by==db.inbox.for_user)&(db.inbox.blocked==db.inbox.from_user))._select(db.inbox.quick_message)
    db(query).delete()
    db.commit()
    return locals()

@auth.requires_login()
def my_messages():
    feed_form = SQLFORM(db.feed,fields=['feed_post'])
    db.feed.feed_poster.default = auth.user.id
    db.feed.feed_poster.readable=db.feed.feed_poster.writable=False
    if feed_form.accepts(request.vars):
        response.flash='Update Successful'
    else:
        None
    db(db.auth_user.username==db.auth_user.email).delete()
    export_classes = dict(csv=False,html=False,tsv=False,xml=False,
                         csv_with_hidden_cols=False,tsv_with_hidden_cols=False,json=False)
    db.inbox.for_user.writable=True
    db.inbox.from_user.readable=True
    db.inbox.from_user.writable=False
    db.inbox.blocked.readable=False
    # db.inbox.for_user.default = request.args(0)
    form = SQLFORM(db.inbox,orderby=1).process()
    grid = SQLFORM.grid(db.inbox.for_user==auth.user.id, editable=False,create=False,orderby=~db.inbox.created_on
                       ,exportclasses= export_classes, paginate=15, links = [dict(header="QM", body = lambda row: A('Reply',_href=URL("default","post_message",args=[row.from_user.id]))),]
)
    '''dict(header="Block", body = lambda row: A('Block',_href=URL("default","block",args=[row.from_user.id]))),'''
    return locals()

@auth.requires_login()
def sent_msgs():
    feed_form = SQLFORM(db.feed,fields=['feed_post'])
    db.feed.feed_poster.default = auth.user.id
    db.feed.feed_poster.readable=db.feed.feed_poster.writable=False
    if feed_form.accepts(request.vars):
        response.flash='Update Successful'
    else:
        None
    db(db.auth_user.username==db.auth_user.email).delete()
    export_classes = dict(csv=False,html=False,tsv=False,xml=False,
                         csv_with_hidden_cols=False,tsv_with_hidden_cols=False,json=False)
    db.inbox.for_user.writable=True
    db.inbox.from_user.readable=True
    db.inbox.from_user.writable=False
    db.inbox.blocked.readable=False
    # db.inbox.for_user.default = request.args(0)
    form = SQLFORM(db.inbox,orderby=1).process()
    grid = SQLFORM.grid(db.inbox.from_user==auth.user.id, editable=False,create=False,orderby=~db.inbox.created_on
                       ,exportclasses= export_classes, paginate=15, links = [dict(header="QM", body = lambda row: A('Reply',_href=URL("default","post_message",args=[row.for_user.id]))),]
)
    '''dict(header="Block", body = lambda row: A('Block',_href=URL("default","block",args=[row.from_user.id]))),'''
    return locals()

@auth.requires_login()
def user_loc():
    form = SQLFORM(db.auth_user,fields=['state_or_province'])
    form.vars.state_or_province= "NY"
    if form.accepts(request.vars):
        session.flash='Users Found!'
    else:
        None
    db(db.auth_user.username==db.auth_user.email).delete()
    user_loc = db(db.auth_user.state_or_province==request.vars.state_or_province).select(orderby=~db.auth_user.created_on,limitby=(0,20))
    return locals()

@auth.requires_login()
def find_user():
    db.auth_user.find_user.readable=True
    db.auth_user.find_user.writable=True
    form = SQLFORM(db.auth_user,fields=['find_user'])
    form.vars.find_user= "Search For User"
    if form.accepts(request.vars):
        session.flash='Searching...'
    else:
        None
    db(db.auth_user.username==db.auth_user.email).delete()
    # search db auth user username that equals request from form order by most recent
    user_loc = db(db.auth_user.username==request.vars.find_user).select(orderby=~db.auth_user.created_on)
    return locals()

@auth.requires_login()
def bi_users():
    feed_form = SQLFORM(db.feed,fields=['feed_post'])
    db.feed.feed_poster.default = auth.user.id
    db.feed.feed_poster.readable=db.feed.feed_poster.writable=False
    if feed_form.accepts(request.vars):
        response.flash='Update Successful'
    else:
        None
    db(db.auth_user.username==db.auth_user.email).delete()
    self = db(db.auth_user.id==auth.user.id).select()
    bi = (db.auth_user.preference=="Both")
    if not request.vars.page:
        redirect(URL(vars={'page':1}))
    else:
        page = int(request.vars.page)
    start = (page-1)*15
    end = page*15
    user = auth.user_id
    bi_users = db(bi).select(orderby=~db.auth_user.created_on, limitby=(start,end))
    return locals()

@auth.requires_login()
def bi_women():
    self = db(db.auth_user.id==auth.user.id).select()
    bi = ((db.auth_user.preference=="Both")&(db.auth_user.gender=="Female"))
    if not request.vars.page:
        redirect(URL(vars={'page':1}))
    else:
        page = int(request.vars.page)
        start = (page-1)*15
        end = page* 15
        bi_users = db(bi).select(orderby=~db.auth_user.created_on, limitby=(start,end))
    return locals()

@auth.requires_login()
def bi_men():
    self = db(db.auth_user.id==auth.user.id).select()
    bi = ((db.auth_user.preference=="Both")&(db.auth_user.gender=="Male"))
    if not request.vars.page:
        redirect(URL(vars={'page':1}))
    else:
        page = int(request.vars.page)
        start = (page-1)*15
        end = page* 15
        bi_users = db(bi).select(orderby=~db.auth_user.created_on, limitby=(start,end))
    return locals()

@auth.requires_login()
def gay_users():
    feed_form = SQLFORM(db.feed,fields=['feed_post'])
    db.feed.feed_poster.default = auth.user.id
    db.feed.feed_poster.readable=db.feed.feed_poster.writable=False
    if feed_form.accepts(request.vars):
        response.flash='Update Successful'
    else:
        None
    db(db.auth_user.username==db.auth_user.email).delete()
    self = db(db.auth_user.id==auth.user.id).select()
    gay = (db.auth_user.preference==db.auth_user.gender)
    if not request.vars.page:
        redirect(URL(vars={'page':1}))
    else:
        page = int(request.vars.page)
        start = (page-1)*15
        end = page* 15
        gay_users = db(gay).select(orderby=~db.auth_user.created_on, limitby=(start,end))
    return locals()

@auth.requires_login()
def gay_women():
    self = db(db.auth_user.id==auth.user.id).select()
    gay = ((db.auth_user.preference==db.auth_user.gender)&(db.auth_user.gender=="Female"))
    if not request.vars.page:
        redirect(URL(vars={'page':1}))
    else:
        page = int(request.vars.page)
        start = (page-1)*15
        end = page* 15
        gay_users = db(gay).select(orderby=~db.auth_user.created_on, limitby=(start,end))
    return locals()

@auth.requires_login()
def gay_men():
    self = db(db.auth_user.id==auth.user.id).select()
    gay = ((db.auth_user.preference==db.auth_user.gender)&(db.auth_user.gender=="Male"))
    if not request.vars.page:
        redirect(URL(vars={'page':1}))
    else:
        page = int(request.vars.page)
        start = (page-1)*15
        end = page* 15
        gay_users = db(gay).select(orderby=~db.auth_user.created_on, limitby=(start,end))
    return locals()

@auth.requires_login()
def straight_users():
    feed_form = SQLFORM(db.feed,fields=['feed_post'])
    db.feed.feed_poster.default = auth.user.id
    db.feed.feed_poster.readable=db.feed.feed_poster.writable=False
    if feed_form.accepts(request.vars):
        response.flash='Update Successful'
    else:
        None
    db(db.auth_user.username==db.auth_user.email).delete()
    self = db(db.auth_user.id==auth.user.id).select()
    straight = ((db.auth_user.preference != db.auth_user.gender)&(db.auth_user.preference != "Both"))
    if not request.vars.page:
        redirect(URL(vars={'page':1}))
    else:
        page = int(request.vars.page)
        start = (page-1)*15
        end = page* 15
        straight_users = db(straight).select(orderby=~db.auth_user.created_on, limitby=(start,end))
    return locals()

@auth.requires_login()
def straight_women():
    self = db(db.auth_user.id==auth.user.id).select()
    straight = ((db.auth_user.preference != db.auth_user.gender)&(db.auth_user.preference != "Both")&(db.auth_user.gender=="Female"))
    if not request.vars.page:
        redirect(URL(vars={'page':1}))
    else:
        page = int(request.vars.page)
        start = (page-1)*15
        end = page* 15
        straight_users = db(straight).select(orderby=~db.auth_user.created_on, limitby=(start,end))
    return locals()

@auth.requires_login()
def straight_men():
    self = db(db.auth_user.id==auth.user.id).select()
    straight = ((db.auth_user.preference != db.auth_user.gender)&(db.auth_user.preference != "Both")&(db.auth_user.gender=="Male"))
    if not request.vars.page:
        redirect(URL(vars={'page':1}))
    else:
        page = int(request.vars.page)
        start = (page-1)*15
        end = page* 15
        straight_users = db(straight).select(orderby=~db.auth_user.created_on, limitby=(start,end))
    return locals()

@auth.requires_login()
def index():
    feed_form = SQLFORM(db.feed,fields=['feed_post'])
    db.feed.feed_poster.default = auth.user.id
    db.feed.feed_poster.readable=db.feed.feed_poster.writable=False
    if feed_form.accepts(request.vars):
        response.flash='Update Successful'
    else:
        None
    db(db.auth_user.username==db.auth_user.email).delete()
    response.flash = T("Welcome to JBTUS")
    self = db(db.auth_user.id==auth.user.id).select()
    straight = ((db.auth_user.preference != db.auth_user.gender)&(db.auth_user.preference != "Both"))
    users = db(db.auth_user.bank>0).select(orderby=~db.auth_user.created_on)
    if not request.vars.page:
        redirect(URL(vars={'page':1}))
    else:
        page = int(request.vars.page)
        start = (page-1)*10
        end = page* 10
        straight_users = db(straight).select(orderby=~db.auth_user.created_on,limitby=(start,end))
    return locals()


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
