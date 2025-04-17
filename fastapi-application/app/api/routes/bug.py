from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_user
from app.schemas.bug import BugCreated, BugResponse, BugUpdated
from app.services.bug import create_bug, get_all_bugs, get_bug_by_id, update_bug, delete_bug
from uuid import UUID
from app.models.bug import PriorityEnum

router = APIRouter()

@router.post("/projects/{projectId}/bugs", response_model=BugResponse)
async def post_bug(projectId: UUID, bug_data: BugCreated, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    bug = create_bug(db, projectId, bug_data, current_user)
    return bug

@router.get("/projects/{projectId}/bugs", response_model=list[BugResponse])
def get_bugs(
    projectId: UUID,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
    title: str = Query(None, description="Filter by name"),
    priority: PriorityEnum = Query(None, description="Filter by priority"),
    sort_by: str = Query("title", regex="^(title|priority)$", description="Sort by title or priority"),
    sort_order: str = Query("asc", regex="^(asc|desc)$", description="Sort order (asc or desc)")
):
    bugs = get_all_bugs(db, projectId=projectId, title=title, priority=priority, sort_by=sort_by, sort_order=sort_order)
    return bugs

@router.get("/projects/{projectId}/bugs/{bugId}", response_model=BugResponse)
def get_bug_detail(
    projectId: UUID,
    bugId: UUID,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    return get_bug_by_id(db, bugId)

@router.put("/projects/{projectId}/bugs/{bugId}", response_model=BugResponse)
def update_bug_route(
    bugId: UUID,
    bug_data: BugUpdated,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    return update_bug(db, bugId, bug_data, current_user)

@router.delete("/projects/{projectId}/bugs/{bugId}")
def delete_bug_route(
    bugId: UUID,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    return delete_bug(db, bugId)
