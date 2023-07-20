-- The usual temperature value should serve as a critical indicator.

-- Add column
ALTER TABLE machines ADD COLUMN usual_temperature real;

-- Add values according to temperature_ranges[1] used in the Python script
UPDATE machines
SET usual_temperature = 
    CASE
        WHEN machine_id = 1 THEN 20
        WHEN machine_id = 2 THEN 21
        WHEN machine_id = 3 THEN 24
        WHEN machine_id = 4 THEN 23
        WHEN machine_id = 5 THEN 28
        WHEN machine_id = 6 THEN 22
        WHEN machine_id = 7 THEN 22
        WHEN machine_id = 8 THEN 22
    END
WHERE machine_id in (1,2,3,4,5,6,7,8);