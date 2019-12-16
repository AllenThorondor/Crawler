# Crawler
Crawler object with functions
## to be done:
* when update the database, the num_id should fetch from the latest database (done)
* to stop scraping right when the count hit the limit (20191216)
* good looking action need to be done also

## planed features:
* 1  got the email extension for notification of process completed.
	
	refer to ShiHao code of mail part
	
	[1]: https://github.com/Holmes-Shelly/html2pyForGUO/blob/master/0620.py#L22	"/html2pyForGUO/0620.py"
	[2]: https://github.com/Holmes-Shelly/intel2py/blob/master/Beta0319.py	"Holmes-Shelly/intel2py/Beta0319.py"
	
	status update: got some condition: gmail blocked by gov and QQ mail is not available currently, so I have to apply for a new email account. and up to now my focus will migrate to the new funciton of name check component .
	
* 2  got the name check fucntion done .

  1. to create a crawler for below web- site link:

     [1]: https://www.babynames.com/name	"the content source website for crawling"
     [2]: https://www.behindthename.com/name	"the figure data source"

     I have done some code on this , and it works just good

  2. to create a database for the data that been scraped, the table structure is some kind of tricky job.

     1. the "name_id", "name", "name_meaning", "origin", "popularity", from baby name
     2. the "rating" from behind the name
     3. store the figure data scraped from the behind the name
  
* 3  add proxy and header function for crawler class. proxy may need to scrap the website

## 

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
3. and insert another table for Image store if the option is on

### Draw plot graph:

1. Source of data which will be plotted comes from?
2. Generate thumbernails of image scraped from the website
3. maybe will output the graphs as PPT of PDF format for sharing and review



## Operation flow:

To be done 













