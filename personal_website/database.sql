CREATE DATABASE IF NOT EXISTS personal_website;
USE personal_website;

CREATE TABLE users (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Firstname VARCHAR(50),
    Middlename VARCHAR(50),
    Lastname VARCHAR(50),
    birthday DATE,
    age INT,
    contact_number VARCHAR(20),
    email VARCHAR(100),
    username VARCHAR(50) UNIQUE,
    password VARCHAR(255),
    role ENUM('admin','User') DEFAULT 'User',
    Status ENUM('active','inactive') DEFAULT 'inactive',
    GameAccess ENUM('enabled','disabled') DEFAULT 'enabled',
    Municipality VARCHAR(100),
    Province VARCHAR(100),
    Zipcode VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
