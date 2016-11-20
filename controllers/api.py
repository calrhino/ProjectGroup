@auth.requires_signature()
def add_student():
    auth_id = request.vars.auth_id
    db(db.students).insert(google_auth_id=auth_id)
    return response.json('add student success')


@auth.requires_signature()
def delete_student():
    auth_id = request.vars.auth_id
    db(db.students.google_auth_id == auth_id).delete()
    return response.json('delete student success')


@auth.requires_signature()
def create_class():
    name = request.vars.name
    description = request.vars.description
    db(db.classes).insert(name=name, description=description)
    return response.json('create class success')


@auth.requires_signature()
def join_class():
    class_id = request.vars.class_id
    auth_id = request.vars.auth_id
    db(db.students.google_auth_id == auth_id).insert(db.classes[class_id])
    return response.json('add class success')


@auth.requires_signature()
def delete_class():
    class_id = request.vars.class_id
    db(db.classes.id == class_id).delete()
    return response.json('delete class success')

@auth.requires_signature()
def create_project():
    auth_id = request.vars.auth_id
    class_id = request.vars.class_id
    name = request.vars.name
    description = request.vars.description

    db(db.projects).insert(name=name, description=description)
    project_id = db(db.projects).select(sortby=~id).first().id
    db(db.classes.id == class_id).insert(db(db.projects.id == project_id))
    db(db.proj_students.id == project_id).insert(db(db.students.google_auth_id == auth_id).select())
    return response.json('create project success')


@auth.requires_signature()
def join_project():
    project_id = request.vars.project_id
    auth_id = request.vars.auth_id
    db(db.proj_students.id == project_id).insert(db(db.students.google_auth_id == auth_id).select())
    return response.json('join project success')


@auth.requires_signature()
def leave_project():
    project_id = request.vars.project_id
    auth_id = request.vars.auth_id
    db(db.proj_students.id == project_id and db.proj_students.students.google_auth_id == auth_id).delete()
    if (db(db.proj_students.id == project_id).select() is None):
        db(db.projects.id == project_id).select().delete()
        db(db.proj_students.id == project_id).select().delete()
        return response.json('leave and remove project success')
    return response.json('leave project success')
