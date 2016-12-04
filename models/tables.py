# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.

import datetime

db.define_table('classes',
                Field('name', 'text'),
                Field('description', 'text', default=''),
                Field('instructor_ref', 'reference auth_user')
                )

db.define_table('projects',
                Field('name', 'text'),
                Field('description', 'text', default=''),
                Field('class_ref', 'reference classes')
                )

db.define_table('groups',
                Field('name', 'text'),
                Field('description', 'text', default=''),
                Field('status', 'text', default=''),
                Field('leader_ref', 'reference auth_user'),
                Field('project_ref', 'reference projects')
                )

db.define_table('group_students',
                Field('student_ref', 'reference auth_user'),
                Field('group_ref', 'reference groups'),
                )

db.define_table('proj_students',
                Field('student_ref', 'reference auth_user'),
                Field('project_ref', 'reference projects')
                )

db.define_table('class_users',
                Field('user_ref', 'reference auth_user'),
                Field('class_ref', 'reference classes')
                )

db.groups.name.requires = IS_NOT_EMPTY()
db.classes.name.requires = IS_NOT_EMPTY()
db.projects.name.requires = IS_NOT_EMPTY()
