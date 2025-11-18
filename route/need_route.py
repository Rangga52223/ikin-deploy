from route import need
from fastapi import UploadFile, File, Form
from base_response import error_response
from feature.need import create_project, delete_project, track_tel_handle, edit_project
from feature.helper.schema import save_project_data, edit_project_sch

@need.post('/upload')
async def upload_r(
    telemetry_file: UploadFile = File(...),
    weather_file: UploadFile = File(...),
    id: str = Form(...)
):
    print('Debug: Upload')
    if not all([telemetry_file, weather_file, id]):
        return error_response(message='file or filename not found')
    return await track_tel_handle(telemetry_file, weather_file, id)

@need.post('/save_project')
async def save_project_r(data : save_project_data):
    try:
        name = data.project_name
        circuit = data.circuit
        note = data.note
        return create_project(name, circuit, note)
    except:
        return error_response(message='Error creat project')

@need.delete('/delete_project/{id}')
async def delete_project_r(id):
    try: 
        return delete_project(id)
    
    except Exception as e:
        return error_response(http_status=402, message="erro for request delete")
    
@need.put('/update_project')
async def update_project_r(user : edit_project_sch):
    try:
        id = user.id
        new_name = user.new_name
        circuit = user.circuit
        return edit_project(id, new_name, circuit)
    
    except:
        return error_response(message='Error Update Project')
