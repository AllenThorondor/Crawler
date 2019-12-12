# Crawler
Crawler object with functions
## done:
* 1  add in class telle
* 2  give Teller method db_setup and customer_service

## planed features:
* 1  update the function for scrap_to_database() 
	- fix by 5 download the website feature
	- fix the image insert problem 
		solution : keep the save option on, when choose to save more than on image, give back the list of image and convert it to a BLOB format   

## Code structure:

### Crawler object:

Feature :

- Get_url, get_image, get_content, get_title



Planed feature:

- Get_timestamp, get_author

- get_inserted_img

  > Get_inserted_img will insert into the content a signal , and download the inserted_img saved at a table,  and reinsert into the content once pulled out .

### Scheduler object:

Feature:

- Update_database
- xiaoshabi
- Feed_to_database

Planed feature:

not yet



### Teller object:

Feature:

- Customer _service function fet back all the needed information from user by interact using line command
- Db_setup
- Db_openup

Planed feature:

not yet





## Core function:

### Process_core

### wheels

### insert into database function:

1. which type of database will this crawler use( currently we have sqlite basically)
2. Data base structure optimisation for URLs and Pages
3. and insert another table for Image store if the option is on .

### Draw plot graph:

1. Source of data which will be plotted comes from?
2. Generate thumbernails of image scraped from the website
3. maybe will output the graphs as PPT of PDF format for sharing and review



## Operation flow:

To be done 



## Study list:

1. Learn matplotlib quickly and learn the real time part carefully
2. learn the NumPy as fundemental bases for Matplotlib , now we have the Indian guy video and the study material from 400 coder camp as well. try to learn it as soon as possible
3. concurrency program for python, learning material fron 400 coder first, find more on YouTube 
4. djangle learning for blog setup , and we should have this done after matplotlib is done, and keep it rolling while doing other things, maybe 1 or 2 hrs per day is good.











