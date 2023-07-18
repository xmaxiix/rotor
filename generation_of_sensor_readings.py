import csv 
import random
import datetime

# Function for generating fictitious sensor data
def generate_sensor_data(num_sensors, start_timestamp, end_timestamp, min_interval_minutes, max_interval_minutes, temperature_ranges, temperature_exception_cases, expected_cases, expected_times):
    data = []
    
    sensor_ids = list(range(1, num_sensors + 1))

    for i in range(num_sensors):
        sensor_id = sensor_ids[i]

        timestamp = start_timestamp
        previous_temperature = None
        exception_case = False
        exceptions_count = 0
        minutes_cumulated = 0

        while timestamp < end_timestamp:
            day = timestamp.weekday()
            hour = timestamp.hour

            if previous_temperature is not None:
                max_increase = temperature_ranges[i][2] - previous_temperature
                min_decrease = previous_temperature - temperature_ranges[i][0]

                if exceptions_count >= expected_cases[i] and minutes_cumulated >= expected_times[i]:
                    exceptions_count = 0
                    minutes_cumulated = 0

                if day in range(0,5) and hour in range(6,19):

                    if expected_cases[i] == 0:
                        if previous_temperature > temperature_ranges[i][1]:
                            max_deviation = min(min_decrease, 3)
                            temperature = round(previous_temperature - random.uniform(0, max_deviation),2)
                            
                        elif min_decrease <= 1.5:
                            max_deviation = min(max_increase,3)
                            temperature = round(previous_temperature + random.uniform(0, max_deviation),2)

                        else:
                            max_deviation = min(min_decrease, max_increase)
                            max_deviation = min(max_deviation, 2)
                            temperature = round(previous_temperature + random.uniform(-1 * max_deviation, max_deviation), 2)
                    
                    elif (exceptions_count == 0) or (exception_case == True) or (minutes_cumulated >= (exceptions_count * expected_times[i]/expected_cases[i])):
                        max_deviation = min(max_increase,3)
                        temperature = round(previous_temperature + random.uniform(0, max_deviation),2)
                        exception_case = True
                    
                    elif (exception_case == False):

                        if previous_temperature > temperature_ranges[i][1]:
                            max_deviation = min(min_decrease, 3)
                            temperature = round(previous_temperature - random.uniform(0, max_deviation),2)
                            
                        elif min_decrease <= 1.5:
                            max_deviation = min(max_increase,3)
                            temperature = round(previous_temperature + random.uniform(0, max_deviation),2)

                        else:
                            max_deviation = min(min_decrease, max_increase)
                            max_deviation = min(max_deviation, 2)
                            temperature = round(previous_temperature + random.uniform(-1 * max_deviation, max_deviation), 2)
                    
                    else:
                        print("Case not considered!")
                    
                    if temperature >= temperature_exception_cases[i]:
                        exceptions_count += 1
                        exception_case = False

                else:
                    if previous_temperature > 23:
                        temperature = round(previous_temperature - random.uniform(0.5, 1.5), 2)

                    elif previous_temperature <= 18:
                        temperature = round(previous_temperature + random.uniform(0.5, 1.5), 2)

                    else:
                        temperature = round(previous_temperature + random.uniform(-0.5,0.5), 2)

            else:
                if day in range(0,5) and hour in range(6,19):
                    temperature = round(random.uniform(temperature_ranges[i][0], temperature_ranges[i][2]), 2)
                else:
                    temperature = round(20 + random.uniform(-2,3), 2)

            reading_id = len(data) + 1
            data.append([reading_id, sensor_id, timestamp, temperature])

            random_time = random.uniform(min_interval_minutes, max_interval_minutes)
            timestamp += datetime.timedelta(minutes=random_time)
            
            minutes_cumulated += random_time
            previous_temperature = temperature

    return data

# Function that writes the generated data to a csv file
def write_data_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['reading_id', 'sensor_id', 'timestamp_utc', 'measured_temperature'])
        writer.writerows(data)

# Set parameters
num_sensors = 8
start_timestamp = datetime.datetime(2022, 9, 1)
end_timestamp = datetime.datetime(2023, 5, 1)
min_interval_minutes = 0.5
max_interval_minutes = 5
temperature_ranges = [
    [15, 20, 43], 
    [13, 21, 42],   
    [21, 24, 59],   
    [20, 23, 55],   
    [15, 28, 60],   
    [16, 22, 28],   
    [18, 22, 40],   
    [18, 22, 41]    
]
temperature_exception_cases = [
    36, 
    34,
    45,
    39,
    50,
    0,
    31,
    32
]
expected_cases = [
    2,
    3,
    1,
    2,
    1,
    0,
    3,
    4
]
expected_times = [
    18765,
    47016,
    4321,
    65843,
    20160,
    0,
    18600,
    25000
]

# Generate data set
data = generate_sensor_data(num_sensors, start_timestamp, end_timestamp, min_interval_minutes, max_interval_minutes, temperature_ranges, temperature_exception_cases, expected_cases, expected_times)

# Write data set to a csv file
write_data_to_csv(data, 'sensor_readings.csv')