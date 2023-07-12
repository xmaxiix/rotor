import csv
import random
import datetime

# Function for generating fictitious sensor data
def generate_sensor_data(num_sensors, start_timestamp, end_timestamp, interval_minutes):
    data = []
    timestamp = start_timestamp
    sensor_ids = list(range(1, num_sensors + 1))

    previous_temperatures = {}

    while timestamp <= end_timestamp:
        for sensor_id in sensor_ids:
            if sensor_id in previous_temperatures:
                temperature = round(previous_temperatures[sensor_id] + random.uniform(-0.5, 0.5), 2)
            else:
                temperature = round(random.uniform(15, 80), 2)

            reading_id = len(data) + 1
            data.append([reading_id, sensor_id, timestamp, temperature])
            timestamp += datetime.timedelta(minutes=interval_minutes)

            previous_temperatures[sensor_id] = temperature

        timestamp += datetime.timedelta(minutes=interval_minutes)

    return data

# Function that writes the generated data to a csv file
def write_data_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['reading_id', 'sensor_id', 'timestamp_utc', 'measured_temperature'])
        writer.writerows(data)

# Set number of sensors and period of data recording
num_sensors = 8
start_timestamp = datetime.datetime(2022, 9, 1)
end_timestamp = datetime.datetime(2023, 7, 16)
interval_minutes = 1

# Generate data set
data = generate_sensor_data(num_sensors, start_timestamp, end_timestamp, interval_minutes)

# Write data set to a csv file
write_data_to_csv(data, 'sensor_readings.csv')