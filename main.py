from http.client import HTTPException

from fastapi import FastAPI, Depends
from sqlmodel import Session, select
from models import Cat, Mission, Target
from database import create_db_and_tables, get_session
import requests
app = FastAPI(title="Spy Cat Agency API")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/cats/", response_model=Cat)
def create_cat(cat: Cat, session: Session = Depends(get_session)):

    response = requests.get("https://api.thecatapi.com/v1/breeds")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Breed validation service unavailable")

    breeds = [b["name"].lower() for b in response.json()]
    if cat.breed.lower() not in breeds:
        raise HTTPException(status_code=400, detail=f"Invalid breed: {cat.breed}")

    session.add(cat)
    session.commit()
    session.refresh(cat)
    return cat


@app.get("/cats/", response_model=list[Cat])
def list_cats(session: Session = Depends(get_session)):
    return session.exec(select(Cat)).all()


@app.get("/cats/{cat_id}", response_model=Cat)
def get_cat(cat_id: int, session: Session = Depends(get_session)):
    cat = session.get(Cat, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    return cat


@app.put("/cats/{cat_id}/salary", response_model=Cat)
def update_cat_salary(cat_id: int, salary: float, session: Session = Depends(get_session)):
    cat = session.get(Cat, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    cat.salary = salary
    session.add(cat)
    session.commit()
    session.refresh(cat)
    return cat


@app.delete("/cats/{cat_id}")
def delete_cat(cat_id: int, session: Session = Depends(get_session)):
    cat = session.get(Cat, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    session.delete(cat)
    session.commit()
    return {"ok": True}


@app.post("/targets/", response_model=Target)
def create_target(target: Target, session: Session = Depends(get_session)):
    session.add(target)
    session.commit()
    session.refresh(target)
    return target


@app.get("/targets/", response_model=list[Target])
def list_targets(session: Session = Depends(get_session)):
    return session.exec(select(Target)).all()


@app.get("/targets/{target_id}", response_model=Target)
def get_target(target_id: int, session: Session = Depends(get_session)):
    target = session.get(Target, target_id)
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")
    return target


@app.put("/targets/{target_id}/notes", response_model=Target)
def update_target_notes(target_id: int, notes: str, session: Session = Depends(get_session)):
    target = session.get(Target, target_id)
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")

    mission = session.get(Mission, target.mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    if mission.status.lower() == "done":
        raise HTTPException(status_code=400, detail="Cannot update target notes for completed mission")

    target.notes = notes
    session.add(target)
    session.commit()
    session.refresh(target)
    return target


@app.post("/missions/", response_model=Mission)
def create_mission(mission: Mission, session: Session = Depends(get_session)):
    # Проверяем количество целей
    if not mission.targets or not (1 <= len(mission.targets) <= 3):
        raise HTTPException(status_code=400, detail="A mission must have 1 to 3 targets")

    session.add(mission)
    session.commit()
    session.refresh(mission)
    return mission


@app.put("/missions/{mission_id}/assign_cat/{cat_id}", response_model=Mission)
def assign_cat_to_mission(mission_id: int, cat_id: int, session: Session = Depends(get_session)):
    mission = session.get(Mission, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    cat = session.get(Cat, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")

    # Проверяем, что у кота нет другой активной миссии
    active_mission = session.exec(
        select(Mission).where(Mission.cat_id == cat_id, Mission.complete == False)
    ).first()
    if active_mission:
        raise HTTPException(status_code=400, detail=f"Cat {cat.name} already has an active mission")

    mission.cat_id = cat_id
    session.add(mission)
    session.commit()
    session.refresh(mission)
    return mission


@app.delete("/targets/{target_id}")
def delete_target(target_id: int, session: Session = Depends(get_session)):
    target = session.get(Target, target_id)
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")
    session.delete(target)
    session.commit()
    return {"ok": True}



@app.post("/missions/", response_model=Mission)
def create_mission(mission: Mission, session: Session = Depends(get_session)):
    session.add(mission)
    session.commit()
    session.refresh(mission)
    return mission

@app.get("/missions/", response_model=list[Mission])
def list_missions(session: Session = Depends(get_session)):
    return session.exec(select(Mission)).all()

@app.get("/missions/{mission_id}", response_model=Mission)
def get_mission(mission_id: int, session: Session = Depends(get_session)):
    mission = session.get(Mission, mission_id)
    if not mission:
        return {"error": "Mission not found"}
    return mission

@app.delete("/missions/{mission_id}")
def delete_mission(mission_id: int, session: Session = Depends(get_session)):
    mission = session.get(Mission, mission_id)
    if not mission:
        return {"error": "Mission not found"}
    if mission.cat_id is not None:
        return {"error": "Mission already assigned to a cat, cannot delete"}
    session.delete(mission)
    session.commit()
    return {"ok": True}



@app.put("/missions/{mission_id}/complete", response_model=Mission)
def complete_mission(mission_id: int, session: Session = Depends(get_session)):
    mission = session.get(Mission, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")


    mission.complete = True


    for target in mission.targets:
        target.complete = True
        session.add(target)

    session.add(mission)
    session.commit()
    session.refresh(mission)
    return mission
