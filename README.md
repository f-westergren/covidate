# CoviDate - Covid-19 Outbreak Tracker
The goal of this website is to help users research how events that involve big gatherings of people may have affected the spread of COVID-19 in their geographic area in USA. The user will enter a date and a location and the website generates a response with information about the local spread of the virus on a county level from that date and three weeks forward.

The site is deployed here: [https://covidate.herokuapp.com/].

## Data
The site uses two APIs:

1. [disease.sh](https://disease.sh/). A free-to-use multi-source open disease API. They source data from [John Hopkins University](https://github.com/CSSEGISandData/COVID-19) and [Worldometers](https://www.worldometers.info/coronavirus/) among others. 
2. [Mapquest](https://developer.mapquest.com/). Their Geocoding API is used to for place search to determine the location the user wants to generate data for. 

## Features
- Search for a location in the US and get information on the spread of Covid-19 in the region. 
- Switch between deaths and cases, and toggle daily cases and deaths.
- Display data from the selected date and 15 days forward, or until today's date.
- Sign up for an account to be able to save searches and revisit them later.

## User Flow
1. On the landing page, the user can enter a location and date and generate a chart with data. Through the navbar the user can also log in and sign up.
2. Once a search is generated the user can toggle between data for 15 dates from the selected search date or until today's date. The user can also toggle between showing number of deaths or cases, as well as showing a second graph with the daily change.
3. Logged in users can enter a description for their search and save it. If a user isn't logged in they can still save the search, and will be redirected to the log in page. Once logged in the search will be saved.
4. Logged in users can access their dashboard showing their saved searches. They can switch between the saved searches and toggle the same information as on the landing page. They can also choose to delete a search.


## Tech Stack
- Backend: Python, Flask, SQLAlchemy, Postgres
- Frontend: Javascript, C3.js

## Database Diagram
An overview of the database is set up can be found [here](https://dbdiagram.io/d/5eeaab869ea313663b3ab643).
