import time
from datetime import datetime
import firebase
import pandas as pd
from collections import deque

db = firebase.db
bulk_writer = db.bulk_writer()
batch = db.batch()
collection = db.collection('gathering')


def create_data_item(row):
    return {
        'date': datetime.combine(row['datetime'], datetime.min.time()),
        'weather': {key: row.get(key, None) for key in
                    ['humidity', 'rainfall', 'atmospheric_pressure', 'max_temperature', 'cloud', 'wind_direction',
                     'min_temperature', 'wind']},
        'pest': {key: row.get(key, None) for key in
                 ['pest_population_counts', 'disease_incidence', 'severity_of_infestations']},
        'irrigation': {key: row.get(key, None) for key in
                       ['water_discharged', 'water_quality', 'water_consumed', 'water_withdrawn', 'water_recycled']},
        'fertilize': row.get('fertilize', None),
        'soil': {key: row.get(key, None) for key in
                 ['soil_nutrient_levels', 'soil_moisture', 'soil_temperature', 'soil_ph']},
    }


def write_data_to_firestore(df):
    facility_docs = {}
    facility_data = {}
    facility_exists = {}

    bulk_writer = db.bulk_writer()

    for index, row in df.iterrows():
        data_item = create_data_item(row)
        facility = row.get('facility', None)

        doc_ref = facility_docs.setdefault(facility, collection.document())
        if facility not in facility_data:
            if facility not in facility_exists:
                doc = doc_ref.get()
                facility_exists[facility] = doc.exists
            if facility_exists[facility]:
                data = doc.to_dict()
                facility_data[facility] = deque(data.get('data', []))
            else:
                facility_data[facility] = deque()

        facility_data[facility].append(data_item)

        data = {
            'facility': facility,
            'location': {key: row.get(key, None) for key in
                         ['district', 'latitude', 'address', 'province', 'longitude']},
            'data': list(facility_data[facility])
        }

        if facility_exists[facility]:
            bulk_writer.update(doc_ref, data)
        else:
            bulk_writer.set(doc_ref, data)
            facility_exists[facility] = True

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
