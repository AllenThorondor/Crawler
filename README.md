# Crawler
Crawler object with functions
## done:
* 1  add in class like scrawler, teller, scheduler 
* 2  define core function such as process_core and wheels

## planed features:
* 1  got the email extension for notification of process completed.
	
	- refer to ShiHao code of mail part
	
	  [1]: https://github.com/Holmes-Shelly/html2pyForGUO/blob/master/0620.py#L22	"/html2pyForGUO/0620.py"
	  [2]: https://github.com/Holmes-Shelly/intel2py/blob/master/Beta0319.py	"Holmes-Shelly/intel2py/Beta0319.py"
	
	  
	
	- 
	
	- 

## Code structure:

### Crawler object:

Feature :

- Get_url, get_image, get_content, get_title

- keep the save option on, when choose to save more than on image, give back the list of image and convert it to a BLOB format   

Planed feature:

- Get_timestamp, get_author

- get_inserted_img

  > Get_inserted_img will insert into the content a signal , and download the inserted_img saved at a table,  and reinsert into the content once pulled out .

### Scheduler object:

Feature:

- Update_database
- check_duplicate (history of chat with HaoShi, updated immediately )
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

1. Learn matplotlib quickly and learn the real time part carefully (done 2 / 10)
   1. completed line and bar plot, next is pie chart
   2. will keep going on pie charts tonight
2. Learn the NumPy as fundemental bases for Matplotlib , now we have the Indian guy video and the study material from 400 coder camp as well. try to learn it as soon as possible (1 / 3)
   1. india guy video (not start yet)
   2. 400 coder material (numpy part is awesome) (3 / 10)
   3. Refresh the pandas method :
      1. Best practice video on data school from Kevin Markham (0 / 10) 
3. Concurrency program for python, learning material fron 400 coder first, find more on YouTube 
4. Coery Schafer's flask tutorial (what is this thing doing) ( 0 / 15)
5. Djangle learning for blog setup , and we should have this done after matplotlib is done, and keep it rolling while doing other things, maybe 1 or 2 hrs per day is good.(0 / 17)
6. 











