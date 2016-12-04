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
                Field('user_first', 'text'),
                Field('user_last', 'text'),
                Field('user_image_link', 'text'),
                Field('user_email', 'text'),
                Field('user_id_token', 'string')
                )

db.define_table('students',
                Field('google_auth_id', 'integer'),
                )

db.define_table('classes',
                Field('name', 'text'),
                Field('description', 'text', default=''),
                Field('instructor_id', 'reference students')
                )

db.define_table('projects',
                Field('name', 'text'),
                Field('description', 'text', default=''),
                Field('class_id', 'reference classes')
                )

db.define_table('groups',
                Field('name', 'text'),
                Field('description', 'text', default=''),
                Field('status', 'text', default=''),
                Field('leader_id', 'reference students'),
                Field('project_id', 'reference projects')
                )

db.define_table('group_students',
                Field('group_id', 'reference groups'),
                Field('student_id', 'reference students')
                )

db.define_table('proj_students',
                Field('project_id', 'reference projects'),
                Field('student_id', 'reference students')
                )

db.define_table('class_students',
                Field('student_id', 'reference students'),
                Field('class_id', 'reference classes')
                )

db.students.google_auth_id.requires = IS_NOT_EMPTY()
db.groups.name.requires = IS_NOT_EMPTY()
db.classes.name.requires = IS_NOT_EMPTY()
db.projects.name.requires = IS_NOT_EMPTY()
