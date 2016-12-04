# database retrieve information for client ------ -------------------------------------------------
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

    class_id = db.classes.insert(name=name, description=description, instructor_ref=instructor)
    db.class_users.insert(user_ref=instructor, class_ref=db.classes[class_id])
    return response.json('create class ' + class_id + ' success')


@auth.requires_login()
def join_class():
    """a student joins a project"""
    class_id = request.vars.class_id
    student = auth.user

    db.class_users.insert(student_ref=student, class_ref=db.classes[class_id])
    return response.json('join class ' + class_id + ' success')


@auth.requires_login()
def leave_class():
    """a student leaves a class"""
    class_id = request.vars.class_id
    student = auth.user

    db(db.class_users.user_ref.id == student.id and db.class_users.class_ref.id == class_id).delete()
    if db(db.class_users.class_ref.id == class_id).select().first() is None:
        db(db.classes.id == class_id).delete()
        return response.json('leave and remove class ' + class_id + ' success')
    return response.json('leave class ' + class_id + ' success')


@auth.requires_login()
def delete_class():
    """delete a class"""
    class_id = request.vars.class_id
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

    project_id = db.projects.insert(name=name, description=description, class_ref=db.classes[class_id])
    return response.json('create project ' + project_id + ' success')


@auth.requires_login()
def join_project():
    """a student joins a project"""
    project_id = request.vars.project_id
    student = auth.user

    db.proj_students.insert(student_ref=student, project_ref=db.projects[project_id])
    return response.json('join project ' + project_id + ' success')


@auth.requires_login()
def leave_project():
    """a student leaves a project"""
    project_id = request.vars.project_id
    student = auth.user

    db(db.proj_students.student_ref == student and db.proj_students.project_ref.id == project_id).delete()
    if db(db.class_users.project_ref.id == project_id).select().first() is None:
        db(db.projects.id == project_id).delete()
        return response.json('leave and remove project ' + project_id + ' success')
    return response.json('leave project ' + project_id + ' success')


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

    group_id = db.groups.insert(name=name, description=description, leader_ref=leader,
                                project_ref=db.projects[project_id])
    db.group_students.insert(student_ref=leader, group_ref=db.groups[group_id])
    return response.json('create group ' + group_id + ' success')


@auth.requires_login()
def join_group():
    """a student joins a group"""
    group_id = request.vars.group_id
    student = auth.user

    db.group_students.insert(student_ref=student, group_ref=db.groups[group_id])
    return response.json('join group ' + group_id + ' success')


@auth.requires_login()
def leave_group():
    """a student leaves a group and autodetect 0 members for deletion"""
    group_id = request.vars.group_id
    student = auth.user

    db(db.group_students.group_ref.id == group_id and db.group_students.student_ref == student).delete()
    if (db(db.group_students.group_ref.id == group_id).select().first() is None):
        db(db.groups.id == group_id).delete()
        return response.json('leave and remove group ' + group_id + ' success')
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

    if db(db.group_students.group_ref == group_id and db.group_students.student_ref == student.id).select().first() is None:
        raise HTTP(401)

    new_status = request.vars.new_status
    db(db.groups.id == group_id).update(status=new_status)
    return response.json('update group ' + group_id + ' status success')


# messages API calls ----------------------------
@auth.requires_login()
def contact_user():
    """contacts the requested user"""
    sender = auth.user
    receiver = db.auth_user[request.vars.id]
    db.messages.insert(sender_ref=sender, receiver_ref=receiver, msg=request.vars.msg)
    return response.json('send message to ' + receiver.first_name + ' success')

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
        members=[]
    )


def response_member(s):
    return dict(
        id=s.id,
        name=s.first_name + ' ' + s.last_name,
        is_user=True if auth.user.id == s else False,
    )

def pr(msg):
    print(msg)
