from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from app.services.note import create_note, get_all_note, get_note_by_id, update_note, delete_note
from app.schemas.project import ProjectCreated, ProjectResponse, ProjectCreateReponse
from app.api.dependencies import get_db, get_current_user
from fastapi import Query
from app.schemas.note import NoteResponse, NoteRequest

router = APIRouter()

@router.post("/projects/{projectId}/bugs/{bugId}/notes/", response_model=NoteResponse)
def create_notes(
    projectId: UUID,
    bugId: UUID,
    body: NoteRequest,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    note = create_note(db, bugId, body, current_user)
    return note

@router.get("/projects/{projectId}/bugs/{bugId}/notes/", response_model=list[NoteResponse])
def get_all_notes(
    projectId: UUID,
    bugId: UUID,
    body: str = Query(None, description="Filter by body"),
    sort_by: str = Query("body", regex="^(body|id)$", description="Sort by body or id"),
    sort_order: str = Query("asc", regex="^(asc|desc)$", description="Sort order (asc or desc)"),
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_all_note(db, bugId, body, sort_by, sort_order)

@router.get("/projects/{projectId}/bugs/{bugId}/notes/{note_id}", response_model=NoteResponse)
def get_note_by_id_route(note_id: UUID, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    """Get a single note by ID"""
    note = get_note_by_id(db, note_id)  # Call the service function
    return note  # Return the note, FastAPI will handle the serialization

@router.put("/projects/{projectId}/bugs/{bugId}/notes/{note_id}", response_model=NoteResponse)
def update_note_route(
    note_id: UUID,
    note_data: NoteRequest,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    note = update_note(db, note_id, note_data, current_user)
    return note

@router.delete("/projects/{projectId}/bugs/{bugId}/notes/{note_id}")
def delete_note_route(
    note_id: UUID,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return delete_note(db, note_id)  
