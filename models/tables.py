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
                Field('status', 'text', default='', length=100),
                Field('leader_ref', 'reference auth_user'),
                Field('project_ref', 'reference projects')
                )

db.define_table('group_students',
                Field('student_ref', 'reference auth_user'),
                Field('group_ref', 'reference groups')
                , ondelete="NO ACTION"
                )

db.define_table('class_users',
                Field('user_ref', 'reference auth_user'),
                Field('class_ref', 'reference classes')
                , ondelete="NO ACTION"
                )

# kind 0: regular message; 1: request to join group
# state 0: not deleted; 1: deleted by sender; 2: deleted by receiver; 3: deleted by both (nonexistent)
# status: 0: pending; 1: approved; -1: rejected
db.define_table('messages',
                Field('sender_ref', 'reference auth_user'),
                Field('receiver_ref', 'reference auth_user'),
                Field('group_ref', 'reference groups', default=None),
                Field('kind', 'integer', default=0),
                Field('del_state', 'integer', default=0),
                Field('status', 'integer', default=0),
                Field('msg', 'string', length=200)
                , ondelete="NO ACTION"
                )

db.groups.name.requires = IS_NOT_EMPTY()
db.classes.name.requires = IS_NOT_EMPTY()
db.projects.name.requires = IS_NOT_EMPTY()
