# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.13.3 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# app configuration made easy. Look inside private/appconfig.ini
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
myconf = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(myconf.get('db.uri'),
             pool_size=myconf.get('db.pool_size'),
             migrate_enabled=myconf.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = ['*'] if request.is_local else []
# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = myconf.get('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.get('forms.separator') or ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

from gluon.tools import Auth, Service, PluginManager

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=myconf.get('host.names'))
service = Service()
plugins = PluginManager()

# -------------------------------------------------------------------------
# create all tables needed by auth if not custom tables
# -------------------------------------------------------------------------
auth.settings.extra_fields[auth.settings.table_user_name] = [Field('gender', requires=IS_IN_SET(['Male', 'Female'])),
                                                             Field('preference', requires=IS_IN_SET(['Male', 'Female', 'Both'])),
                                                             Field('city_state', 'string', default="Example: Sanantonio Texas"),
                                                             Field('bank', 'integer'),
                                                             Field('find_user', 'string'),
                                                             Field('picture', 'upload',requires=[IS_IMAGE(extensions=('gif','jpg','jpeg','png'),error_message=" file types accepted: jpg, jpeg, png, gif")])]


auth.define_tables(username=True, signature=True)
db.auth_user.first_name.readable=db.auth_user.first_name.writable=False
db.auth_user.last_name.readable=db.auth_user.last_name.writable=False
db.auth_user.find_user.readable=db.auth_user.find_user.writable=False
db.auth_user.bank.readable=db.auth_user.bank.writable=False
# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.get('smtp.server')
mail.settings.sender = myconf.get('smtp.sender')
mail.settings.login = myconf.get('smtp.login')
mail.settings.tls = myconf.get('smtp.tls') or False
mail.settings.ssl = myconf.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True
auth.settings.allow_delete_accounts=True

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------
db.define_table('inbox',
    Field('for_user', 'reference auth_user'),
    Field('from_user', 'reference auth_user'),
    Field('quick_message', 'string'),
    Field('blocked', 'reference auth_user'),
    Field('blocked_by', 'reference auth_user'),
    auth.signature)
db.inbox.id.readable=db.inbox.id.writable=False
db.inbox.blocked.readable=db.inbox.blocked.writable=False
db.inbox.blocked_by.readable=db.inbox.blocked_by.writable=False

db.define_table('bi_chat',
               Field('bi_poster', 'reference auth_user'),
               Field('bi_message', 'string', requires=IS_NOT_EMPTY()),
               auth.signature)

db.define_table('gay_chat',
               Field('gay_poster', 'reference auth_user'),
               Field('gay_message', 'string', requires=IS_NOT_EMPTY()),
               auth.signature)

db.define_table('straight_chat',
               Field('straight_poster', 'reference auth_user'),
               Field('straight_message', 'string', requires=IS_NOT_EMPTY()),
               auth.signature)

db.define_table('feed',
               Field('feed_poster', 'reference auth_user', default=auth.user_id),
               Field('feed_post', 'string', requires=IS_NOT_EMPTY(),default="What's new?" ),
                Field('feed_comment', 'string', requires=IS_NOT_EMPTY()),
                Field('created_by', 'reference auth_user', default=auth.user_id),
                Field('created_on','datetime', default=request.now),
               auth.signature)
db.feed.created_by.readable=db.feed.created_by.writable=False
db.feed.created_on.readable=db.feed.created_on.writable=False

db.define_table('feed_comment',
               Field('feed_id','reference feed'),
               Field('your_comment', 'string'),
               Field('created_on','datetime', default=request.now),
               Field('created_by', 'reference auth_user', default=auth.user_id))
db.feed_comment.created_by.readable=db.feed_comment.created_by.writable=False
db.feed_comment.created_on.readable=db.feed_comment.created_on.writable=False
db.feed_comment.feed_id.readable=db.feed_comment.feed_id.writable=False

db.define_table('the_page',
               Field('title'),
               Field('body', 'text'),
               Field('created_on','datetime', default=request.now),
               Field('created_by', 'reference auth_user', default=auth.user_id),
               format='%(title)s')

db.define_table('post',
               Field('page_id','reference the_page'),
               Field('body', 'string'),
               Field('created_on','datetime', default=request.now),
               Field('created_by', 'reference auth_user', default=auth.user_id))

db.define_table('documents',
               Field('page_id', 'reference the_page'),
               Field('name'),
               Field('file_field', 'upload'),
               Field('created_on','datetime', default=request.now),
               Field('created_by', 'reference auth_user', default=auth.user_id),
               format='%(name)s')

db.the_page.body.requires=IS_NOT_EMPTY()
db.the_page.created_by.readable=db.the_page.created_by.writable=False
db.the_page.created_on.readable=db.the_page.created_on.writable=False
db.post.page_id.readable=db.post.page_id.writable=False
db.post.created_by.readable=db.post.created_by.writable=False
db.post.created_on.readable=db.post.created_on.writable=False
db.documents.created_on.readable=db.documents.created_on.writable=False
db.documents.created_by.readable=db.documents.created_by.writable=False
db.documents.page_id.readable=db.documents.page_id.writable=False


# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)
