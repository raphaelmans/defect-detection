

import streamlit
from db import AppDatabase
from features.models.batch import BatchInsertDTO, insert_new_batch
from features.models.classification_result import ClassificationResultInsertDTO, insert_new_result
from helper import get_mysql_timestamp


conn = AppDatabase.init_connection()
print("=====DB CONNECTED=====")


def create_data():
    # Create a BatchInsertDTO object with mock data
    batch_dto = BatchInsertDTO(
        date=get_mysql_timestamp(),
        batch_name='Test Batch',
        product_model='Model 123',
        department='Production',
        total_items=100
    )

    # Insert the new batch into the database and get the ID
    batch_id = insert_new_batch(batch_dto, conn)

    return batch_id


def create_data_result():
    # Create a BatchInsertDTO object with mock data
    batch_id = create_data()
    result_dto = ClassificationResultInsertDTO(

        created_at=get_mysql_timestamp(),
        class_name='No Good',
        batch_id=batch_id
    )

    # Insert the new batch into the database and get the ID
    result_id = insert_new_result(result_dto, conn)

    return result_id


streamlit.button('Test Create Batch', on_click=create_data)
streamlit.button('Test Create Result', on_click=create_data_result)
