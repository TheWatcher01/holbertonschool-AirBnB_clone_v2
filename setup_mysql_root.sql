-- Create the database 'hbnb_root_db' if it does not already exist
CREATE DATABASE IF NOT EXISTS hbnb_root_db;

-- Switch to the 'hbnb_root_db' database for subsequent commands
USE hbnb_root_db;

-- Create the user 'hbnb_root' with the password 'hbnb_root_pwd' if it does not already exist
-- and set the authentication method to 'mysql_native_password'
CREATE USER IF NOT EXISTS 'root' @'localhost' IDENTIFIED
WITH
    mysql_native_password BY 'hbnb_root_pwd';

-- Grant all privileges on the 'hbnb_root_db' database to the 'hbnb_root' user
GRANT ALL PRIVILEGES ON hbnb_root_db.* TO 'root' @'localhost';

-- Grant the 'hbnb_root' user the privilege to select from the 'performance_schema' database
GRANT SELECT ON performance_schema.* TO 'root' @'localhost';

-- Refresh any changes to the privileges
FLUSH PRIVILEGES;

-- Test if the user and database are accessible
SELECT DATABASE() AS "Current Database", USER () AS "Current User";