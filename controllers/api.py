@auth.requires_signature()
def add_class():
    request.vars.join_class
 def add_post():
     """Here you get a new post and add it.  Return what you want."""
     p_id = db.post.insert(post_content=request.vars.content)
     p = db.post(p_id)
     return response.json(dict(post=response_post(p)))


 @auth.requires_signature()
 def del_post():
     """Used to delete a post."""
     id = int(request.vars.post_id) if request.vars.post_id is not None else 0
     del db.post[request.vars.post_id]
     return response.json("delete ok")

 @auth.requires_signature()
 def edi_post():
     """Take existing post and edit it."""
     id = int(request.vars.post_id) if request.vars.post_id is not None else 0
     db.post[id] = dict(post_content = request.vars.content)
     p = db.post(id)
     return response.json(dict(updated_on=p.updated_on))

 # Helper Functions:
 def response_post(p):
     """Correctly create a post intended for the client"""
     return dict(
         id=p.id,
         user=get_user_name_from_email(p.user_email),
         content=p.post_content,
         created_on=p.created_on,
         updated_on=p.updated_on if p.updated_on != p.created_on else None,
         is_user=True if auth.user and auth.user.email == p.user_email else False,
         is_edit=False,
         edit_field=p.post_content,
     )

 def get_user_name_from_email(email):
     u = db(db.auth_user.email == email).select().first()
     if u is None:
         return 'None'
     else:
         return ' '.join([u.first_name, u.last_name])