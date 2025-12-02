import os
import sys
from typing import List, Tuple

import pandas as pd
from pymongo import MongoClient, UpdateOne

# Self-contained Mongo initialization (no external import)
MONGO_URI = 'mongodb+srv://taalanzi35_db_user:TaaH-11233@stroke.xsvmyml.mongodb.net/'
DB_NAME = 'stroke_database'
COLLECTION_NAME = 'stroke_collection'
METADATA_COLLECTION = 'stroke_metadata'

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]
metadata_collection = db[METADATA_COLLECTION]



def project_root() -> str:
    return os.path.dirname(os.path.abspath(os.path.dirname(__file__)))


def csv_path() -> str:
    # Relative path provided by user: com7033-assignment-TahaniA3/stroke.csv
    return os.path.join(project_root(), 'stroke.csv')


def extract_headers(df: pd.DataFrame) -> List[str]:
    return list(df.columns)


def to_records(df: pd.DataFrame, headers: List[str]) -> List[dict]:
    """Convert dataframe rows to list of dictionaries with safe type coercion.

    The previous implementation used .astype('Int64') which raised:
    "cannot safely cast non-equivalent float64 to int64" when a column
    contained non-integer float values. We now coerce integer-like columns
    value-by-value, truncating/rounding only if they are very close to an
    integer (|x - round(x)| < 1e-9). Otherwise we log and cast via int() which
    effectively floors; adjust if a different policy is desired.
    """

    # Normalize NaN to None for MongoDB
    df = df.where(pd.notna(df), None)

    integer_like = ['id', 'age', 'hypertension', 'heart_disease', 'stroke']
    float_like = ['avg_glucose_level', 'bmi']

    # Coerce integer-like columns safely
    for col in integer_like:
        if col in df.columns:
            series = pd.to_numeric(df[col], errors='coerce')
            non_int_mask = series.notna() & (abs(series - series.round()) > 1e-9)
            non_int_count = int(non_int_mask.sum())
            if non_int_count:
                print(f"[WARN] Column '{col}' has {non_int_count} non-integer values; casting with int() (floor).")
            # Replace with int or None
            def to_int(val):
                if pd.isna(val):
                    return None
                try:
                    return int(val)
                except Exception:
                    return None
            df[col] = series.apply(to_int)

    # Coerce float-like columns
    for col in float_like:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').apply(lambda v: float(v) if pd.notna(v) else None)

    # Convert pandas NA to Python None
    records = []
    for rec in df.to_dict(orient='records'):
        # All numeric coercion already handled; ensure consistent types
        if 'id' in rec and isinstance(rec['id'], float):
            rec['id'] = int(rec['id'])
        # Embed headers list in each record if requested by user requirement
        rec['columns'] = headers
        records.append(rec)
    return records


def test_connection() -> None:
    info = client.server_info()
    print(f"Connected to MongoDB version: {info.get('version')}")
    print(f"Database: {DB_NAME}; Collection: {COLLECTION_NAME}")


def upsert_metadata(headers: List[str]) -> None:
    metadata_collection.update_one(
        {'_id': 'schema'},
        {'$set': {'headers': headers, 'count': len(headers)}},
        upsert=True
    )
    print(f"Stored headers metadata document with {len(headers)} columns.")


def main(drop_first: bool = False) -> None:
    path = csv_path()
    if not os.path.exists(path):
        raise FileNotFoundError(f'CSV not found at {path}')

    print(f'Reading CSV from: {path}')
    df = pd.read_csv(path)
    headers = extract_headers(df)
    print(f'CSV headers: {headers}')
    records = to_records(df, headers)
    print(f'Prepared {len(records)} records for upsert')

    if drop_first:
        print('Dropping existing documents in collection...')
        collection.delete_many({})

    # Upsert on patient id
    ops = [
        UpdateOne({'id': rec.get('id')}, {'$set': rec}, upsert=True)
        for rec in records if rec.get('id') is not None
    ]

    if not ops:
        print('No valid records with an id field were found. Aborting.')
        return

    result = collection.bulk_write(ops, ordered=False)
    print('Bulk upsert complete:')
    print(f' - matched: {result.matched_count}')
    print(f' - modified: {result.modified_count}')
    print(f' - upserted: {len(result.upserted_ids)}')

    # Store headers separately in metadata collection
    upsert_metadata(headers)

    # Simple verification: count documents
    doc_count = collection.count_documents({})
    print(f'Collection now contains {doc_count} documents.')
    sample = collection.find_one({}, projection={'_id': False})
    if sample:
        print('Sample document (truncated columns list):')
        if 'columns' in sample and isinstance(sample['columns'], list):
            sample['columns'] = sample['columns'][:5] + ['...']
        print(sample)


if __name__ == '__main__':
    drop = '--drop-first' in sys.argv
    print('Testing MongoDB connection...')
    test_connection()
    main(drop_first=drop)
