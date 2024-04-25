import os
from sqlmodel import create_engine, Session, select
from fastapi.responses import JSONResponse
from models import Project, ProjectAll


class DatabaseMaker:
    def __init__(
        self,
        ward=None,
        bbox=None,
        tags=None,
    ):
        db_name = os.getenv("POSTGRES_DB")
        db_user = os.getenv("POSTGRES_USER")
        db_pw = os.getenv("POSTGRES_PW")
        db_host = os.getenv("POSTGRES_HOST")
        db_port = os.getenv("POSTGRES_PORT")
        db_url = f"postgresql://{db_user}:{db_pw}@{db_host}:{db_port}/{db_name}"
        self.engine = create_engine(db_url)
        self.ward = ward
        self.tags = tags
        self.bbox = bbox

    def create_project_table(self):
        session = Session(self.engine)
        try:
            Project.metadata.create_all(self.engine)
            print("Project table created successfully.")
        except Exception as e:
            if "already exists" in str(e):
                print("Project table already exists.")
            else:
                raise e

        with session:
            if self.ward:
                existing_project = session.exec(
                    select(Project).where(Project.ward_name == self.ward)
                ).first()
                if existing_project:
                    session.close()
                    return JSONResponse(content={"message": f"Project with ward_name '{self.ward}' already exists."})
                else:
                    project = Project(ward_name=self.ward)
            elif self.tags:
                print('I am here')
                existing_project = session.exec(
                    select(Project).where(Project.tag == self.tags)
                ).first()
                print(existing_project)
                if existing_project:
                    print('data is there')
                    session.close()
                    return JSONResponse(content={"message": f"Project with ward_name '{self.tags}' already exists."})
                else:
                    project = Project(tag=self.tags)
            else:
                print(self.bbox)
                print(type(self.bbox))
                existing_project = session.exec(
                    select(Project).where(Project.bboxes == self.bbox)
                ).first()
                if existing_project:
                    session.close()
                    return JSONResponse(content={"message": f"Project with ward_name '{self.bbox}' already exists."})
                else:
                    project = Project(bboxes=self.bbox)

            session.add(project)
            session.commit()
            print("Added successfully")

    def create_project_table_separate(self):
        session = Session(self.engine)
        try:
            ProjectAll.metadata.create_all(self.engine)
            print("ProjectAll table created successfully.")
        except Exception as e:
            if "already exists" in str(e):
                print("ProjectAll table already exists.")
            else:
                raise e

        with session:
            if self.ward:
                project = ProjectAll(ward_name=self.ward)
            elif self.bbox:
                project = ProjectAll(bboxes=self.bbox)
            else:
                project = ProjectAll(tag=self.tags)

            session.add(project)
            session.commit()
            print("Added successfully")
