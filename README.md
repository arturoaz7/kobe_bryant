# Kaggle Competition: Kobe Bryant Shot Selection

In this repo you'll find the following files related to my late participation on the competition.

- Media folder which contains all the images and gifs that are in the markdown cells in both notebooks.
- Submissions folder contains 3 csv files containing each shot_id to be predicted along with the probablity of the shot_made_flag belonging to the class 1 (the shot going in).
- kobe_shots.csv is a csv file containing the data provided by the competition.
- kobe_bryant_shot_selection_(pre-processing).ipynb is a notebook containing the first part of our project which consists on the analysis and cleaning process.
By the end of the notebook a python script is generated.
- kb_load_process.py is a python script generated at the end of the first notebook, this script loads the dataset and performs all the transformations that resulted from the 
exploration and data cleaning process.
-kobe_bryant_shot_selection(ML).ipynb is the final notebook for the project in which we load and process the data by simply exectuing the python script mentioned above and 
start the process of Machine Learning by validating estimators, selecting features and optimizing hyper-parameters. At the of the notebook we attached snips with the results obtained
after submitting our 3 csv files.
