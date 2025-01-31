import time
from datetime import datetime

import pandas as pd

import firebase

db = firebase.db
bulk_writer = db.bulk_writer()
batch = db.batch()
collection = db.collection('gathering')
doc_ref = db.collection("gathering").document()

location_data = ['latitude', 'longitude', 'district', 'province', 'address']
weather_data = ['humidity', 'rainfall', 'atmospheric_pressure',
                'max_temperature', 'cloud', 'wind_direction',
                'min_temperature', 'wind']
pest_data = ['pest_population_counts', 'disease_incidence', 'severity_of_infestations']
soil_data = ['soil_nutrient_levels', 'soil_moisture', 'soil_temperature', 'soil_ph']
irrigation_data = ['water_discharged', 'water_quality', 'water_consumed', 'water_withdrawn', 'water_recycled']


def create_data_item(row):
    return {
        'date': datetime.combine(row['datetime'], datetime.min.time()),
        'fertilize': row.get('fertilize', None),
        'weather': {key: row.get(key, None) for key in weather_data},
        'pest': {key: row.get(key, None) for key in pest_data},
        'irrigation': {key: row.get(key, None) for key in irrigation_data},
        'soil': {key: row.get(key, None) for key in soil_data},
    }


def write_data_to_firestore(df):
    bulk_writer = db.bulk_writer()

    for index, row in df.iterrows():
        data_item = create_data_item(row)
        facility = row.get('facility', None)
        data = {
            'facility': facility,
            'location': {key: row.get(key, None) for key in location_data},
            'data': data_item
        }
        bulk_writer.set(doc_ref, data)

    bulk_writer.flush()


def delete_all_documents(collection):
    docs = collection.list_documents()
    for doc in docs:
        doc.delete()


if __name__ == '__main__':
    df = pd.read_excel('./data.xlsx', sheet_name='data_temp')
    start = time.time()
    write_data_to_firestore(df)
    end = time.time()
    print(f'Execution time: {end - start} seconds')
    # delete_all_documents(collection)
