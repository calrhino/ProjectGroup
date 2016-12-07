# database retrieve information for client ------ -------------------------------------------------

@auth.requires_login()
def get_all_classes():
    """get the classes not associated with a user"""
    # exclude all relations between user and classes, pick remaining ones
    # This is really ... not so good use of resources :(
    classes = db(db.classes).select()
    exclude = db(db.class_users.user_ref == auth.user).select()

    # for i, e in enumerate(exclude):
    #    classes = classes.exclude(lambda row: row.id == e.id)
    # exclude code above does not work quite right, so have hacky fix instead

    response_classes = []

    # get class from each relation (classes of student)
    for c in classes:
        bool = True
        for e in exclude:
            if (e.class_ref == c.id):
                bool = False
        if bool:
            response_classes.append(response_class(c))
    return response.json(dict(classes=response_classes))


@auth.requires_login()
def get_messages():
    """get the messages associated with a user"""
    received_messages = db(db.messages.receiver_ref == auth.user).select(orderby=~db.messages.id)
    sent_messages = db(db.messages.sender_ref == auth.user).select(orderby=~db.messages.id)
    response_received_messages = []
    response_sent_messages = []

    # dict to return the appropriate status of a message
    text = {0: 'pending', 1: 'accepted', -1: 'rejected'}

    # get all messages you have sent, except those deleted by you
    # response_message(m, is_sender=True)
    for i, m in enumerate(sent_messages):
        if not m.del_state & 1:
            response_sent_messages.append(response_message(m, text, True))

    # get all messages sent to you, except those deleted by you
    # response_message(m, is_sender=False)
    for i, m in enumerate(received_messages):
        if not m.del_state & 2:
            response_received_messages.append(response_message(m, text, False))

    return response.json(dict(received_messages=response_received_messages,
                              sent_messages=response_sent_messages))


@auth.requires_login()
def get_classes():
    """get the classes associated with a student"""
    # select all relations between user and classes for particular student
    class_refs = db(db.class_users.user_ref == auth.user).select()
    response_classes = []

    # get class from each relation (classes of student)
    for i, cref in enumerate(class_refs):
        response_classes.append(response_class(cref.class_ref))
    return response.json(dict(classes=response_classes))


@auth.requires_login()
def get_projects():
    """get all projects associated with a class"""
    projects = db(db.projects.class_ref == request.vars.class_id).select()
    response_projects = []

    for i, p in enumerate(projects):
        response_projects.append(response_project(p))
    return response.json(dict(projects=response_projects))


@auth.requires_login()
def get_groups():
    """get the groups associated with a class"""
    # select all groups for a class
    groups = db(db.groups.project_ref == request.vars.project_id).select()
    response_groups = []

    # groups are only associated to one class per
    for i, g in enumerate(groups):
        response_groups.append(response_group(g))
    return response.json(dict(groups=response_groups))


@auth.requires_login()
def get_members():
    """get the students associated with a group"""
    # select all relations between groups and students for particular group
    member_refs = db(db.group_students.group_ref == request.vars.group_id).select()
    response_members = []

    # get student from each relation (members of group)
    for i, mref in enumerate(member_refs):
        response_members.append(response_member(mref.student_ref))
    return response.json(dict(members=response_members))


# instructor permissions ------------------------
def auth_instructor_class(class_id):
    if auth.user.id != db.classes[class_id].instructor_ref.id:
        raise HTTP(401)


def auth_instructor_project(project_id):
    if auth.user.id != db.projects[project_id].class_ref.instructor_ref.id:
        raise HTTP(401)


def auth_instructor_group(group_id):
    if auth.user.id == db.groups[group_id].project_ref.class_ref.instructor_ref.id:
        return True
    return False


# leader permissions ----------------------------
def auth_leader_group(group_id):
    if auth.user.id is not db.groups[group_id].leader_ref.id:
        return True
    return False


# database insert and delete -------------------- -------------------------------------------------
# class api calls -------------------------------
@auth.requires_login()
def create_class():
    """a student creates a class and is the 'instructor'"""
    name = request.vars.name
    description = request.vars.description
    instructor = auth.user

    class_ref = db.classes.insert(name=name, description=description, instructor_ref=instructor)
    db.class_users.insert(user_ref=instructor, class_ref=db.classes[class_ref])
    return response.json(response_class(class_ref))


@auth.requires_login()
def join_class():
    """a student joins a project"""
    class_id = request.vars.class_id
    student = auth.user

    cref = db.classes[class_id]
    db.class_users.insert(user_ref=student, class_ref=cref)
    return response.json(response_class(cref))


@auth.requires_login()
def leave_class():
    """a student leaves a class"""
    class_id = request.vars.class_id
    student = auth.user

    students = db(db.class_users.class_ref == class_id).select()
    students = students.find(lambda row: row.user_ref == student.id)
    id = students.first().id
    db(db.class_users.id == id).delete()
    return response.json('leave class ' + class_id + ' success')


@auth.requires_login()
def delete_class():
    """delete a class"""
    class_id = request.vars.class_id
    auth_instructor_class(class_id)

    db(db.classes.id == class_id).delete()
    return response.json('delete class ' + class_id + ' success')


# project api calls -----------------------------
@auth.requires_login()
def create_project():
    """only instructor of class may create project"""
    class_id = request.vars.class_id
    auth_instructor_class(class_id)

    name = request.vars.name
    description = request.vars.description

    project_ref = db.projects.insert(name=name, description=description, class_ref=db.classes[class_id])
    return response.json(response_project(project_ref))


@auth.requires_login()
def delete_project():
    """instructor deletes a project"""
    project_id = request.vars.project_id
    auth_instructor_project(project_id)

    db(db.projects.id == project_id).delete()
    return response.json('delete project ' + project_id + ' success')


# group api calls -------------------------------
@auth.requires_login()
def create_group():
    """a student creates a group and is the 'leader'"""
    project_id = request.vars.project_id
    name = request.vars.name
    description = request.vars.description
    leader = auth.user

    group_ref = db.groups.insert(name=name, description=description, leader_ref=leader,
                                 project_ref=db.projects[project_id])
    db.group_students.insert(student_ref=leader, group_ref=db.groups[group_ref])
    return response.json(response_group(group_ref))


@auth.requires_login()
def join_group():
    """a student joins a group"""
    group_id = request.vars.group_id
    student = auth.user
    group = db.groups[group_id]
    if db(db.group_students.group_ref == group.id and
                          db.group_students.student_ref == student.id).select().first() is not None:
        raise HTTP(400)
    db.group_students.insert(student_ref=student, group_ref=group)
    return response.json(response_member(auth.user))


@auth.requires_login()
def leave_group():
    """a student leaves a group and autodetect 0 members for deletion"""
    group_id = request.vars.group_id
    student = auth.user

    students = db(db.group_students.group_ref == group_id).select()
    students = students.find(lambda row: row.student_ref == student.id)
    id = students.first().id
    db(db.group_students.id == id).delete()
    return response.json('leave group ' + group_id + ' success')


@auth.requires_login()
def delete_group():
    """delete a class"""
    group_id = request.vars.group_id
    if not auth_instructor_group(group_id) and not auth_leader_group(group_id):
        raise HTTP(401)

    db(db.groups.id == group_id).delete()
    return response.json('delete group ' + group_id + ' success')


@auth.requires_login()
def set_group_status():
    """set group status if member of group"""
    group_id = request.vars.group_id
    student = auth.user

    if db(db.group_students.group_ref == group_id and
                          db.group_students.student_ref == student.id).select().first() is None:
        raise HTTP(401)

    new_status = request.vars.new_status
    db(db.groups.id == group_id).update(status=new_status)
    return response.json('update group ' + group_id + ' status success')


# messages API calls ----------------------------
@auth.requires_login()
def request_join_group():
    """user requests to join a group"""
    sender = auth.user
    receiver = db.auth_user[request.vars.id]
    group = db.groups[request.vars.group_id]
    db.messages.insert(group_ref=group, sender_ref=sender, receiver_ref=receiver, msg=request.vars.msg, kind=1)
    return response.json('send request join group success')


@auth.requires_login()
def accept_join_group():
    """user in group accepts a user to join group"""
    msg = db.messages[request.vars.id]
    msg.update_record(status=1)
    student = db.auth_user[msg.sender_ref]
    group = db.groups[msg.group_ref]
    if db(db.group_students.group_ref == group.id and
                          db.group_students.student_ref == student.id).select().first() is not None:
        raise HTTP(400)
    db.group_students.insert(student_ref=student, group_ref=group)
    return response.json('accept request success; student has joined your group')


@auth.requires_login()
def reject_join_group():
    """user in group rejects a user requesting to join"""
    msg = db.messages[request.vars.id]
    msg.update_record(status=-1)
    return response.json('reject request success')


@auth.requires_login()
def delete_message():
    """delete message from user's view or from database if both users have deleted the message"""
    id = request.vars.id
    # if invalid variables raise error
    if id is None:
        raise HTTP(400)

    msg = db.messages[request.vars.id]
    if msg.sender_ref.id == msg.receiver_ref.id:
        db(db.messages.id == id).delete()
        return response.json('delete message success')
    else:
        is_sender = True if msg.sender_ref.id == auth.user_id else False

    # if the message is already "deleted" by the user, raise error
    if is_sender and msg.del_state & 1 or not is_sender and msg.del_state & 2:
        raise HTTP(400)

    # delete message request(from user) is valid

    # delete message from table if the other user has already "deleted" the message
    if msg.del_state + 3 > 3:
        db(db.messages.id == id).delete()
    else:
        msg.update_record(del_state=1 if is_sender else 2)
    return response.json('delete message success')


@auth.requires_login()
def contact_user():
    """contacts the requested user"""
    sender = auth.user
    receiver = db.auth_user[request.vars.id]
    msg = db.messages.insert(sender_ref=sender, receiver_ref=receiver, msg=request.vars.msg)
    text = {0: 'pending', 1: 'accepted', -1: 'rejected'}
    return response.json(dict(message=response_message(msg, text, True)))


# other methods  -------------------------------- -------------------------------------------------
# check if the vars exist
def assert_vars(*vars):
    for var in vars:
        if var is None:
            return False
    return True


# helper methods to ensure proper dictionary is sent to client
def response_class(c):
    return dict(
        id=c.id,
        description=c.description,
        name=c.name,
        is_instructor=True if auth.user.id == c.instructor_ref.id else False,
        projects=[],
    )


def response_project(p):
    return dict(
        id=p.id,
        description=p.description,
        name=p.name,
        groups=[]
    )


def response_group(g):
    return dict(
        id=g.id,
        description=g.description,
        name=g.name,
        status=g.status,
        new_status='',
        is_leader=True if auth.user.id == g.leader_ref.id else False,
        is_group=True if db(db.group_students.group_ref == g.id).select().find(
            lambda row: row.student_ref == auth.user.id).first() is not None else False,
        members=[]
    )


def response_member(s):
    return dict(
        id=s.id,
        name=s.first_name + ' ' + s.last_name,
        is_user=True if auth.user.id == s else False,
        img_link=db(db.auth_user.id == s.id).select().first().img_link
    )


def response_message(m, text, is_sender):
    ref = m.receiver_ref if is_sender else m.sender_ref
    kind = True if m.kind else False
    return dict(
        id=m.id,
        notuser_name=ref.first_name + ' ' + ref.last_name,
        notuser_id=ref.id,
        notuser_img=ref.img_link,
        msg=m.msg,
        status=text[m.status] if kind else None,
        group_name=m.group_ref.name if kind else None,
        kind=m.kind,
    )


def pr(msg):
    print(msg)
