-- Create Batch table
CREATE TABLE Batch (
    id INT PRIMARY KEY AUTO_INCREMENT,
    date TIMESTAMP,
    batch_name VARCHAR(255),
    product_model VARCHAR(255),
    department VARCHAR(255),
    total_items INT
) AUTO_INCREMENT=1;

-- Create ClassificationResult table
CREATE TABLE ClassificationResult (
    id INT PRIMARY KEY AUTO_INCREMENT,
    class VARCHAR(10),
    batch_id INT,
    created_at TIMESTAMP,
    FOREIGN KEY (batch_id) REFERENCES Batch(id)
);
