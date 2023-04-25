import statistics
from functools import reduce
import operator
from datetime import datetime


def flat_result_data(data):
    return reduce(operator.iconcat, data, [])


def filter_data_by_treshold(records, threshold):
    return list(filter(lambda record: record['confidence'] > threshold, records))


def get_categories(data):
    categories_found = []

    for obj in data:
        category = obj['name']
        if categories_found.count(category) == 0:
            categories_found.append(category)

    return categories_found


def export_to_json(json_str, file_number):
    with open('./output/batch-'+str(file_number)+'.json', 'w') as f:
        f.write(json_str)


def get_mysql_timestamp():
    # Get the current datetime object
    now = datetime.now()

    # Format the datetime object as a MySQL timestamp string
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    # Return the timestamp string
    return timestamp


