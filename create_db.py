import csv
import sqlite3
import requests

DB_NAME = 'us_covid_data.sqlite'

def create_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    drop_us_sql = 'DROP TABLE IF EXISTS "US"'
    drop_states_sql = 'DROP TABLE IF EXISTS "States"'
    drop_counties_sql = 'DROP TABLE IF EXISTS "Counties"'
    drop_census_count_sql = 'DROP TABLE IF EXISTS "Census_Counties"'
    drop_census_state_sql = 'DROP TABLE IF EXISTS "Census_States"'

    create_us_sql = '''
        CREATE TABLE IF NOT EXISTS "US" (
            "Id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "Date" DATE NOT NULL,
            "ConfirmedCases" INTEGER NOT NULL,
            "ConfirmedDeaths" INTEGER NOT NULL
        )
    '''

    create_states_sql = '''
        CREATE TABLE IF NOT EXISTS "States" (
            "Id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "StateId" INTEGER NOT NULL,
            "Date" DATE NOT NULL,
            "State" TEXT NOT NULL,
            "ConfirmedCases" INTEGER NOT NULL,
            "ConfirmedDeaths" INTEGER NOT NULL
        )
    '''

    create_counties_sql = '''
        CREATE TABLE IF NOT EXISTS "Counties" (
            "Id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "CountyId" INTEGER NOT NULL,
            "Date" DATE NOT NULL,
            "County" TEXT NOT NULL,
            "State" TEXT NOT NULL,
            "ConfirmedCases" INTEGER NOT NULL,
            "ConfirmedDeaths" INTEGER NOT NULL
        )
    '''

    create_census_count_sql = '''
        CREATE TABLE IF NOT EXISTS "Census_Counties" (
            "Id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "State_fips" INTEGER NOT NULL,
            "County_fips" INTEGER NOT NULL,
            "State" TEXT NOT NULL,
            "County" TEXT NOT NULL,
            "2010_Pop" INTEGER NOT NULL,
            "2019_PopEstimate" INTEGER NOT NULL
        )
    '''

    create_census_state_sql = '''
        CREATE TABLE IF NOT EXISTS "Census_States" (
            "Id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "State_fips" INTEGER NOT NULL,
            "County_fips" INTEGER NOT NULL,
            "State" TEXT NOT NULL,
            "County" TEXT NOT NULL,
            "2010_Pop" INTEGER NOT NULL,
            "2019_PopEstimate" INTEGER NOT NULL
        )
    '''
    cur.execute(drop_us_sql)
    cur.execute(drop_states_sql)
    cur.execute(drop_counties_sql)
    cur.execute(drop_census_count_sql)
    cur.execute(drop_census_state_sql)
    cur.execute(create_us_sql)
    cur.execute(create_states_sql)
    cur.execute(create_counties_sql)
    cur.execute(create_census_count_sql)
    cur.execute(create_census_state_sql)
    conn.commit()
    conn.close()

def load_us():
    file_contents = open('us_data.csv', 'r')
    csv_reader = csv.reader(file_contents)
    next(csv_reader)

    insert_us_sql = '''
        INSERT INTO US
        VALUES (NULL, ?, ?, ?)
    '''
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    for row in csv_reader:
        cur.execute(insert_us_sql, [
            row[0], #date
            row[1], #cases
            row[2], #deaths
        ])
    conn.commit()
    conn.close()

        
def load_count_census():
    file_contents = open('census_counties.csv','r')
    csv_reader = csv.reader(file_contents)
    next(csv_reader)

    insert_census_sql = '''
        INSERT INTO Census_Counties
        VALUES (NULL, ?, ?, ?, ?, ?, ?)
    '''
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    for row in csv_reader:
        cur.execute(insert_census_sql, [
            row[0], #State fips id
            row[1], #County fips id
            row[2], #State name
            row[3], #County name
            row[4], #2010 county population
            row[5], #2019 extimated county population
        ])
    conn.commit()
    conn.close()

def load_state_census():
    file_contents = open('census_states.csv','r')
    csv_reader = csv.reader(file_contents)
    next(csv_reader)

    insert_census_sql = '''
        INSERT INTO Census_States
        VALUES (NULL, ?, ?, ?, ?, ?, ?)
    '''
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    for row in csv_reader:
        cur.execute(insert_census_sql, [
            row[0], #State fips id
            row[1], #County fips id
            row[2], #State name
            row[3], #County name
            row[4], #2010 county population
            row[5], #2019 extimated county population
        ])
    conn.commit()
    conn.close()

def load_states():
    file_contents = open('us_state_data.csv', 'r')
    csv_reader = csv.reader(file_contents)
    next(csv_reader)
    
    insert_state_sql = '''
        INSERT INTO States
        VALUES (NULL,?, ?, ?, ?, ?)
    '''

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    for row in csv_reader:
        cur.execute(insert_state_sql,[
        row[2],# fips id
        row[0], #date
        row[1], #state
        row[3], #confirmed cases
        row[4], #confirmed deaths
    ])
    conn.commit()
    conn.close()

def load_counties():
    file_contents = open('us_state_county_data.csv','r')
    csv_reader = csv.reader(file_contents)
    next(csv_reader)

    select_county_id_sql = '''
        SELECT Id FROM Census_Counties
        WHERE County = ? AND State = ?
    '''

    insert_county_sql = '''
        INSERT INTO Counties
        VALUES (NULL, ?, ?, ?, ?, ?, ?)
    ''' 
    conn=sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    for row in csv_reader:
        #Get county id from census table
        cur.execute(select_county_id_sql, [row[1], row[2]])
        res = cur.fetchone()
        county_id = None
        if res is not None:
            county_id = res[0]
            cur.execute(insert_county_sql, [
            county_id,
            row[0], #date
            row[1], #county name
            row[2], #state
            row[4], #confirmed cases
            row[5], #confirmed deaths
        ])
    conn.commit()
    conn.close()

create_db()
load_us()
load_states()
load_state_census()
load_count_census()
load_counties()
