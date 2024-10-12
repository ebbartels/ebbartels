# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# + [code] deletable=false editable=false
import otter
# nb_name should be the name of your notebook without the .ipynb extension
nb_name = "p8"
py_filename = nb_name + ".py"
grader = otter.Notebook(nb_name + ".ipynb")

# + deletable=false editable=false
import p8_test

# +
# PLEASE FILL IN THE DETAILS
# Enter none if you don't have a project partner
# You will have to add your partner as a group member on Gradescope even after you fill this

# project: p8
# submitter: ebbartels
# partner: temartin6

# + [markdown] deletable=false editable=false
# # Project 8: Going to the Movies

# + [markdown] deletable=false editable=false
# ## Learning Objectives:
#
# In this project, you will demonstrate how to:
#
# * integrate relevant information from various sources (e.g. multiple csv files),
# * build appropriate data structures for organized and informative presentation (e.g. list of dictionaries),
# * practice good coding style
#
# Please go through [lab-p8](https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f22-projects/-/tree/main/lab-p8) before working on this project. The lab introduces some useful techniques related to this project.

# + [markdown] deletable=false editable=false
# ## Note on Academic Misconduct:
#
# **IMPORTANT**: p8 and p9 are two parts of the same data analysis. You **cannot** switch project partners between these two projects. That is if you partner up with someone for p8, you have to sustain that partnership until end of p9. Now may be a good time to review [our course policies](https://cs220.cs.wisc.edu/f22/syllabus.html).

# + [markdown] deletable=false editable=false
# ## Testing your code:
#
# Along with this notebook, you must have downloaded the file `p8_test.py`. If you are curious about how we test your code, you can explore this file, and specifically the value of the variable `expected_json`, to understand the expected answers to the questions.

# + [markdown] deletable=false editable=false
# ## Introduction:
#
# In this project and the next, we will be working on the [IMDb Movies Dataset](https://www.imdb.com/interfaces/). We will use Python to discover some cool facts about our favorite movies, cast, and directors.
#
# In this project, you will combine the data from the movie and mapping files into a more useful format.
# Start by downloading the following files: `p8_test.py`, `small_mapping.csv`, `small_movies.csv`, `mapping.csv`, and `movies.csv`.

# + [markdown] deletable=false editable=false
# ## The Data:
#
# Open `movies.csv` and `mapping.csv` in any spreadsheet viewer, and see what the data looks like.
# `movies.csv` has ~100,000 rows and `mapping.csv` has ~350,000 rows. These files store information about **every** movie on the IMDb dataset which was released in the US. These datasets are **very** large when compared to `small_movies.csv` and `small_mapping.csv` from [lab-p8](https://github.com/msyamkumar/cs220-f22-projects/tree/main/lab-p8), but the data is stored in the **same format**. For description of the datasets, please refer back to [lab-p8](https://github.com/msyamkumar/cs220-f22-projects/tree/main/lab-p8).
#
# Before we start working with these very large datasets, let us start with the much smaller datasets, `small_movies.csv` and `small_mapping.csv` from lab-p8. In the latter half of p8 and in p9, you will be working with `movies.csv` and `mapping.csv`. Since the files `movies.csv` and `mapping.csv` are large, some of the functions you write in p8 and p9 **may take a while to execute**. You do not have to panic if a single cell takes between 5 to 10 seconds to run. If any cell takes significantly longer, follow the recommendations below:
#
# - **Do not** calling **slow functions** multiple times within a loop.
# - **Do not** calling functions that **iterate over the entire dataset within a loop**; instead, call the function before the loop and store the result in a variable.
# - **Do not** compute quantities **inside a loop** if it can be computed outside the loop; for example, if you want to calculate the average of a list, you should use the loop to find the numerator and denominator but divide **once** after the loop ends instead of inside the loop.

# + [markdown] deletable=false editable=false
# ## Project Requirements:
#
# You **may not** hardcode indices in your code, unless the question explicitly . If you open your `.csv` files with Excel, manually count through the rows and use this number to loop through the dataset, this is also considered as hardcoding. We'll **manually deduct** points from your autograder score on Gradescope during code review.
#
# **Store** your final answer for each question in the **variable specified for each question**. This step is important because Otter grades your work by comparing the value of this variable against the correct answer.
#
# For some of the questions, we'll ask you to write (then use) a function to compute the answer. If you compute the answer **without** creating the function we ask you to write, we'll **manually deduct** points from your autograder score on Gradescope, even if the way you did it produced the correct answer.
#
# Required Functions:
# - `get_mapping`
# - `get_raw_movies`
# - `get_movies`
# - `find_specific_movies`
# - `bucketize_by_genre`
#
# In this project, you will also be required to define certain **data structures**. If you do not create these data structures exactly as specified, we'll **manually deduct** points from your autograder score on Gradescope, even if the way you did it produced the correct answer.
#
# Required Data Structures:
# - `small_movies`
# - `movies`
# - `genre_dict`
#
# You are only allowed to define these data structures **once** and we'll **manually deduct** points from your autograder score on Gradescope if you redefine the values of these variables.
#
# In this project (and the next), you will be asked to create **lists** of movies. For all such questions, **unless it is explicitly mentioned otherwise**, the movies should be in the **same order** as in the `movies.csv` (or `small_movies.csv`) file. Similarly, for each movie, the **list** of `genres`, `directors`, and `cast` members should always be in the **same order** as in the `movies.csv` (or `small_movies.csv`) file.
#
# Students are only allowed to use Python commands and concepts that have been taught in the course prior to the release of p8. Therefore, you should not use the pandas module.  We will **manually deduct** points from your autograder score on Gradescope otherwise.
#
# In addition, you are also **required** to follow the requirements below:
# - **Do not use the method `csv.DictReader` for p8**. Although the required output can be obtained using this method, one of the learning outcomes of this project is to demonstrate your ability to build dictionaries with your own code.  
# - Additional import statements beyond those that are stated in the directions are not allowed. For this project, we allow you to use `csv` and `copy` packages (that is, you can use the `import csv` and `import copy` statements in your submission). You should not use concepts / modules that are yet to be covered in this course; for example: you should not use modules like `pandas`. **We'll manually deduct points** accordingly, if you don't follow the provided directions.
#
# For more details on what will cause you to lose points during code review and specific requirements, please take a look at the [Grading rubric](https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f22-projects/-/blob/main/p8/rubric.md).
#

# + [markdown] deletable=false editable=false
# ## Questions and Functions:
#
# Let us start by importing all the modules we will need for this project.
#
#

# + tags=[]
# it is considered a good coding practice to place all import statements at the top of the notebook
# please place all your import statements in this cell if you need to import any more modules for this project
import csv
import copy


# + [markdown] deletable=false editable=false
# ### Function 1: `get_mapping(path)`
#
# We require you to complete the below function to answer the next several questions (this is a **requirement**, and you will **lose points** if you do not implement this function). You may copy/paste code from your lab-p8 notebook to finish this function.
# -

def process_csv(filename):
    example_file = open(filename, encoding="utf-8")
    example_reader = csv.reader(example_file)
    example_data = list(example_reader)
    example_file.close()
    return example_data


# + tags=[]
def get_mapping(path):
    """
    get_mapping(path) converts a mapping csv in 'path' 
    into a dict with keys as IDs and values as names
    """
    example_data = process_csv(path)
    mapping_dict = {}
    for row in example_data:
        mapping_dict[row[0]] = row[1]
    return mapping_dict
        
    pass # replace with your code
#     TODO: process path
#     TODO: create a dictionary  
#     TODO: iterate through each row of processed path
#     TODO: map value in first column (ID) to value in second column (name/title)


# + [markdown] deletable=false editable=false
# **Question 1:** What is returned by `get_mapping("small_mapping.csv")`?
#
# Your output **must** be a **dictionary** which maps the *IDs* in `small_mapping.csv` to *names*.

# + tags=[]
# compute and store the answer in the variable 'small_mapping', then display it
small_mapping = get_mapping('small_mapping.csv')
small_mapping

# + deletable=false editable=false
grader.check("q1")

# + [markdown] deletable=false editable=false
# **Question 2:** What is the **value** associated with the **key** *nm2110418*?
#
# Your output **must** be a **string**.

# + tags=[]
# access and store the answer in the variable 'nm2110418_value', then display it
nm2110418_value = small_mapping['nm2110418']
nm2110418_value

# + deletable=false editable=false
grader.check("q2")

# + [markdown] deletable=false editable=false
# **Question 3:** What are the **values** associated with **keys** that **begin** with *nm*?
#
# Your output **must** be a **list** of **strings**.

# + tags=[]
# compute and store the answer in the variable 'nm_values', then display it
nm_values = []
for key in small_mapping:
    if key.startswith('nm'):
        nm_values.append(small_mapping[key])
nm_values

# + deletable=false editable=false
grader.check("q3")

# + [markdown] deletable=false editable=false
# **Question 4:** Find the **keys** of the people (keys **beginning** with *nm*) whose **last name** is *Spencer*.
#
# Your output **must** be a **list** of **string(s)**.
#
# **Requirements:** Your **code** must be robust and satisfy all the requirements, even if you were to run this on a larger dataset (such as `mapping.csv`). In particular:
# 1. You will **lose points** if your code would find people whose **first** name or **middle** name is *Spencer* (e.g. *Spencer Garrett* or *Charlie Spencer Clark*).
# 2. You will **lose points** if your code would find people whose **last** name contains *Spencer* as a **substring** (e.g. *Tara Spencer-Nairn*). The name should be **exactly** *Spencer*. 
# 3. You will **lose points** if your code would find any **movie titles** (e.g. *Meeting Spencer*).

# + tags=[]
# compute and store the answer in the variable 'nm_spencer', then display it
nm_spencer =[]
for key in small_mapping:
    name = small_mapping[key].split(' ')
    if name[1] == 'Spencer':
        if key.startswith('nm'):
            nm_spencer.append(key)

nm_spencer

# + deletable=false editable=false
grader.check("q4")


# + [markdown] deletable=false editable=false
# #### Now, let's move on to reading the movie files!

# + [markdown] deletable=false editable=false
# ### Function 2: `get_raw_movies(path)`
#
# We require you to complete the below function to answer the next several questions (this is a **requirement**, and you will **lose points** if you do not implement this function).
#
# This function **must** return a **list** of **dictionaries**, where each **dictionary** is of the following format:
#
# ```python
#    {
#         'title': <title-id>,
#         'year': <the year as an integer>,
#         'duration': <the duration as an integer>,
#         'genres': [<genre1>, <genre2>, ...],
#         'rating': <the rating as a float>,
#         'directors': [<director-id1>, <director-id2>, ...],
#         'cast': [<actor-id1>, <actor-id2>, ....]
#     }
# ```
#
# Here is an example:
#
# ```python
#     {
#         'title': 'tt0033313',
#         'year': 1941,
#         'duration': 59,
#         'genres': ['Western'],
#         'rating': 5.2,
#         'directors': ['nm0496505'],
#         'cast': ['nm0193318', 'nm0254381', 'nm0279961', 'nm0910294', 'nm0852305']
#     }
# ```
#
# You may copy/paste code from your lab-p8 notebook to finish this function.

# + tags=[]
def get_raw_movies(path):
    """
    get_raw_movies(path) converts a movies csv in 'path' 
    into a list of dicts with column names as keys and
    the corresponding type converted values as the values
    """
    csv_data = process_csv(path)
    csv_header = csv_data[0]
    csv_rows = csv_data[1:]
    num_rows = len(csv_rows)
    raw_movies_list = [] 
    for i in range(num_rows):

        new_movie = {} 
        new_movie["title"] = csv_rows[i][csv_header.index('title')]
        new_movie["year"] = int(csv_rows[i][csv_header.index('year')])
        new_movie["genres"] = csv_rows[i][csv_header.index('genres')].split(', ')
        new_movie["duration"] = int(csv_rows[i][csv_header.index('duration')])
        new_movie["rating"] = float(csv_rows[i][csv_header.index('rating')])
        new_movie["directors"] = csv_rows[i][csv_header.index('directors')].split(', ')
        new_movie["cast"] = csv_rows[i][csv_header.index('cast')].split(', ')
        raw_movies_list.append(new_movie)


    return raw_movies_list
    pass # replace with your code

# + [markdown] deletable=false editable=false
# **Question 5:** What is returned by `get_raw_movies("small_movies.csv")`?
#
# Your output **must** be a **list** of **dictionaries** where each dictionary contains information about a movie.

# + tags=[]
# compute and store the answer in the variable 'raw_small_movies', then display it
raw_small_movies = get_raw_movies('small_movies.csv')
raw_small_movies

# + deletable=false editable=false
grader.check("q5")

# + [markdown] deletable=false editable=false
# If your answer looks correct, but does not pass `grader.check`, make sure that the **datatypes** are all correct. Also make sure that the **directors** and **cast**  are in the **same order** as in `small_movies.csv`.

# + [markdown] deletable=false editable=false
# **Question 6:** How **many** cast members does the **first** movie have?
#
# Your output **must** be an **int**.

# + tags=[]
# compute and store the answer in the variable 'num_cast_first_movie', then display it
num_cast_first_movie = len(raw_small_movies[0]['cast'])
num_cast_first_movie

# + deletable=false editable=false
grader.check("q6")

# + [markdown] deletable=false editable=false
# **Question 7:** What is the *ID* of the **first** cast member listed for the **first** movie of the dataset?
#
# Your output **must** be a **string**.

# + tags=[]
# compute and store the answer in the variable 'first_actor_id_first_movie', then display it
first_actor_id_first_movie = raw_small_movies[0]['cast'][0]
first_actor_id_first_movie

# + deletable=false editable=false
grader.check("q7")


# + [markdown] deletable=false editable=false
# ### Function 3: `get_movies(movies_path, mapping_path)`
#
# We require you to complete the below function to answer the next several questions (this is a **requirement**, and you will **lose points** if you do not implement this function).
#
#
# This function **must** return a **list** of **dictionaries**, where each **dictionary** is of the following format:
#
# ```python
#    {
#         'title': "the movie name",
#         'year': <the year as an integer>,
#         'duration': <the duration as an integer>,
#         'genres': [<genre1>, <genre2>, ...],
#         'rating': <the rating as a float>,
#         'directors': ["director-name1", "director-name2", ...],
#         'cast': ["actor-name1", "actor-name2", ....]
#     }
# ```
#
# Here is an example:
#
# ```python
#     {
#         'title': 'Across the Sierras',
#         'year': 1941,
#         'duration': 59,
#         'genres': ['Western'],
#         'rating': 5.2,
#         'directors': ['D. Ross Lederman'],
#         'cast': ['Dick Curtis', 'Bill Elliott', 'Richard Fiske', 'Luana Walters', 'Dub Taylor']
#     }
# ```
#
# You may copy/paste code from your lab-p8 notebook to finish this function.

# + tags=[]
def get_movies(movies_path, mapping_path):
    """
    get_movies(movies_path, mapping_path) converts a movies csv in 'movies_path' 
    into a list of dicts with column names as keys and the corresponding 
    type converted values as the values; then uses the mapping csv in 'mapping_path'
    to replace the IDs of the titles, cast, and directors into actual names
    """
    movie_list = get_raw_movies(movies_path)
    mapping_list = get_mapping(mapping_path)
    
    
    for movies in movie_list:
        cast_list = []
        directors_list = []

        for cast in movies['cast']:
            cast_id = cast
            cast_name = mapping_list[cast_id]
            cast_list.append(cast_name)
        for directors in movies['directors']:
            directors_id = directors
            directors_name = mapping_list[directors_id]
            directors_list.append(directors_name)
        title_id = movies['title']
        title_name = mapping_list[title_id]
            
        movies['cast'] = cast_list
        movies['directors'] = directors_list
        movies['title'] = title_name
        
    return movie_list
        
    pass # replace this code
    # you are allowed to call get_mapping and get_raw_movies
    # on movies_path and mapping_path

# + [markdown] deletable=false editable=false
# **Question 8:** What is returned by `get_movies("small_movies.csv", "small_mapping.csv")`?
#
# Your output **must** be a **list** of **dictionaries** where each dictionary contains information about a movie.

# + tags=[]
# compute and store the answer in the variable 'small_movies_data', then display it
small_movies_data = get_movies('small_movies.csv','small_mapping.csv')
small_movies_data

# + deletable=false editable=false
grader.check("q8")

# + [markdown] deletable=false editable=false
# **Question 9:** What is `title` of the **second** movie in `small_movies_data`?
#
# Your output **must** be a **string**.

# + tags=[]
# compute and store the answer in the variable 'second_movie_title_small_movies', then display it
second_movie_title_small_movies = small_movies_data[1]['title']
second_movie_title_small_movies

# + deletable=false editable=false
grader.check("q9")

# + [markdown] deletable=false editable=false
# **Question 10:** Who are the `cast` members of the **second** movie in `small_movies_data`?
#
# Your output **must** be a **list** of **string(s)**.

# + tags=[]
# compute and store the answer in the variable 'second_movie_cast_small_movies', then display it
second_movie_cast_small_movies = small_movies_data[1]['cast']
second_movie_cast_small_movies

# + deletable=false editable=false
grader.check("q10")

# + [markdown] deletable=false editable=false
# **Question 11:** Who are the `directors` of the **last** movie in `small_movies_data`?
#
# Your output **must** be a **list** of **string(s)**.

# + tags=[]
# compute and store the answer in the variable 'last_movie_directors_small_movies', then display it
last_movie_directors_small_movies =  small_movies_data[-1]['directors']
last_movie_directors_small_movies

# + deletable=false editable=false
grader.check("q11")

# + [markdown] deletable=false editable=false
# #### Now that you’ve made it this far, your functions must be working pretty well with small datasets. Next, let's try a much bigger dataset!
#
# Run the following code to open the full dataset:
# -

movies = get_movies("movies.csv", "mapping.csv")
len(movies)

# + [markdown] deletable=false editable=false
# As the files are very large, this cell is expected to take around ten seconds to run. If it takes much longer (say, around a minute), then you will **need** to **optimize** your `get_movies` function so it runs faster.
#
# **Warning**: You are **not** allowed to call `get_movies` more than once on the full dataset (`movies.csv` and `mapping.csv`) in your notebook. Instead, reuse the `movies` variable, which is more efficient. You will **lose points** during manual review if you call `get_movies` again on these files.
#
# **Warning:** Do **not** display the value of the variable `movies` **anywhere** in your notebook. It will take up a **lot** of space, and your **Gradescope code will not be displayed** for grading. So, you will receive **zero points** for p8. Instead you should verify `movies` has the correct value by looking at a small *slice* of the **list** as in the question below. 

# + [markdown] deletable=false editable=false
# **Question 12:** What are the movies in `movies[20200:20220]`?
#
# Your answer should be a *list* of *dictionaries* that follows the format below:
#
# ```python
# [{'title': 'Aliens in the Attic',
#   'year': 2009,
#   'duration': 86,
#   'genres': ['Adventure', 'Comedy', 'Family'],
#   'rating': 5.4,
#   'directors': ['John Schultz'],
#   'cast': ['Ashley Tisdale',
#    'Robert Hoffman',
#    'Carter Jenkins',
#    'Austin Butler']},
#  {'title': 'Dark Buenos Aires',
#   'year': 2010,
#   'duration': 90,
#   'genres': ['Thriller'],
#   'rating': 4.8,
#   'directors': ['Ramon Térmens'],
#   'cast': ['Francesc Garrido',
#    'Daniel Faraldo',
#    'Natasha Yarovenko',
#    'Julieta Díaz']},
#  ...
# ]
# ```

# + tags=[]
# compute and store the answer in the variable 'movies_20200_20220', then display it
movies_20200_20220 = movies[20200:20220]
movies_20200_20220

# + deletable=false editable=false
grader.check("q12")

# + [markdown] deletable=false editable=false
# **Question 13:** What is the **number** of movies released in the `year` *2018*?
#
# Your outuput must be an **int**.

# + tags=[]
# compute and store the answer in the variable 'num_movies_2018', then display it
num_movies_2018 =0
for movie in movies:
    if movie['year'] == 2018:
        num_movies_2018+=1


num_movies_2018

# + deletable=false editable=false
grader.check("q13")


# + [markdown] deletable=false editable=false
# ### Function 4: `find_specific_movies(movies, keyword)`
#
# Now that we have created this data structure `movies`, we can start doing some fun things with the data!
# We will continue working on this data structure for the next project (p9) as well.
#
# Let us now use this data structure `movies` to create a **search bar** like the one in Netflix!
# **Do not change the below function in any way**.
# This function takes in a keyword like a substring of a title, a genre, or the name of a person, and returns a list of relevant movies with that title, genre, or cast member/director.
#
# **Warning:** As `movies` is very large, the function `find_specific_movies` may take five to ten seconds to run. This is normal and you should not panic if it takes a while to run.

# + deletable=false editable=false
# DO NOT EDIT OR REDEFINE THIS FUNCTION
def find_specific_movies(movies, keyword):
    """
    find_specific_movies(movies, keyword) takes a list of movie dictionaries 
    and a keyword; it returns a list of movies that contain the keyword
    in either its title, genre, cast or directors.
    """
    idx = 0
    while idx < len(movies):
        movie = movies[idx]
        # note: \ enables you split a long line of code into two lines
        if (keyword not in movie['title']) and (keyword not in movie["genres"]) \
        and (keyword not in movie["directors"]) and (keyword not in movie["cast"]):
            movies.pop(idx)
        else:
            idx += 1
    return movies


# + [markdown] deletable=false editable=false
# **Important:** While it might look as if we are making it easy for you by providing `find_specific_movies`, there is a catch! There is a subtle flaw with the way the function is defined, that will cause you issues in the next two questions. If you can spot this flaw by just observing the definition of `find_specific_movies`, congratulations! Since you are **not** allowed to modify the function definition, you will have to be a little clever with your function arguments to sidestep the flaw with the function definition.
#
# If you don't see anything wrong with the function just yet, don't worry about it. Solve q14 and q15 as you normally would, and see if you notice anything suspicious about your answers.

# + [markdown] deletable=false editable=false
# **Question 14:** List all the movies that *Katharine Hepburn* acted in.
#
# Your answer **must** be a **list** of **dictionaries**.
#
# You **must** answer this question by calling `find_specific_movies` with the keyword `"Katharine Hepburn"`.
#
# The `find_specific_movies` function is expected to take around 5 seconds to run, so do not panic if it takes so long to run.

# + tags=[]
# compute and store the answer in the variable 'hepburn_films', then display it
hepburn_films = find_specific_movies(copy.deepcopy(movies),'Katharine Hepburn')
hepburn_films

# + deletable=false editable=false
grader.check("q14")

# + [markdown] deletable=false editable=false
# **Question 15:** List all the movies that contain the string *Wisconsin* in their `title`.
#
# Your answer **must** be a **list** of **dictionaries**.
#
# You **must** answer this question by calling `find_specific_movies` with the keyword `"Wisconsin"`.
#
# **Important Hint:**  If you did not notice the flaw with the definition of `find_specific_movies` before, you are likely to have run into an issue with this quetsion. It is likely that you will see that your output for this question is an empty list. To see why this happened, find the value of `len(movies)` and see if it is equal to the value you found earlier.
#
# Remember that you are **not** allowed to modify the definition of `find_specific_movies`. You will need to cleverly pass arguments to `find_specific_movies` (in both q14 and q15) to ensure that `movies` does not get modified by the function calls. Take a look at the [lecture slides](https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-lecture-material/-/tree/main/f22/meena_lec_notes/lec-21) from October 26 for more hints. You will have to Restart and Run all your cells to see the correct output after you fix your answer for q14 (and q15).

# + tags=[]
# compute and store the answer in the variable 'wisconsin_movies', then display it
wisconsin_movies = find_specific_movies(copy.copy(movies),'Wisconsin')
wisconsin_movies

# + deletable=false editable=false
grader.check("q15")


# + [markdown] deletable=false editable=false
# ### Function 5: `bucketize_by_genre(movies)`
#
# We require you to complete the below function to answer the next several questions (this is a **requirement**, and you will **lose points** if you do not implement this function).

# + tags=[]
def bucketize_by_genre(movies):
    """bucketize_by_genre(movies) takes a list of movie dictionaries;
    it returns a dict in which each genre is a key and
    the value is a list of all movies that contain that genre"""
    genre_dict = {}
    for movie in movies:
        for genre in movie['genres']:
            if genre not in genre_dict:
                genre_dict[genre] = [movie]
            else:
                genre_dict[genre].append(movie)
    return genre_dict
    pass # replace with your code
    # TODO: initialize a dictionary
    # TODO: loop through all movies
    # TODO: loop through all genres in this movie
    # TODO: if this genre is not a key in our dictionary, set the value associated with this genre to an empty list
    # TODO: if we already have this genre in our dictionary, add the movie to the list associated with this genre
    # TODO: return the dictionary


# + tags=[]
# call the function bucketize_by_genre on 'movies' and store it in the variable 'genre_dict'
# do NOT display the output directly

genre_dict = bucketize_by_genre(movies)


# + [markdown] deletable=false editable=false
# **Warning:** You are **not** allowed to call `bucketize_by_genre` more than once on the full list of movies (`movies`) in your notebook. You will **lose points** during manual review if you call `bucketize_by_genre` again on `movies`.

# + [markdown] deletable=false editable=false
# **Question 16:** How many **unique** movie `genres` are present in the dataset?

# + tags=[]
# compute and store the answer in the variable 'num_genres', then display it
num_genres = len(genre_dict)
num_genres

# + deletable=false editable=false
grader.check("q16")

# + [markdown] deletable=false editable=false
# **Question 17:** How many *Music* movies (i.e. movies with *Music* as one of their `genres`) do we have in the dataset released **after** the `year` *2019*?
#
# Your output **must** be an **int**. You **must** use the `genre_dict` data structure to answer this question.

# + tags=[]
# compute and store the answer in the variable 'music_after_2019', then display it
music_after_2019 = 0
for movie in genre_dict['Music']:
    if movie['year'] > 2019:
        music_after_2019 +=1
        
music_after_2019

# + deletable=false editable=false
grader.check("q17")

# + [markdown] deletable=false editable=false
# **Question 18:** List the `title` of all *Horror* movies (i.e. movies with *Horror* as one of their `genres`) with `rating` **larger** than *9.0* in the dataset.
#
# Your output **must** be a **list** of **strings**. You **must** use the `genre_dict` data structure to answer this question.

# + tags=[]
# compute and store the answer in the variable 'horror_movies_above_9', then display it
horror_movies_above_9 = []
for movie in genre_dict['Horror']:
    if movie['rating'] > 9.0:
        horror_movies_above_9.append(movie['title'])
horror_movies_above_9

# + deletable=false editable=false
grader.check("q18")

# + [markdown] deletable=false editable=false
# **Question 19:** Which movie `genre` does *Jennifer Aniston* play the most?
#
# There is a **unique** `genre` that *Jennifer Aniston* has played the most. You do **not** have to worry about breaking ties.
#
# **Hint:** You can combine the *two* functions above to bucketize the movies that *Jennifer Aniston* has acted in by their `genres`. Then, you can loop through each genre to find the one with the most number of movies in it.

# + tags=[]
# compute and store the answer in the variable 'jen_aniston_genre, then display it
jen_aniston_genre = None
jen_aniston_movies = find_specific_movies(copy.copy(movies),'Jennifer Aniston')
jen_aniston_movies_genre = bucketize_by_genre(jen_aniston_movies)
for genre in jen_aniston_movies_genre:
    if jen_aniston_genre == None:
        jen_aniston_genre = genre
    elif len(jen_aniston_movies_genre[genre]) > len(jen_aniston_movies_genre[jen_aniston_genre]):
        jen_aniston_genre = genre
        
jen_aniston_genre

# + deletable=false editable=false
grader.check("q19")

# + [markdown] deletable=false editable=false
# **Question 20:** Who are the `directors` of the *Documentary* movies with the **highest** `rating` in the movies dataset?
#
# There are **multiple** *Documentary* movies in the dataset with the joint highest rating. You **must** output a **list** of **strings** containing the **names** of **all** the `directors` of **all** these movies.
#
# **Hint:** If you are unsure how to efficiently add the elements of one list to another, take a look at the [lecture slides](https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-lecture-material/-/tree/main/f22/meena_lec_notes/lec-14) from October 10.

# + tags=[]
# compute and store the answer in the variable 'max_docu_rating_directors', then display it
max_docu_rating_directors = []
max_rating = 0
for movie in genre_dict['Documentary']:
    if movie['rating'] > max_rating:
        max_rating = movie['rating']
for movie in genre_dict['Documentary']:
    if movie['rating'] == max_rating:
        for directors in movie['directors']:
            max_docu_rating_directors.append(directors)

max_docu_rating_directors


# + deletable=false editable=false
grader.check("q20")

# + [markdown] deletable=false editable=false
# ## Submission
# Make sure you have run all cells in your notebook in order before running the following cells, so that all images/graphs appear in the output.
# It is recommended that at this stage, you Restart and Run all Cells in your notebook.
# That will automatically save your work and generate a zip file for you to submit.
#
# **SUBMISSION INSTRUCTIONS**:
# 1. **Upload** the zipfile to Gradescope.
# 2. Check **Gradescope otter** results as soon as the auto-grader execution gets completed. Don't worry about the score showing up as -/100.0. You only need to check that the test cases passed.

# + [code] deletable=false editable=false
# running this cell will create a new save checkpoint for your notebook
from IPython.display import display, Javascript
display(Javascript('IPython.notebook.save_checkpoint();'))

# + [code] deletable=false editable=false
# !jupytext --to py p8.ipynb

# + [code] deletable=false editable=false
p8_test.check_file_size("p8.ipynb")
grader.export(pdf=False, run_tests=True, files=[py_filename])

# + [markdown] deletable=false editable=false
#  
