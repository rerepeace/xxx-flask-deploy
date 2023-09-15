from flask import make_response, abort, request
from note_model import Note, NoteSchema
from person_model import Person, PersonSchema
from config import db

# GET /notes
def read_all():
    notes = Note.query.join(Person).all()

    note_schema = NoteSchema(many=True)
    results = note_schema.dump(notes)
    
    return results

# POST /people/{person_id}/notes
def create(person_id, note):
    person = (
        Person.query.filter(Person.person_id == person_id).outerjoin(Note).one_or_none()
    )

    if person is None:
        abort (404, f'Person with id {person_id} is not found')
    
    content = note.get('content')
    new_note = Note(content = content, person_id = person_id)

    person.notes.append(new_note)
    person.save()

    note_schema = NoteSchema()
    result = note_schema.dump(new_note)

    return result 
    #db.session.commit()

# GET /people/{person_id}/notes/{note_id}
def read_one(person_id, note_id):
    note = (
        Note.query.filter(Note.note_id == note_id).filter(Person.person_id == Note.person_id).one_or_none()
    )

    print(note, '<<<<<<<<')

    if note is None:
        abort (404, f'Note with id {note_id} own by person id {person_id} is not found')

    note_schema = NoteSchema()
    result = note_schema.dump(note)

    return result

# PUT /people/{person_id}/notes/{note_id}
def update(person_id, note_id, note):
    found_note = (
        Note.query.filter(Note.note_id == note_id).filter(Person.person_id == Note.person_id).one_or_none()
    )

    if found_note is None:
        abort (404, f'Note with id {note_id} own by person id {person_id} is not found')
    
    content = note.get('content')
    found_note.update(content)

    note_schema = NoteSchema()
    result = note_schema.dump(note)

    return result

# DELETE /people/{person_id}/notes/{note_id}
def delete(person_id, note_id):
    found_note = (
        Note.query.filter(Note.note_id == note_id).filter(Person.person_id == Note.person_id).one_or_none()
    )

    if found_note is None:
        abort (404, f'Note with id {note_id} own by person id {person_id} is not found')

    found_note.delete()

    return f'Note with id {note_id} own by person id {person_id} is successfuly deleted.'



