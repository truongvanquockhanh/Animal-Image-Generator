from sqlalchemy.orm import Session
from app.models import Note, User, Bug
from uuid import UUID
from fastapi import HTTPException
from app.schemas.note import NoteRequest

def create_note(db: Session, bug_id: UUID, note_data: NoteRequest, current_user: str):

    member = db.query(User).filter(User.username == current_user).first()
    if not member:
        raise HTTPException(status_code=404, detail="User not found")

    # Create a new note
    new_note = Note(
        body=note_data.body,
        authorId=member.id,
        bugId=bug_id,
        author=member
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note 

def get_all_note(db: Session, bug_id: UUID, body: str, sort_by: str = "body", sort_order: str = "asc"):

    query = db.query(Note).filter(Note.bugId == bug_id)

    if body:
        query = query.filter(Note.body.ilike(f"%{body}%"))

    if sort_by == "body":
        if sort_order == "asc":
            query = query.order_by(Note.body.asc())
        else:
            query = query.order_by(Note.body.desc())
    elif sort_by == "id":
        if sort_order == "asc":
            query = query.order_by(Note.id.asc())
        else:
            query = query.order_by(Note.id.desc())

    notes = query.all()

    if not notes:
        raise HTTPException(status_code=404, detail="Notes not found")
    return notes

def get_note_by_id(db: Session, note_id: UUID):

    note = db.query(Note).filter(Note.id == note_id).first()

    # If the note doesn't exist, raise a 404 HTTPException
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

def update_note(db: Session, note_id: UUID, note_data: NoteRequest, current_user: str):

    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    # Update the note's attributes
    if note_data.body:
        note.body = note_data.body

    db.commit()
    db.refresh(note)
    return note

def delete_note(db: Session, note_id: UUID, current_user: str):

    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(note)
    db.commit()
    return {"detail": "Note deleted successfully"}
