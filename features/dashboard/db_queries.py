

class DB_Queries:
    @staticmethod
    def defect_rate_per_batch_query():
        return """
                SELECT b.id,b.batch_name, b.total_items, SUM(CASE WHEN cr.class_name = 'No Good' THEN 1 ELSE 0 END) AS defect_count, SUM(CASE WHEN cr.class_name = 'No Good' THEN 1 ELSE 0 END)/b.total_items AS defect_rate FROM Batch b JOIN ClassificationResult cr ON b.id = cr.batch_id GROUP BY b.id;
            """

    @staticmethod
    def defect_rate_over_time_query():
        return """
SELECT DATE(b.date) AS date, 
       SUM(CASE WHEN cr.class_name = 'No Good' THEN 1 ELSE 0 END) / SUM(b.total_items) AS defect_rate
FROM Batch b
JOIN ClassificationResult cr ON b.id = cr.batch_id
GROUP BY DATE(b.date)
"""

    @staticmethod
    def defect_rate_by_product_model_query():
        return """
SELECT b.product_model, SUM(CASE WHEN cr.class_name = 'No Good' THEN 1 ELSE 0 END)/SUM(b.total_items) AS defect_rate
FROM Batch b
JOIN ClassificationResult cr ON b.id = cr.batch_id
GROUP BY b.product_model;
"""
