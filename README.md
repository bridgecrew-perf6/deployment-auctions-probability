# deployment-auctions-probability
The following repository contains the deployment into a google sheet file of the output of a machine learning model. 
The goal of this project is to successfully feed the Machine Learning algorithm a test set (real estate auctions), and write daily on google sheet the corresponding award probability.

The zip contains 8 Python scripts that implement the reading / writing of some data on a google sheet. These scripts contain numerous classes that interact with each other and the way they communicate are described in the 'main.py' file which is essentially the only file that must be run and which in a synthetic and descriptive way tells all the code of the others 8 scripts in very few lines.

Here is a small description of the main classes in order to facilitate its understanding and evaluation:
"Auction Repository" is a class whose task is to read from a simple Google Sheet some data about real estate auctions (they will be the test set to be fed to a model), 
and then give it as input to another class. This will return other information which the 'Auction Repository' will then rewrite on the Google Sheet. It is therefore the class that deals with communicating with the google sheet, through the use of google API, by logging in and reading / writing operations.
"Auctions DataFrame" receives auction data from the Auction Repository, and has the task of applying some transformations to the data, carrying out operations similar to a Pandas dataframe, but customized to the auction dataframe.
"Marketability Calculator" is a class having in its init an object 'sav' which contains the ready model which outputs the probabilities of award (so there is no modeling operation, but the model is already finished and given as input). In fact, the 'evaluate' method initially delegates the preparation of the test set to Auctions DataFrame and then calculates the award probabilities. Finally, it inserts the Probability as a new column in the Auction DataFrame, which will then be written daily, by Auction Repository, on the Google Sheet, with the help of Heroku Scheduler.
