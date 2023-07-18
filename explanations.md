# Explanations regarding the implementation

As already mentioned in [README.md](README.md), I had no suitable data for the further processing of the case study. So I tried to imagine what data my sample company would probably collect and analyse. I will try to explain my thoughts on this below.

## Table of contents
1. [Tables](#tables)
2. [Data](#data)
3. [Script explanation](#script-explanation)

## Tables

It was clear to me that I would need temperature data in any case. According to the case description, these were present in non-relational format, but simulating this would have been beyond both my capabilities and the reasonableness of the project. Instead, I decided to create the table *sensor_readings* with the columns
- *reading_id* (as primary key),
- *sensor_id* (to assign the record to a sensor),
- *timestamp_utc* (for recording the time of temperature recording or data transmission) and
- *measured_temperature* (to record a fictitious temperature).

In addition, I have created the tables *production_sites* and *machines*. These will serve me as dimensions later and offer me the possibility to put the temperature data into context.

## Data

After I had set up a database and created the tables according to my idea, my next step was to feed them with data. For the tables *production_sites* and *machines* this was easily done. I simply thought up completely arbitrary values and inserted them into my database using SQL statements. Obviously this step would not work for the temperature data. I therefore decided to write a Python script that generates data for my case through a slightly more complex function and individually defined parameters.

## Script explanation

The script can be divided into four parts:

**1. Import of libraries**
- I have included the standard Python libraries **csv** , **random** and **datetime**.

**2. Definition of functions**
- **generate_sensor_data** is used to generate sensor readings including the set parameters
- **write_data_to_csv** writes the generated data to a csv file so that it can subsequently be read into a database.

**3. Definition of variables and specification of parameters**
- It was important to me to have the possibility to set different parameters in my script and thus to influence the output.

**4. Generation and storage of the data by executing the functions with the set parameters**
- By executing the functions, random data is generated and stored in a csv file.  

---

In the following, I will describe in much detail how I tried to create a script that would take into account various conditions that I had in mind in order to get as variable and realistic data as (for me) possible.

### Parameters

Below are the adjustable parameters and the values I used to generate my data:
```python 
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
```
- `num_sensors` - For how many sensors should data be recorded?
- `start_timestamp` - From what date on should data be recorded?
- `end_timestamp` - Until what date should data be recorded?
- `min_interval_minutes` - What is the minimum number of minutes a timestamp can deviate from the previous one?
- `max_interval_minutes` - What is the maximum number of minutes a timestamp can deviate from the previous one?

The number of values/ranges to be specified in the following lists must be exactly the same as the number of sensors:
- `temperature_ranges` - In which range can the measured temperatures vary? 
    - `temperature_ranges[0]` - minimum temperature
    - `temperature_ranges[1]` - usual temperature
    - `temperature_ranges[2]` - maximum temperature
- `temperature_exception_cases` - What temperature is considered an exception case? 
- `expected_cases` - How many exception cases are expected? 
- `expected_times` - After how many minutes should the expected exception cases occur? 

### Function: generate_sensor_data

From a high-level perspective, the function for generating sensor data is structured as below:

```python 
def generate_sensor_data(num_sensors, start_timestamp, end_timestamp, min_interval_minutes, max_interval_minutes, temperature_ranges, temperature_exception_cases, expected_cases, expected_times):
    data = []
    
    sensor_ids = list(range(1, num_sensors + 1))

    for i in range(num_sensors):
        [...]

    return data
```

- The function will consider all parameter that have been set.
- An empty list `data` is created, in which the generated data records are added during runtime.
- A list is created for `sensor_ids`, which stores as many values as defined in `num_sensors` in ascending order from 1.
- A loop follows (`for i in range(num_sensors)`), which ensures that the code is run through as often as there are sensors.
- When this loop has been passed through, the function returns the filled list `data`.

```python 
sensor_id = sensor_ids[i]

timestamp = start_timestamp
previous_temperature = None
exception_case = False
exceptions_count = 0
minutes_cumulated = 0

while timestamp < end_timestamp:
    [...]

reading_id = len(data) + 1
data.append([reading_id, sensor_id, timestamp, temperature])

random_time = random.uniform(min_interval_minutes, max_interval_minutes)
timestamp += datetime.timedelta(minutes=random_time)
            
minutes_cumulated += random_time
previous_temperature = temperature
```

- Initially, the specific `sensor_id` and other relevant variables for the data generation are defined. These variables are
    - `timestamp`,
    - `previous_temperature`,
    - `exception_case`,
    - `exceptions_count` and
    - `minutes_cumulated`.
- The code will then run as long as the variable `timestamp` is smaller than the specified end time (`end_timestamp`).
- In this loop there are different principles to generate a temperature value. *These will be explained in the following sections.*
- After generating a `temperature` and a `reading_id` (depending on the existing data sets in the list `data`), the new data set consisting of `reading_id`, `sensor_id`, `timestamp` and `temperature` is added to the list `data`.
- Then a random number of minutes (`random_time`) is generated and added to the variable `timestamp`.
- The time increase in minutes (`minutes_cumulated`) and the temperature as the previous temperature for the next record (`previous_temperature`) are updated.

```python 
day = timestamp.weekday()
hour = timestamp.hour

if previous_temperature is not None:
    max_increase = temperature_ranges[i][2] - previous_temperature
    min_decrease = previous_temperature - temperature_ranges[i][0]

    if exceptions_count >= expected_cases[i] and minutes_cumulated >= expected_times[i]:
        exceptions_count = 0
        minutes_cumulated = 0

    if day in range(0,5) and hour in range(6,19):
        [...]

    else:
        if previous_temperature > 23:
            temperature = round(previous_temperature - random.uniform(0.5, 1.5), 2)

        elif previous_temperature <= 18:
            temperature = round(previous_temperature + random.uniform(0.5, 1.5), 2)

        else:
            temperature = round(previous_temperature + random.uniform(-0.5,0.5), 2)

else:
    if day in range(0,5) and hour in range(6,19):
        temperature = round(random.uniform(temperature_ranges[i][0], temperature_ranges[i][1]), 2)
    else:
        temperature = round(20 + random.uniform(-2,3), 2)
```

- The day and hour of the timestamp are determined.
    - `weekday()` returns the day of the week as an integer, where Monday is 0 and Sunday is 6.
    - `hour` returns an integer value in range(24).
    - These values are later used to check operating times. The operating times in my example are Monday to Friday (`range[0,5]`) from 6 to 18 (`range[6,19]`).
- Afterwards it is checked if there is already a previous temperature (`if previous_temperature is not None`):
    - Case 1: There is already a previous temperature.
        - It is determined how much the temperature is allowed to rise or fall (`max_increase`/`min_decrease`). The threshold values of `temperature_ranges` serve as reference here.
        - A check is made whether the expected exceptions were reached in the expected time. If so, the variables `exceptions_count` and `minutes_cumulated` are reset to `0`.
        - It is also checked whether the timestamp is within the operating times or not. In case the timestamp is beyond the operating times, the following logic is applied:
            - If the previous temperature is above 23, then a value is generated as temperature, which results from the previous temperature reduced by a value between 0.5 and 1.5.
            - If the previous temperature is less than or equal to 18, then a value is generated as temperature, which results from the previous temperature increased by a value between 0.5 and 1.5.
            - Otherwise, a value is generated as temperature which is within the range of the previous temperature +/- 0.5.
            - *After the next code section, the generation of temperature values during operating times will be explained in detail.*
    - Case 2: There is no previous temperature yet.
        - If the timestamp is within the operating times: Any number within the temperature range of the sensor is recorded as the temperature.
        - If the timestamp is beyond the operating times: A temperature between 18 and 23 is recorded. This range was chosen because it can be assumed to be room temperature and a machine out of operation should also have approximately this temperature.

```python
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
```

- Using various condition checks, I have tried to steer the temperature change so that during the set time `expected_times[i]` as many exceptions occur as defined in `expected_cases[i]`
- Case 1:
    - the number of expected cases equals `0`.
- Case 2:
    - the counted cases are `0` or
    - the variable `exception_case` equals `True` or
    - the cumulative time is less than `(exceptions_count * expected_times[i]/expected_cases[i])`, which is the average time in minutes until an/the next exception case should occur.
- Case 3:
    - the variable `exception_case` equals `False`.
- To make sure that any case is considered, I have included this message to indicate if it is not so.
- Depending on the case, there are different principles by which a value for the temperature will be generated:
    - for Case 1 & 3:
        - If the previous temperature is higher than the usual temperature, the previous temperature value is decreased by 0 to a maximum of 3 degrees.
        - If the previous temperature is 1.5 or less degrees above the lower limit, then the previous temperature value is increased by 0 to a maximum of 3 degrees.
        - Otherwise, the change in temperature value is within a range of +/- 2 degrees maximum.
    - for Case 2:
        - The previous temperature value is increased by 0 to a maximum of 3 degrees to force a temperature rise.
        - Furthermore, the variable `exception_case` is set to `True` to indicate that an exception case is generated.
- After a temperature has been generated, it is checked whether the value is equal to or higher than the set temperature for exceptions. If this is the case, the exception case is counted and the variable `exception_case` is set to `False`.