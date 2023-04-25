class BatchInsertDTO:
    def __init__(self, date, batch_name, product_model, department, total_items):
        self.date = date
        self.batch_name = batch_name
        self.product_model = product_model
        self.department = department
        self.total_items = total_items

    def to_tuple(self):
        return (self.date, self.batch_name, self.product_model, self.department, self.total_items)


def insert_new_batch(batch_dto, db):

    sql = "INSERT INTO Batch (date, batch_name, product_model, department, total_items) VALUES (%s, %s, %s, %s, %s)"

    cursor = db.cursor()

    values = batch_dto.to_tuple()
    cursor.execute(sql, values)

    db.commit()

    return cursor.lastrowid
