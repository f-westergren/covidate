## Covid Event Spread Checker

**Goal**

The goal of this website is to help users research how events that involve big gatherings of people may have affected the spread of COVID-19 in their geographic area in USA (and later hopefully more countries). The user will enter a date and a location and the website will generate a response with about the spread (such as daily new cases etc) from that date and three weeks forward. 

**Expected Users**

The website does not aim to provide a service to a specific demographic, it will simply provide a quick way for people to check the spread from one date to another without having to go through complex sites with a lot of charts and statistics. 


**Data**

The website uses Mapquest's geolocation API (https://developer.mapquest.com/documentation/geocoding-api/) to let the user select a location for their search, and using that location it will get data from a suitable COVID-19 API. The data is pulled from NovelCOVID API (https://disease.sh/docs), which provides detailed historical information per county, province and subregion. 

The database schema consists of two tables - users and searches. It can be found here: https://dbdiagram.io/d/5eeaab869ea313663b3ab643.


**User Flow**

The front page might feature some Covid-related news or some interesting date searches. Anyone who goes to the site can do a date search. Enter location date and get a result. C3.js is used to generate charts from the results. Functionality includes user registration, edit user, save searches, delete searches and copy searches. 
