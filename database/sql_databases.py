from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

### Create Models ###
# class Hero(SQLModel, table=True):
#     id: int = Field(default=None, primary_key=True)
#     name: str = Field(index=True)
#     age: int | None = Field(default=None, index=True)
#     secret_name: str
    
### Create the database engine ###

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}

engine = create_engine(sqlite_url, connect_args=connect_args)


### Create the database tables ###
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    

### Create a Session Dependency ###

def get_session():
    with Session(engine) as session:
        yield session
        
SessionDependency = Annotated[Session, Depends(get_session)]


### Create Database Tables on Application Startup ###
from contextlib import asynccontextmanager

# We create the database tables on application startup to ensure
# that all required tables exist before handling any requests.

@asynccontextmanager
async def on_startup(app: APIRouter):
    create_db_and_tables()
    yield
    
router = APIRouter(lifespan=on_startup)

# For production using a migration script or tool like Alembic is recommended

### Create a Hero ###

# @router.post("/heroes/")
# def create_hero(hero: Hero, session: SessionDependency) -> Hero:
#     session.add(hero)
#     session.commit()
#     session.refresh(hero)
#     return hero

### Read Heroes with limit and offset to paginate the results. ###
# @router.get("/heroes/")
# def read_heroes(
#     session: SessionDependency,
#     offset: int = 0,
#     limit: Annotated[int, Query(le=100)] = 100
# ) -> list[Hero]:
#     heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
#     return list(heroes)


### Read one Hero by ID ###

# @router.get("/heroes/{hero_id}")
# def read_hero(hero_id: int, session: SessionDependency) -> Hero:
#     hero = session.get(Hero, hero_id)
#     if not hero:
#         raise HTTPException(status_code=404, detail="Hero not found")
#     return hero

### Delete a Hero by ID ###

# @router.delete("/heroes/{hero_id}")
# def delete_hero(hero_id: int, session: SessionDependency):
#     hero = session.get(Hero, hero_id)
#     if not hero:
#         raise HTTPException(status_code=404, detail="Hero not found")
#     session.delete(hero)
#     session.commit()
#     return {"ok": True}


### Create Multiple Models ###

class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    
class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    secret_name: str
    
class HeroResponse(HeroBase):
    id: int
    
class HeroCreate(HeroBase):
    secret_name: str
    
class HeroUpdate(SQLModel):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None

#### Create a Hero with the new models ###    
    
@router.post("/heroes/", response_model=HeroResponse)
def create_hero(hero: HeroCreate, session: SessionDependency):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

### Read Heroes with the new models ###

@router.get("/heroes/", response_model=list[HeroResponse])
def read_heroes(
    session: SessionDependency,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes

### Update a Hero by ID with the new models ###
@router.patch("/heroes/{hero_id}", response_model=HeroResponse)
def update_hero(hero_id: int, hero: HeroUpdate, session: SessionDependency):
    hero_db = session.get(Hero, hero_id)
    if not hero_db:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_data = hero.model_dump(exclude_unset=True)
    hero_db.sqlmodel_update(hero_data)
    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)
    return hero_db

### Delete a Hero by ID with the new models ###

@router.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDependency):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}