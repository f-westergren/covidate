## Covid Event Spread Checker

**Goal**

The goal of this website is to help users research how events that involve big gatherings of people may have affected the spread of COVID-19 in their geographic area (primarily North America). The user will enter a date and a location and the website will generate a response with about the spread (such as daily new cases etc) from that date and three weeks forward. 

**Expected Users**

The website does not aim to provide a service to a specific demographic, it will simply provide a quick way for people to check the spread from one date to another without having to go through complex sites with a lot of charts and statistics. 


**API**

The website will use a geolocation API such as Mapquest or Google Maps API to let the user select a location for their search, and using that location it will get data from a suitable COVID-19 API. Most of the data (if not all) will be pulled from NovelCOVID API (https://disease.sh/docs), which provides detailed historical information per county, province and subregion. 

The database schema consists of two tables - users and searches. It can be found here: https://dbdiagram.io/d/5eeaab869ea313663b3ab643.


**User Flow**

The front page might feature some Covid-related news or some interesting date searches. Anyone who goes to the site can do a date search. Enter location date and get a result. The searches that will provide results that look visually good. Ideally there will be a graph as well as data outlining the change in cases. Functionality will include user registration, save searches, modify searches, delete searches and copy searches. 

Once users have created a search, they will have the option to save that search. If they do they will be prompted to register or log in. When they are logged in, they will have a simple dashboard with a link to their searches and the front page search field. They will be able to edit their searches, delete them, or copy them and create a new modified search from the copied search. 
