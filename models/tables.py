# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.

import datetime

db.define_table('google_auth',
                Field('user_id', 'text'),
                Field('user_first','text'),
                Field('user_last', 'text'), 
                Field('user_image_link', 'text'),
                Field('user_email', 'text'),
                Field('user_id_token', 'string')
                )

db.define_table('projects',
                Field('name', 'text'),
                Field('description', 'text', default=''),
                )

db.define_table('classes',
                Field('name', 'text'),
                Field('description', 'text', default=''),
                Field('project_id', 'reference projects', default=None),
                )

db.define_table('students',
                Field('class_id', 'reference classes', default=None),
                Field('google_auth_id', 'text'),
                )

db.define_table('proj_students',
                Field('student_id', 'reference students')
                )





db.proj_students.student_id.requires = IS_NOT_EMPTY()
db.students.google_auth_id.requires = IS_NOT_EMPTY()
db.projects.name.requires = IS_NOT_EMPTY()
db.classes.name.requires = IS_NOT_EMPTY()

# I don't want to display the user email by default in all forms.
# db.post.user_email.readable = db.post.user_email.writable = False
# db.post.post_content.requires = IS_NOT_EMPTY()
# db.post.created_on.readable = db.post.created_on.writable = False
# db.post.updated_on.readable = db.post.updated_on.writable = False

# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
