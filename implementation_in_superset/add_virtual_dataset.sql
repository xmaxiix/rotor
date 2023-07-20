-- The query is used to create a virtual data set that can be used as datasource.
-- This could lead to performance problems with larger data sets, but for the purpose of the prototype it is an easy way to create meaningful charts and apply filters to all of them

SELECT sensor_readings.reading_id
       ,sensor_readings.sensor_id
       ,sensor_readings.timestamp_utc
       ,sensor_readings.measured_temperature
       ,machines.machine_id
       ,machines.machine_name
       ,machines.in_operation_time
       ,machines.in_use
       ,machines.usual_temperature
       ,(sensor_readings.measured_temperature - machines.usual_temperature) AS "temperature_deviation"
       ,machines.production_site_id
       ,production_sites.city
       ,production_sites.latitude
       ,production_sites.longitude
       ,production_sites.iso_code
FROM
       sensor_readings
       LEFT JOIN machines
        ON sensor_readings.sensor_id = machines.sensor_id
       LEFT JOIN production_sites
        ON machines.production_site_id = production_sites.production_site_id
;