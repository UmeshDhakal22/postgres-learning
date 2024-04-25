from sqlmodel import SQLModel, Field


class Project(SQLModel, table=True):
    __tablename__ = "project"

    id: int = Field(primary_key=True)
    ward_name: str = Field(index=True, nullable=True)
    tag: str = Field(index=True, nullable=True)
    bboxes: str = Field(index=True, nullable=True)


class ProjectAll(SQLModel, table=True):
    __tablename__ = "project_all"

    id: int = Field(primary_key=True)
    ward_name: str = Field(index=True, unique=True, nullable=True)
    tag: str = Field(index=True, unique=True, nullable=True)
    bboxes: str = Field(index=True, unique=True, nullable=True)
