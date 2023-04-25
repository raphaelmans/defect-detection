from statistics import mode

from helper import get_mysql_timestamp


class ClassificationResultInsertDTO:
    def __init__(self, class_name, batch_id, created_at):
        self.class_name = class_name
        self.batch_id = batch_id
        self.created_at = created_at

    def to_tuple(self):
        return (self.class_name, self.batch_id, self.created_at)

    def to_dict(self):
        return {"class_name": self.class_name, "batch_id": self.batch_id, "created_at": self.created_at}


def insert_new_result(result_dto: ClassificationResultInsertDTO, db):
    sql = "INSERT INTO ClassificationResult (class_name, batch_id, created_at) VALUES (%s, %s, %s)"
    cursor = db.cursor()
    values = result_dto.to_tuple()

    cursor.execute(sql, values)
    db.commit()
    return cursor.lastrowid


def save_class_results_to_db(my_dict,db):
    if db is not None:
        for key in my_dict:
            label = my_dict[key]['class_name']
            batch_id = my_dict[key]['batch_id']
            created_at = my_dict[key]['created_at']

            dto = ClassificationResultInsertDTO(label, batch_id, created_at)
            sql = "INSERT INTO ClassificationResult (class_name, batch_id, created_at) VALUES (%s, %s, %s)"
            cursor = db.cursor()
            values = dto.to_tuple()

            cursor.execute(sql, values)
        db.commit()
