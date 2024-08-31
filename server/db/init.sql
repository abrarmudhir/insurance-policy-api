CREATE DATABASE insurance_db;

\c insurance_db

CREATE TABLE policies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    coverage_amount FLOAT NOT NULL,
    premium FLOAT NOT NULL
);

INSERT INTO policies (name, coverage_amount, premium) VALUES
('Policy A', 100000.00, 500.00),
('Policy B', 200000.00, 1000.00),
('Policy C', 300000.00, 1500.00);
