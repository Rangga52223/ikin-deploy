from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class save_project_data(BaseModel):
    project_name : str
    circuit : str
    note : Optional[str] = None

class edit_project_sch(BaseModel):
    id  : UUID
    new_name : str
    circuit : Optional[str] = None

class get_data(BaseModel):
    id_document : UUID
    id_veh  : str

class get_veh_data(BaseModel):
    vehicle_id : str
