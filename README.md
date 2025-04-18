# ET-206-Final-Project

#Steps to Run Our Code
Step 1:
- In the Harvard folder, run Harvard.py once 
    - Creates ‘harvard.json’ and ‘harvard_directors.json’
Step 2:
- In the Met Museum folder, run met.py once
    - Creates ‘met.json’
Step 3:
- In the Met Museum folder, run metwiki.py once
    - Creates ‘met_directors.json’
Step 4:
- In the Database folder, run database.py five times
    - database.py adds 25 rows of data per run during the first 4 runs, then adds the remainder of the data during the 5th and final run, per suggestions from the teaching team. This prevents the need to run the file 30+ times to gather the 800+ rows of data from the Harvard Art Museums.
    - Creates ‘Art.db’ and uses ‘harvard.json’, ‘harvard_directors.json’, ‘met.json’, and ‘met_directors.json’ to insert data into ‘Art.db’
Step 5:
- In the Database folder, run met_graphics.py one time
    - Uses ‘Art.db’ to create and save a pie chart (‘met_pie_chart.png’) and a bar chart (‘comparison_bar_chart.png’). Creates and writes calculations to ‘calculations.txt’
Step 6:
- In the Database folder, run harvard_graphics.py one time
    - Uses ‘Art.db’ to create and save a pie chart (‘harvard_art_by_gender.png’) and a line graph (‘harvard_art_by_accession_year.png’). Appends calculations to ‘calculations.txt’