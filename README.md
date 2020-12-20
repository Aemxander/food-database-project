# Houhou Discord Bot
This Discord bot connects to many different APIs and can be added to a Discord server to allow users to get the functionality of the APIs without leaving Discord!

If you would like to test out the bot you can join the discord server by clicking this [link]! 



## APIs
APIs currently in use by the bot:
* [Alpha Vantage]
* [icanhazdadjoke]
* [NASA APOD]
* [NASA Image and Video Library]
* [NASA Mars Rover Photos]
* [OMBd]
* [RoboHash]



## Commands
#### <ins>CAT COMMANDS</ins>
<ins>!cat</ins>
 * Sends a random cat GIF
 
<ins>!cat upvote</ins>
 *  Upvotes the last cat GIF

<ins>!cat downvote</ins>
 *  Upvotes the last cat GIF <br>

#### <ins>DOG COMMANDS</ins>
<ins>!dog</ins>
 * Sends a random dog GIF

<ins>!dog upvote</ins>
 * Upvotes the last dog GIF

<ins>!dog downvote</ins>
 * Upvotes the last dog GIF <br>

#### <ins>IMBD COMMANDS</ins>
<ins>!imbd TITLE</ins>
 * Searches IMBd for information on the movie/series based on the title
 * `Ex. !imbd Life of Pi`

<ins>!imbd search TITLE</ins>
 * Searches IMBd for movies/series based on the title
 * `Ex. !imbd search Prisoners` <br>
 
#### <ins>JOKE COMMANDS</ins>
<ins>!joke</ins>
 * Sends a random dad joke

<ins>!joke SEARCHTERM</ins>
 * Sends a random dad joke based on the search term
 * `Ex. !joke Teacher` <br>
 
#### <ins>NASA APOD COMMANDS</ins>
<ins>!nasa apod</ins>
 * Sends the NASA Astronomy Picture of the Day

<ins>!nasa apod DATE</ins>
 * Sends the NASA Astronomy Picture of the Day for the given date\
 * `Ex. !nasa apod 2020-1-1` <br>
 
#### <ins>NASA ROVER COMMANDS</ins>
<ins>!nasa rover</ins>
 * Send a random image from NASA's Mars Curiosity Rover

<ins>!nasa rover DATE</ins>
 * Send a random image from NASA's Mars Curiosity Rover for the given date
 * `Ex. !nasa rover 2020-1-1` <br>
 
#### <ins>NASA SEARCH COMMANDS</ins>
<ins>!nasa search</ins>
 * Sends a random image from NASA's image library

<ins>!nasa search SEARCHTERM</ins>
 * Sends an image from NASA's image library based on the search term
 * `Ex. !nasa search Uranus` <br>
 
#### <ins>ROBOT COMMANDS</ins>
<ins>!robot SET(optional) BACKGROUND(optional)</ins>
 * Sends a random robot image
 * `Ex. !robot set1 background1`

<ins>!robot TERM SET(optional) BACKGROUND(optional)</ins>
 * Sends a robot image based on the search term
 * `Ex. !robot My name is Alex! set4 background2`

<ins>SET can either be set1, set2, set3, set4, or set5</ins> \
<ins>BACKGROUND can either be background1 or background2</ins> <br>
 
#### <ins>STOCK COMMANDS</ins>
<ins>!stock STOCKTICKER</ins>
 * Sends a stock chart based on the stock ticker
 * `Ex. !stock MSFT`

<ins>!stock search SEARCHTERM</ins>
 * Searches for stocks based on the search term
 * `Ex. !stock search Amazon`



## Installation
Our project requires Python 3 and multiple packages to run.

[Install Python here.](https://www.python.org/downloads/)

Install packages.

```sh
pip install -r Requirements.txt
```



## Usage
To run the project through Command Prompt you have to CD into the folder and then run DiscordBot.py.

```sh
cd C:\Users\Alex\Downloads\Houhou-Discord-Bot-main
```

```sh
python DiscordBot.py
```



## Authors
Alex Mello - [Twitter](https://twitter.com/Alex_E_Mello), [GitHub](https://github.com/Alex-E-Mello)



## License
MIT



[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [link]: <https://discord.gg/JYxbQKkB>
   
   [Alpha Vantage]: <https://www.alphavantage.co/documentation/>
   [icanhazdadjoke]: <https://icanhazdadjoke.com/api>
   [NASA APOD]: <https://api.nasa.gov/>
   [NASA Image and Video Library]: <https://images.nasa.gov/docs/images.nasa.gov_api_docs.pdf>
   [NASA Mars Rover Photos]: <https://github.com/chrisccerami/mars-photo-api>
   [OMBd]: <http://www.omdbapi.com/>
   [RoboHash]: <https://github.com/e1ven/Robohash>
