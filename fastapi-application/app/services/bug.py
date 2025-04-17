from sqlalchemy.orm import Session
from app.models import Bug, User, Note
from app.schemas.bug import BugCreated, BugUpdated
from uuid import UUID
from app.models.bug import PriorityEnum
from fastapi import HTTPException

def create_bug(db: Session, project_id: UUID, bug_data: BugCreated, current_user: str):

    member = db.query(User).filter(User.username == current_user).first()
    new_bug = Bug(
        title=bug_data.title,
        description=bug_data.description,
        priority=bug_data.priority,
        projectId=project_id,
        createdBy=member
    )
    db.add(new_bug)
    db.commit()
    db.refresh(new_bug)
    return new_bug

def get_all_bugs(db: Session, title: str = None, priority: PriorityEnum = None, projectId: str = None, sort_by: str = "title", sort_order: str = "asc"):

    query = db.query(Bug)

    if title:
        query = query.filter(Bug.title.ilike(f"%{title}%"))

    if priority:
        query = query.filter(Bug.priority == priority)

    if sort_by == "title":
        if sort_order == "asc":
            query = query.order_by(Bug.title.asc())
        else:
            query = query.order_by(Bug.title.desc())
    elif sort_by == "priority":
        if sort_order == "asc":
            query = query.order_by(Bug.id.asc())
        else:
            query = query.order_by(Bug.id.desc())

    query = query.filter(Bug.projectId == projectId)

    bugs = query.all()

    if not bugs:
        raise HTTPException(status_code=404, detail="No bugs found")
    
    

    bugs = query.all()
    for bug in bugs:
            notes = db.query(Note).filter(Note.bugId == bug.id).all()
            note_ids = []
            for note in notes:
                note_ids.append(note.id)
            bug.notes = note_ids

    return bugs

def get_bug_by_id(db: Session, bug_id: UUID):

    bug = db.query(Bug).filter(Bug.id == bug_id).first()
    if not bug:
        raise HTTPException(status_code=404, detail="Bug not found")
    notes = db.query(Note).filter(Note.bugId == bug.id).all()
    note_rp = []
    for note in notes:
        note_rp.append(note)
    bug.notes = note_rp
    return bug

def update_bug(db: Session, bug_id: UUID, bug_data: BugUpdated, current_user: str):

    member = db.query(User).filter(User.username == current_user).first()
    print(member.username, type(member))
    bug = db.query(Bug).filter(Bug.id == bug_id).first()

    if not bug:
        raise HTTPException(status_code=404, detail="Bug not found")
    
    if bug_data.title:
        bug.title = bug_data.title

    if bug_data.description:
        bug.description = bug_data.description

    if bug_data.priority:
        bug.priority = bug_data.priority

    bug.updatedBy = member

    db.commit()
    db.refresh(bug)
    return bug

def delete_bug(db: Session, bug_id: UUID):

    bug = db.query(Bug).filter(Bug.id == bug_id).first()

    if not bug:
        raise HTTPException(status_code=404, detail="Bug not found")

    db.delete(bug)
    db.commit()

    return {"message": "Bug deleted successfully"}
