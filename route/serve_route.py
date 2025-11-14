from route import serve
from feature.serve import get_docs_ser, get_veh_id, get_tele_data
from feature.helper.schema import get_data
import uuid
@serve.get('/docs')
async def get_docs_r():
    return get_docs_ser()

@serve.get('/veh_id_data/{file_id}')
async def get_veh_id_r(file_id : uuid.UUID):
    return get_veh_id(file_id)

@serve.post('/car_data')
async def get_car_dat_r(veh_data : get_data):
    id_doc = veh_data.id_document
    veh_id = veh_data.id_veh
    return get_tele_data(id_doc, veh_id)