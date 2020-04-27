#Desing choices#
1. Speed first
2. If you can - non blocking

Quart is used as is similar to Flask and add async to routes.
SQLAlchemy is use as has flexibility to add if necessary external database.

Coded on Win 10 with Python 3.8.1 64 bit

# Data

Expected format for data is JSON. Source template in Awasu:

*Awasu\JSON.template* - use this to get correct data. Group articles by channel. Another settings as you wish.
*config.py* - example config

# Code structure #

## Templates ##

All template inherit from base.html. Used template language - Jinja2:
https://jinja.palletsprojects.com/en/2.10.x/templates/

Add here to common Jquery libraries, extension etc.

Inside templates are:

###Main menu

Application is splitted by logic blocks: articles, channels, analytics, export
*articles* - browse latest articles
*channel* - browse articles by channels and from channels grouped in categories
*analytics* - metadata - not implemented. Proposed - Spacy.

### macros ###

Folder for snippet inside templates fx. generate buttons.

*browsing.html*

Elements connected with browsing experience like pagination

*menus.html*

All types menus and commons for all views like main menu

*tables.html*

Mainly for presentation articles in responsive tables.


### views ###
Each logic block has separate Blueprint. One catalog for one Blueprint. Using extend is override default base template. Used conventions in variables:

*submenu* - menu specific to category

*content* - category data

#Core

Heart of app with sections:
## data
*manipulation* - general data manipulators like change names to PEP8, join dicts, more Python default structure oriented

*presentation* - visualising data what is out of using in template fx. colored data output

## database
*base* - preparing data, first filling, tables declaration

*operation* - get filtered result from database

*result_manipulation* - add extra formatting outside SQL Alchemy fx. prepare for view and interact with templates

##settings
*config* - settings for app

*initialcheck* - first run checks to be sure that base configuration and running dependency are OK

*slices* - declarations of slices and variables to avoid magic numbers

##views
Group all related to views inside browser.

###articles
Presentation data as articles. Default is show latest. Number is defined in config LATEST_ARTICLE_NUMBER

###categories
Browse as categories and directory tree folders

###channels
Get articles inside channel and basic information about channel like succeful update, number of articles in channel

###search
Search engine related stuff.

###selected
Prepare data for export and use outside application.

###settings
Used to get missed configuration, first run etc. Create new setup, backup etc.