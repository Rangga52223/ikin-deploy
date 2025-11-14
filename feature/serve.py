from db_control.db_connect import SessionLocal
from sqlalchemy import select
from sqlalchemy.orm import Session
from db_control.model import RaceTelematry, ProjectName
from base_response import succes_response, error_response
from datetime import datetime, date
import uuid

db : Session = SessionLocal()

def serialize_model(obj):
    result = {}
    for col in obj.__table__.columns:
        val = getattr(obj, col.name)
        if isinstance(val, (datetime, date)):
            result[col.name] = val.isoformat()
        elif isinstance(val, uuid.UUID):
            result[col.name] = str(val)
        else:
            result[col.name] = val
    return result

def get_docs_ser():
    rows = db.execute(select(ProjectName)).scalars().all()
    data = [serialize_model(r) for r in rows]
    return succes_response(message='ok', data=data)

def get_veh_id(doc_id):
    statement = select(RaceTelematry.vehicle_id).where(RaceTelematry.id_project == doc_id).distinct()
    rows = db.execute(statement).scalars().all()
    return succes_response(message='ok', data=rows)

def get_tele_data(doc_id, veh_id):
    statement = select(RaceTelematry.timestamp,
                       RaceTelematry.speed,
                       RaceTelematry.gear,
                       RaceTelematry.nmot,
                       RaceTelematry.pbrake_f,
                       RaceTelematry.pbrake_r,
                       RaceTelematry.aps,
                       RaceTelematry.accy_can,
                       RaceTelematry.lap,
                       RaceTelematry.VBOX_Lat_Min,
                       RaceTelematry.VBOX_Long_Minutes).where(RaceTelematry.vehicle_id == veh_id, RaceTelematry.id_project == doc_id)
    row = db.execute(statement).mappings().all()
    data = [dict(row) for row in row]
    return succes_response(message='ok', data=data)


