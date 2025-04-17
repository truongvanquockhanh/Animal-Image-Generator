from sqlalchemy.orm import Session
from app.models.project import Project
from app.models.project_member import ProjectMember
from datetime import datetime, timezone
from app.schemas.project import ProjectCreated, ProjectMemberResponse, ProjectResponse, UpdateProject
from app.schemas.user import UserResponse
from app.models import User, Bug
from fastapi import HTTPException
from uuid import UUID

def create_project(db: Session, project_data: ProjectCreated, user: str):
    """Create a new project"""
    member = db.query(User).filter(User.username == user).first()
    project = Project(name=project_data.name, createdById=member.id)
    db.add(project)
    db.commit()
    db.refresh(project)

    project_member = ProjectMember(project_id=project.id, user_id=member.id, joined_at=datetime.now(timezone.utc))
    db.add(project_member)
    db.commit()
    db.refresh(project_member)

    members = []
    for project_member in project.members:
        members.append(ProjectMemberResponse(
            id=project_member.id,
            joinedAt=project_member.joined_at,
            member=UserResponse(id=project_member.members.id, username=project_member.members.username)
        ))

    list_bugs = []
    bugs = db.query(Bug).filter(Bug.projectId == project.id).all()
    if bugs:
        for bug in bugs:
            list_bugs.append({
                "id": bug.id
            })

    return ProjectResponse(
        id = project.id,
        name = project.name,
        createdAt = project.createdAt,
        updatedAt = project.updatedAt,
        createdBy = member,
        members = members,
        bugs = list_bugs
    )


def get_project(db: Session, project_id: UUID):
    """Get project by ID"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    createdBy = db.query(User).filter(User.id == project.createdById).first()
    if not createdBy:
        raise HTTPException(status_code=404, detail="Creator user not found")

    # Get members of the project, including the `joinedAt` timestamp
    members = []
    for project_member in project.members:
        members.append(ProjectMemberResponse(
            id=project_member.id,
            joinedAt=project_member.joined_at,
            member=UserResponse(id=project_member.members.id, username=project_member.members.username)
        ))

    list_bugs = []
    bugs = db.query(Bug).filter(Bug.projectId == project.id).all()
    if bugs:
        for bug in bugs:
            list_bugs.append({
                "id": bug.id
            })

    return ProjectResponse(
        id = project.id,
        name = project.name,
        createdAt = project.createdAt,
        updatedAt = project.updatedAt,
        createdBy = createdBy,
        members = members,
        bugs = list_bugs
    )

def get_all_projects(db: Session, name: str = None, sort_by: str = "name", sort_order: str = "asc"):

    query = db.query(Project)

    if name:
        query = query.filter(Project.name.ilike(f"%{name}%"))

    if sort_by == "name":
        if sort_order == "asc":
            query = query.order_by(Project.name.asc())
        else:
            query = query.order_by(Project.name.desc())
    elif sort_by == "id":
        if sort_order == "asc":
            query = query.order_by(Project.id.asc())
        else:
            query = query.order_by(Project.id.desc())

    projects = query.all()

    if not projects:
        raise HTTPException(status_code=404, detail="No users found")

    project_responses = []

    for project in projects:
        # 🔹 Get project creator
        createdBy = db.query(User).filter(User.id == project.createdById).first()
        if not createdBy:
            raise HTTPException(status_code=404, detail=f"Creator user not found for project {project.id}")

        # 🔹 Get project members
        members = []
        for project_member in project.members:
            members.append(ProjectMemberResponse(
                id=project_member.id,
                joinedAt=project_member.joined_at,
                member=UserResponse(id=project_member.members.id, username=project_member.members.username)
            ))
        list_bugs = []
        bugs = db.query(Bug).filter(Bug.projectId == project.id).all()
        if bugs:
            for bug in bugs:
                list_bugs.append({
                    "id": bug.id
                })
        # 🔹 Build the response object
        project_responses.append(ProjectResponse(
            id=project.id,
            name=project.name,
            createdAt=project.createdAt,
            updatedAt=project.updatedAt,
            createdBy=createdBy,
            members=members,
            bugs= list_bugs  # Fetch bugs here if needed
        ))

    return project_responses

def update_project(db: Session, project_id: UUID, project_data: UpdateProject, current_user: str):

    print("data put: ", project_data)

    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project_data.name:
        project.name = project_data.name

    members = []
    if project_data.members:
        for member in project_data.members:
            project_member = ProjectMember(project_id=project.id, user_id=member, joined_at=datetime.now(timezone.utc))
            db.add(project_member)
            db.commit()
            db.refresh(project_member)

    for project_member in project.members:
        members.append(ProjectMemberResponse(
            id=project_member.id,
            joinedAt=project_member.joined_at,
            member=UserResponse(id=project_member.members.id, username=project_member.members.username)
        ))

    db.commit()
    db.refresh(project)
    return project

def add_members_project(db: Session, project_id: UUID, project_data: UpdateProject, current_user: dict):

    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project_data.name:
        project.name = project_data.name

    members = []
    if project_data.members:
        for member in project_data.members:
            project_member = ProjectMember(project_id=project.id, user_id=member, joined_at=datetime.now(timezone.utc))
            db.add(project_member)
            db.commit()
            db.refresh(project_member)

    for project_member in project.members:
        members.append(ProjectMemberResponse(
            id=project_member.id,
            joinedAt=project_member.joined_at,
            member=UserResponse(id=project_member.members.id, username=project_member.members.username)
        ))

    db.commit()
    db.refresh(project)
    return members

def delete_members_project(db: Session,project_id: UUID, member_id: UUID, current_user: str):

    project_member = db.query(ProjectMember).filter(ProjectMember.project_id == project_id, ProjectMember.user_id == member_id).first()
    if not project_member:
        raise HTTPException(status_code=404, detail="Project member not found")

    db.delete(project_member)
    db.commit()
    return {"message": "Project member deleted successfully"}

def delete_project(db: Session, project_id: UUID, current_user: dict):

    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(project)
    db.commit()

    return {"message": "Project deleted successfully"}
