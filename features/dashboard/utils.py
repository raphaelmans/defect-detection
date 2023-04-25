

from db import AppDatabase
from features.dashboard.db_queries import DB_Queries

class Utils:
    database = None

    def __init__(self, database):
        self.database = database

    def get_defect_rate_per_batch(self):
        query = DB_Queries.defect_rate_per_batch_query()
        res = AppDatabase.run_query_one_no_cache(self.database, query)
        print("🚀 ~ file: utils.py:17 ~ res:", res)
        return res

    def get_defect_rate_over_time(self):
        query = DB_Queries.defect_rate_over_time_query()
        res = AppDatabase.run_query_one_no_cache(self.database, query)
        print("🚀 ~ file: utils.py:25 ~ res:", res)
        return res

    def get_defect_rate_by_product_model(self):
        query = DB_Queries.defect_rate_by_product_model_query()
        res = AppDatabase.run_query_one_no_cache(self.database, query)
        print("🚀 ~ file: utils.py:38 ~ res:", res)
        return res
