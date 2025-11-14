import pandas as pd
def clean_df_tel(df):
    print('DEBUG: Clean_df')
    for c in ['expire_at', 'meta_source']:
        if c in df.columns:
            df = df.drop(columns=c)

    # 1. Tentukan SEMUA kolom yang DIJAMIN harus ada
    # Kolom Metadata yang diambil dari df
    meta_cols = ["timestamp", "meta_session", "meta_time", "original_vehicle_id",
                 "outing", "vehicle_id", "vehicle_number", "lap"]
    
    # Kolom Telemetri yang dihasilkan dari pivot
    telemetry_cols = [
        "Laptrigger_lapdist_dls", "Steering_Angle", "VBOX_Lat_Min", "VBOX_Long_Minutes", 
        "accx_can", "accy_can", "aps", "ath", "gear", "nmot", 
        "pbrake_f", "pbrake_r", "speed"
        # Perhatikan: Kolom data cuaca (AIR_TEMP, TRACK_TEMP, dll.) tidak termasuk dalam daftar ini
    ]

    # Gabungkan semua kolom yang diharapkan
    required_cols = meta_cols + telemetry_cols
    
    # 2. Lakukan Pivot
    df_pivot = df.pivot_table(
        index="timestamp",
        columns="telemetry_name",
        values="telemetry_value",
        aggfunc="first"
    ).reset_index()

    # 3. Gabungkan Metadata
    # Hanya ambil kolom metadata yang benar-benar ada di input df
    actual_meta_cols = [c for c in meta_cols if c in df.columns]
    meta_df = df[actual_meta_cols].drop_duplicates(subset="timestamp")
    
    final_df = pd.merge(meta_df, df_pivot, on="timestamp", how="left")
    final_df = final_df.sort_values(by="timestamp").reset_index(drop=True)

    # 4. Memastikan Semua Kolom Ada (JAMINAN STRUKTUR) ⬅️ MODIFIKASI INI
    # Tambahkan kolom yang hilang dan atur ulang urutan kolom.
    # Kolom yang hilang akan diisi dengan NaN (Null).
    missing_cols = list(set(required_cols) - set(final_df.columns))
    for col in missing_cols:
        final_df[col] = pd.NA # Mengisi dengan NA/NaN

    # Atur ulang kolom sesuai urutan yang diinginkan
    final_df = final_df.reindex(columns=required_cols)

    # 5. Operasi Pembersihan dan Pengisian Null (Interpolasi/Median)
    
    # safe operations (Karena kita sudah menjamin kolom ada, kita bisa menghapus 'if c in final_df.columns' 
    # untuk kolom telemetri yang dijamin ada, tapi pertahankan untuk keamanan)
    
    if 'nmot' in final_df.columns:
        # buat nearest median neighborhood
        final_df['nmot'] = final_df['nmot'].fillna(final_df['nmot'].rolling(window=30, min_periods=1, center=True).median())
    if 'speed' in final_df.columns:
        final_df['speed'] = final_df['speed'].fillna(final_df['speed'].rolling(window=30, min_periods=1, center=True).median())
    if 'Laptrigger_lapdist_dls' in final_df.columns:
        final_df['Laptrigger_lapdist_dls'] = final_df['Laptrigger_lapdist_dls'].interpolate(
            method='linear',
            limit_direction='both'
        )
        # Bagian ini tetap sama
        try:
            _ = final_df.groupby('lap', include_groups=False).apply(lambda x: x.loc[x['Laptrigger_lapdist_dls'] >= 200].head(1))
        except TypeError:
            _ = final_df.groupby('lap').apply(lambda x: x.loc[x['Laptrigger_lapdist_dls'] >= 200].head(1))

    return final_df

def combine_data_tel_weather(df, df2):
    print('DEBUG: Combine_Weather ')
    # jika ada kolom epoch seconds, langsung parse
    if 'TIME_UTC_SECONDS' in df2.columns:
        try:
            df2['timestamp_dt'] = pd.to_datetime(df2['TIME_UTC_SECONDS'], unit='s', utc=True)
        except Exception:
            # jika parsing gagal, buang kolom dan lanjutkan detection
            df2 = df2.drop(columns='TIME_UTC_SECONDS')
    # jika belum ada timestamp_dt, coba kolom umum
    if 'timestamp_dt' not in df2.columns:
        candidates = ['TIME_UTC_STR', 'TIME_UTC', 'TIME', 'time', 'timestamp']
        found = False
        for col in candidates:
            if col in df2.columns:
                temp = pd.to_datetime(df2[col], utc=True, errors='coerce')
                if temp.notna().any():
                    df2['timestamp_dt'] = temp
                    found = True
                    break
        # fallback: coba deteksi otomatis pada kolom objek/datetime
        if not found:
            for col in df2.columns:
                if pd.api.types.is_object_dtype(df2[col]) or pd.api.types.is_datetime64_any_dtype(df2[col]) or pd.api.types.is_integer_dtype(df2[col]):
                    temp = pd.to_datetime(df2[col], utc=True, errors='coerce', unit='s' if pd.api.types.is_integer_dtype(df2[col]) else None)
                    if temp.notna().any():
                        df2['timestamp_dt'] = temp
                        found = True
                        break
        if not found:
            raise KeyError(f"No suitable time column found in weather dataframe. Available columns: {list(df2.columns)}")

    # pastikan telemetry punya kolom timestamp
    if 'timestamp' not in df.columns:
        raise KeyError("No 'timestamp' column found in telemetry dataframe.")
    df['timestamp_dt'] = pd.to_datetime(df['timestamp'], utc=True, errors='coerce')
    if df['timestamp_dt'].isna().all():
        raise ValueError("Failed to parse telemetry 'timestamp' column into datetimes.")

    # urutkan dan merge_asof (tolerance bisa disesuaikan)
    df_tel = df.sort_values('timestamp_dt')
    df_weath = df2.sort_values('timestamp_dt')
    df_merged = pd.merge_asof(
        df_tel,
        df_weath,
        on='timestamp_dt',
        direction='nearest',
        tolerance=pd.Timedelta('5s')  # ubah sesuai kebutuhan atau hapus tolerance jika tidak diinginkan
    )
    return df_merged