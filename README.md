# Rotor - Implementation of a case study

## Background information
This project was developed as part of my studies. In the module "Data Analytics and Big Data", I had the task to design a system architecture for a medium-sized rotor blade manufacturer that is suitable for the company according to the described requirements of the case study. Following on from this, a prototype should be developed to represent the task of a tool within the overall architecture.
I will not share the given case and the related task as I assume that the publication of this is legally protected by my university. However, for general understanding, it is important to know that the company collects temperature data of their manufacturing machines and wants to analyse it.

## Idea for the prototype
I have proposed *Apache Superset* (superset) in my system architecture for the visualization of the data and decided to implement this tool in its functionality as a prototype: 
- To begin with, I made superset locally available on my computer according to the instructions in this [guide](https://superset.apache.org/docs/installation/installing-superset-using-docker-compose).
- Since I was not provided with a sample data set for the task and could not find a suitable data set online that I could have adapted to my case, I needed to create a fictitious database first:
    - To do this, I initially set up a database using *PostgreSQL*, which I can later connect to superset.
    - I decided to create three different tables to store my sample data, see [database_setup.sql](database_setup.sql).
    - I arbitrarily invented the data for the tables on production sites and machines.
    - The previous approach is unfortunately not appropriate for easily creating larger amounts of data, such as temperature data sets from sensors in my case. That is why I created a the Python script [generation_of_sensor_readings.py](generation_of_sensor_readings.py), which generates some random data for my purpose.
    - Finally, I used the script [data_entry.sql](data_entry.sql) to enter the data into my database.
- Once my intended data was available, I designed a sample dashboard in superset:
    - I created a virtual data set based on the query [add_virtual_dataset.sql](implementation_in_superset/add_virtual_dataset.sql).
    - I created various charts and added other general information to my data that I wanted to display (see [add_iso_codes.sql](implementation_in_superset/add_iso_codes.sql) and [add_usual_temperature.sql](implementation_in_superset/add_usual_temperature.sql)).
    - A demonstration of the finished interactive dashboard can be found in [dashboard_demo.md](implementation_in_superset/dashboard_demo.md) in the form of short screen recordings.