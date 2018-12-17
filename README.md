# Python-DB-Aggrigator
Crawls sales tables in a DB and computes the Yoy sales of a given client. Yoy sales are then correlated with usage data to gauge effectivity of a platform. code result of a one day hackathon.

**aggrigateSales.py**
For a specified table aggrigateSales produces a YoY sales figure, this YoY sales metric can be used for graphical data analysis in plotAggrigates.py.

**returnCSV.py**
A simple function to crawl through a DB and retrieve table names that fit a specified format, these tables can then be used as an input of the Yoy function of aggrigateSales.py.

**plotAggrigates.py**
Plots the resulting Yoy data from returnCSV.py and the usage data to provide a picture of effectivity. Several functions can be used. 
