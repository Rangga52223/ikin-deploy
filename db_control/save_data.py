from db_control.db_connect import SessionLocal
from db_control.model import RaceTelematry, ProjectName
from sqlalchemy.exc import SQLAlchemyError
from base_response import error_response
import uuid 
from datetime import datetime, timezone
import pandas as pd
import numpy as np
db = SessionLocal()
def insert_race_telematry(df, id_name_file):
    print('Debug: Save data')
    data_list = df.to_dict(orient="records")
    allowed = {
        "timestamp","meta_session","original_vehicle_id","outing","vehicle_id","vehicle_number","lap",
        "Laptrigger_lapdist_dls","Steering_Angle","VBOX_Lat_Min","VBOX_Long_Minutes","accx_can","accy_can",
        "aps","ath", "gear","nmot","pbrake_f","pbrake_r","speed","timestamp_dt",
        "AIR_TEMP","TRACK_TEMP","HUMIDITY","PRESSURE","WIND_SPEED","WIND_DIRECTION","RAIN"
    }

    objects = []
    for row in data_list:
        filtered = {}
        for k, v in row.items():
            if k in allowed:
                if pd.isna(v):
                    filtered[k] = None
                elif hasattr(v, "to_pydatetime"):
                    filtered[k] = v.to_pydatetime()
                elif isinstance(v, (np.integer, np.floating, np.bool_)):
                    filtered[k] = v.item()
                else:
                    filtered[k] = v
        objects.append(RaceTelematry(id_project=id_name_file, **filtered))

    db.add_all(objects)
    db.commit()

# def insert_file_name(file_name):
#     id_file_name = str(uuid.uuid4())
#     obj = File(id_name_file=id_file_name, name_file=file_name, created_at=datetime.now(timezone.utc))
#     db.add(obj)
#     db.commit()
#     db.refresh(obj)
#     return id_file_name


def safe_project(name,circuit, Note = None):
    id_project = str(uuid.uuid4())
    obj = ProjectName(id=id_project, project_name=name, circuit = circuit, note = Note)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return id_project

def delete_pro(id):
    data_delete = db.query(ProjectName).get(id)
    db.delete(data_delete)
    db.commit()

def edit_project(id: str, name: str, circuit: str = None):
    try:
        # 1. AMBIL OBJEK MODEL MENGGUNAKAN .first()
        # project_update sekarang adalah objek ProjectName, BUKAN Query
        project_item = db.query(ProjectName).filter(ProjectName.id == id).first()

        if not project_item:
            # 2. Logika pemeriksaan keberadaan objek
            return error_response(success=False, message='Project not found')
        
        project_item.project_name = name
        
        # Atribut circuit hanya diubah jika nilai baru diberikan (bukan None)
        if circuit is not None:
             project_item.circuit = circuit
        
        # 4. Commit Perubahan
        db.commit()
        db.refresh(project_item)
        
        return {"success": True, "data": project_item} # Asumsi sukses_response
        
    except SQLAlchemyError as e:
        # PENTING: Rollback transaksi sebelum raise/return error
        db.rollback() 
        return error_response(success=False, message=f'Database Error during update: {e}')
    
    except Exception as e:
        # Rollback juga untuk kesalahan non-SQLAlchemy
        db.rollback() 
        return error_response(success=False, message=f'General Error: {e}')
        


