from sqlalchemy import String,Integer,Column
from sqlalchemy.orm import declarative_base,sessionmaker
from src.util import get_sql_server_engine

Base=declarative_base()

class Resume(Base):
    __tablename__='Resumes'

    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String(100))
    email=Column(String(100))
    phone=Column(String(20))
    education_summary=Column(String)
    experience_summary=Column(String)
    projects=Column(String)

def insert_resume_data(data:dict):
    engine=get_sql_server_engine()
    Base.metadata.create_all(engine)

    Session=sessionmaker(bind=engine)
    session=Session()

    try:
        resume=Resume(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            education_summary=data.get('education_summary'),
            experience_summary=data.get('experience_summary'),
            projects="; ".join(data.get('projects', []))
        )
        session.add(resume)
        session.commit()
        print("Resume data inserted successfully")

    except Exception as e:
        session.rollback()
        print("Error occured",e)
    
    finally:
        session.close()
