from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from app.services.project import create_project, get_project, get_all_projects, update_project, delete_project, add_members_project, delete_members_project
from app.schemas.project import ProjectCreated, ProjectResponse, ProjectCreateReponse, UpdateProject, UpdateProjectResponse, ProjectMemberResponse
from app.api.dependencies import get_db, get_current_user
from fastapi import Query

router = APIRouter()

@router.get("/projects", response_model=list[ProjectResponse])
def get_projects(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
    name: str = Query(None, description="Filter by name"),
    sort_by: str = Query("name", regex="^(name|id)$", description="Sort by name or id"),
    sort_order: str = Query("asc", regex="^(asc|desc)$", description="Sort order (asc or desc)")
):
    projects = get_all_projects(db, name=name, sort_by=sort_by, sort_order=sort_order)
    return projects

@router.post("/projects", response_model=ProjectResponse)
def create_projects(
    project_data: ProjectCreated,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create a new project"""
    return create_project(db, project_data, current_user)

@router.get("/projects/{project_id}", response_model=ProjectResponse)
def get_detail_project(
    project_id: UUID,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user), 
):
    """Get project by ID"""
    return get_project(db, project_id)

@router.put("/projects/{project_id}", response_model=UpdateProjectResponse)
def update_projects(
    project_id: UUID,
    project_data: UpdateProject,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return update_project(db, project_id, project_data, current_user)

@router.put("/projects/{project_id}/members", response_model=list[ProjectMemberResponse])
def add_members_projects(
    project_id: UUID,
    project_data: UpdateProject,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return add_members_project(db, project_id, project_data, current_user)

@router.delete("/projects/{project_id}/members/{member_id}")
def add_members_projects(
    project_id: UUID,
    member_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return delete_members_project(db, project_id, member_id, current_user)

@router.delete("/projects/{project_id}")
def delete_projects(
    project_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return delete_project(db, project_id, current_user)
