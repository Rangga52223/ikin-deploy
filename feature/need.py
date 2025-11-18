import pandas as pd
import numpy as np
from feature.helper.cleaning import clean_df_tel, combine_data_tel_weather
from db_control.save_data import insert_race_telematry,  safe_project, delete_pro, edit_project
from base_response import succes_response , error_response
import io

async def track_tel_handle(telemetry_file, weather_file, id):
    # Read uploaded files
    telemetry_content = await telemetry_file.read()
    weather_content = await weather_file.read()
    
    # Convert to pandas dataframes
    df = pd.read_csv(io.BytesIO(telemetry_content))
    df2 = pd.read_csv(io.BytesIO(weather_content), sep=';')
    
    # Process dataframes
    df_tel = clean_df_tel(df)
    df_comb = combine_data_tel_weather(df_tel, df2)
    insert_race_telematry(df_comb, id)
    
    # Cleanup
    del df, df2, df_comb, df_tel
    return succes_response(message='File Uploaded')

def create_project(name, circuit, Note = None):
    try:
        id_project = safe_project(name, circuit, Note)
        return succes_response(message='ok', data=id_project)
    except Exception as e:
        return error_response(http_status=402, message=f'error = {str(e)}')
    
def delete_project(id):
    try:
        delete_pro(id)
        return succes_response(message="deleted project success")
    except Exception as e:
        return error_response(http_status=402, message=f'Error = {str(e)}')
    
def update_data(id, new_name, circuit):
    try:
        edit_project(id, new_name, circuit)
        return succes_response(message='update data success')
    except Exception as e:
        return error_response(message='Error update data')
    
    
    

    





