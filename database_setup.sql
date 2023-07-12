-- Create table for production sites
CREATE TABLE production_sites
(
    production_site_id int,
    city               varchar(50),
    latitude           real,
    longitude          real
);

-- Create table for manufacturing machines
CREATE TABLE machines
(
    machine_id         int,
    machine_name       varchar(60),
    in_operation_time  date,
    in_use             boolean,
    production_site_id int,
    sensor_id          int
);

-- Create table for measured temperature
CREATE TABLE sensor_readings
(
    reading_id           int,
    sensor_id            int,
    timestamp_utc        timestamp,
    measured_temperature real
);