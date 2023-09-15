from flask import make_response, abort, request
from note_model import Note
from person_model import Person, PersonSchema
from config import db

def read_all():
    people= Person.query.order_by(Person.lname).all()
    person_schema = PersonSchema(many=True)
    print(people)
    data = person_schema.dump(people)
    return data

# def read_one(person_id):
#     person = Person.query.get(person_id)

#     print(person)

#     if person is None:
#         abort(
#             404,
#             f"Person with id {person_id} is not found"
#         )
#     person_schema = PersonSchema()
#     return person_schema.dump(person)

def read_one(person_id):
    """
    This function responds to a request for /api/people/{person_id}
    with one matching person from people

    :param person_id:   Id of person to find
    :return:            person matching id
    """
    # Build the initial query
    person = (
        Person.query.filter(Person.person_id == person_id)
        .outerjoin(Note)
        .one_or_none()
    )

    # Did we find a person?
    if person is not None:

        # Serialize the data for the response
        person_schema = PersonSchema()
        data = person_schema.dump(person)
        return data

    # Otherwise, nope, didn't find that person
    else:
        abort(404, f"Person not found for Id: {person_id}")
        
def create():

    person_data = request.get_json()
    #schema = untuk reformat JSON
    schema = PersonSchema()
    #created_person = PersonSchema(person_data)
    print(person_data)
    p = Person(lname=person_data.get('lname'), fname=person_data.get('fname'))

    Person.create(p)
    #db.session.merge(updated_person)
    #db.session.commit()

    return schema.dump(p)

def update(person_id, person_data):

    # Amvil 1 data dari database
    updated_person = Person.query.get(person_id)

    if updated_person is None:
        abort(
            404,
            f"Person with id {person_id} is not found"
        )
    else:
        #schema = untuk reformat JSON
        schema = PersonSchema()
        #updateX = schema.load(person_data, session=db.session)

        updated_person.lname = person_data.get('lname')
        updated_person.fname = person_data.get('fname')

        updated_person.update()

        #db.session.merge(updated_person)
        #db.session.commit()

        return schema.dump(updated_person)
        # person_data

def delete(person_id):

    deleted_person = Person.query.get(person_id)

    if deleted_person is None:
        abort(
            404,
            f"Person with id {person_id} is not found"
        )
    else:
        deleted_person.delete()

        return f"Person ID {person_id} successfuly deleted."
