-- Enter data to production_sites table
INSERT INTO production_sites (production_site_id, city, latitude, longitude)
VALUES (1, 'Husum', 54.485378, 9.053620),
       (2, 'Grimma', 51.238682, 12.726540),
       (3, 'Barleben', 52.205559, 11.618830),
       (4, 'Sömmerda', 51.159439, 11.118720),
       (5, 'Eisenberg', 50.968201, 11.900720),
       (6, 'Kolkwitz', 51.749506, 14.256707);

-- Enter data to machines table
INSERT INTO machines (machine_id, machine_name, in_operation_time, in_use, production_site_id, sensor_id)
VALUES (1, 'Turm', '2022-06-01', true, 1, 1),
       (2, 'Leiter', '2022-06-01', true, 1, 2),
       (3, 'Zahnkranz', '2022-09-01', true, 4, 3),
       (4, 'Gondel', '2022-09-01', true, 6, 4),
       (5, 'Generator', '2022-09-01', true, 3, 5),
       (6, 'Anemometer', '2022-09-01', true, 1, 6),
       (7, 'Rotorblatt', '2022-09-01', true, 2, 7),
       (8, 'Rotornabe', '2022-09-01', true, 5, 8);

-- Enter data to sensor_readings table
COPY sensor_readings (reading_id, sensor_id, timestamp_utc, measured_temperature) FROM '/Users/maxirudolph/projects/rotor/sensor_readings.csv' DELIMITER ',' CSV HEADER;