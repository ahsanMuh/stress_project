-- Insert data into the Admin table
INSERT INTO Admin (name, username, phone, company, email, password, created_at, updated_at)
VALUES ('Alpha Charlie', 'uid001', 1234567890, 'Company A', 'admin1@companya.com', 'password123', NOW(), NOW()),
       ('Bravo Charlie', 'uid002', 9876543210, 'Company B', 'admin2@companyb.com', 'password456', NOW(), NOW());

-- Insert data into the Employee table
INSERT INTO Employee (name, admin_id)
VALUES ('John Doe', 1),
       ('Jane Smith', 2),
       ('Bob Johnson', 1);

-- Insert data into the Stress table
INSERT INTO Stress (employee_id, stress_level, datetime)
VALUES (1, TRUE, '2022-01-01 09:00:00'),
       (1, FALSE, '2022-01-02 13:00:00'),
       (2, TRUE, '2022-01-03 11:00:00'),
       (3, FALSE, '2022-01-04 15:00:00');