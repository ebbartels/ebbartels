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
nb_name = "p12"
py_filename = nb_name + ".py"
grader = otter.Notebook(nb_name + ".ipynb")

# + deletable=false editable=false
import p12_test

# +
# PLEASE FILL IN THE DETAILS
# Enter none if you don't have a project partner
# You will have to add your partner as a group member on Gradescope even after you fill this

# project: p12
# submitter: ebbartels
# partner: temartin6

# + [markdown] deletable=false editable=false
# # Project 12: World University Rankings

# + [markdown] deletable=false editable=false
# ## Learning Objectives:
#
# In this project, you will demonstrate your ability to
#
# * read and write files,
# * create and use `Pandas DataFrames`,
# * use `BeautifulSoup` to parse web pages.
#
# Please go through [lab-p12](https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f22-projects/-/tree/main/lab-p12) before working on this project. The lab introduces some useful techniques related to this project.

# + [markdown] deletable=false editable=false
# ## Note on Academic Misconduct:
#
# **IMPORTANT**: p12 and p13 are two parts of the same data analysis. You **cannot** switch project partners between these two projects. That is if you partner up with someone for p12, you have to sustain that partnership until the end of p13. Now may be a good time to review [our course policies](https://cs220.cs.wisc.edu/f22/syllabus.html).

# + [markdown] deletable=false editable=false
# ## Testing your code:
#
# Along with this notebook, you must have downloaded the file `p12_test.py`. If you are curious about how we test your code, you can explore this file, and specifically the value of the variable `expected_json`, to understand the expected answers to the questions.
#
# For answers involving DataFrames, `p12_test.py` compares your tables to those in `p12_expected.html`, so take a moment to open that file on a web browser (from Finder/Explorer).
#
# `p12_test.py` doesn't care if you have extra rows or columns, and it doesn't care about the order of the rows or columns. However, you must have the correct values at each index/column location shown in `p12_expected.html`.

# + [markdown] deletable=false editable=false
# ## Introduction:
#
# For this project, you're going to analyze World University Rankings!
#
# Specifically, you're going to use Pandas to analyze various statistics of the top ranked universities across the world, over the last three years.
#
# Start by downloading the files `p12_test.py`, and `p12_expected.html`.
#
# **Important Warning:** Do **not** download any of the other files manually (you **must** write Python code to download these automatically, as in lab-p12). When we run the autograder, the other files such as `rankings.json`, `2019-2020.html`, `2020-2021.html`, `2021-2022.html` will **not** be in the directory. So, unless your `p12.ipynb` downloads these files, you will get a **zero score** on the project. More details can be found in the **Setup** section of the project.

# + [markdown] deletable=false editable=false
# ## Data:
#
# For this project, we will be analyzing statistics about world university rankings adapted from [here](https://cwur.org/). These are the specific webpages that we extracted the data from:
#
# * https://cwur.org/2019-20.php
# * https://cwur.org/2020-21.php
# * https://cwur.org/2021-22.php
#
# Later in the project, you will be scraping these webpages and extracting the data yourself. Since we don't want all of you bombarding these webpages with requests, we have made snapshots of these webpages, and hosted them on GitHub. You can find the snapshots here:
#
# * https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f22-projects/-/raw/main/p12/2019-2020.html
# * https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f22-projects/-/raw/main/p12/2020-2021.html
# * https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f22-projects/-/raw/main/p12/2021-2022.html
#
# You will be extracting the data from these three html pages and analyzing them. However, to make the start of the project a little easier, we have already parsed the files for you! We have gathered the data from these html files, and collected them in a single json file, which can be found here:
#
# * https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f22-projects/-/raw/main/p12/rankings.json
#
# You will work with this json file for most of this project. At the end of this project, you will generate an identical json file by parsing the html files yourself.

# + [markdown] deletable=false editable=false
# ## Project Requirements:
#
# You **may not** hardcode indices in your code. You **may not** manually download **any** files for this project, unless you are **explicitly** told to do so. For all other files, you **must** use the `download` function to download the files.
#
# **Store** your final answer for each question in the **variable specified for each question**. This step is important because Otter grades your work by comparing the value of this variable against the correct answer.
#
# For some of the questions, we'll ask you to write (then use) a function to compute the answer. If you compute the answer **without** creating the function we ask you to write, we'll **manually deduct** points from your autograder score on Gradescope, even if the way you did it produced the correct answer.
#
# Required Functions:
# - `download`
# - `parse_html`
#
# In this project, you will also be required to define certain **data structures**. If you do not create these data structures exactly as specified, we'll **manually deduct** points from your autograder score on Gradescope, even if the way you did it produced the correct answer.
#
# Required Data Structures:
# - `institutions_df`
#
# In addition, you are also **required** to follow the requirements below:
# * **Avoid using loops to iterate over pandas dataframes and instead use boolean indexing.**
# * Do **not** use `loc` to look up data in **DataFrames** or **Series**. You are **allowed** to use `iloc`.
# * Do **not** use **absolute** paths such as `C://ms//cs220//p12`. You may **only** use **relative paths**.
# * Do **not** use meaningless names for variables or functions (e.g. `uuu = "my name"`).
# * Do **not** leave irrelevant output or test code that we didn't ask for.
# * Do **not** write the exact same code in multiple places. Instead, wrap this code into a function and call that function whenever the code should be used.
# * Do **not** call unnecessary functions.
# * **Avoid** calling **slow** functions multiple times within a loop.
# * **Avoid** inappropriate use of data structures. For instance: do **not** use a `for` loop to search for a corresponding value in a dictionary with a given key; instead use `dictname[key]` directly.
# * Do **not** define multiple functions with the same name or define multiple versions of one function with different names. Just keep the best version.
#
# For more details on what will cause you to lose points during code review and specific requirements, please take a look at the [Grading rubric](https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f22-projects/-/blob/main/p12/rubric.md).

# + [markdown] deletable=false editable=false
# # Questions and Functions:
#
# Let us start by importing all the modules we will need for this project.

# + tags=[]
# it is considered a good coding practice to place all import statements at the top of the notebook
# please place all your import statements in this cell if you need to import any more modules for this project
import requests
import os
import json
import pandas as pd
from bs4 import BeautifulSoup


# + [markdown] deletable=false editable=false
# ### Function 1: `download(page, filename)`
#
# You **must** now copy/paste the `download` function from lab-p12. This function **must** extract the data in the webpage `page` and store it in `filename`. If the `filename` already exists, it **must not** download the file again.

# + tags=[]
# copy/paste the 'download' function from lab-p12
def download(filename, url):
    if os.path.exists(filename):
        return str(filename)+ ' already exists!'
    r = requests.get(url)
    r.raise_for_status
    url_text = r.text
    f = open(filename, 'w',encoding = 'utf-8')
    f.write(url_text)
    f.close()
    return (str(filename) + " created!")


# + [markdown] deletable=false editable=false
# Now, use `download` to pull the data from here (**do not manually download**): https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f22-projects/-/raw/main/p12/rankings.json and store it in the file `rankings.json`. Once you have created the file, create a Dataframe `rankings` from this file.
#
# **Warning:** Make sure your `download` function meets the specifications mentioned in lab-p12 and does **not** download the file if it already exists. The TAs will **manually deduct** points otherwise. Make sure you use the `download` function to pull the data instead of manually downloading the files. Otherwise you will get a zero.

# + tags=[]
# use the 'download' function to download the data from the webpage
# 'https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f22-projects/-/raw/main/p12/rankings.json'
# to the file 'rankings.json'
download('rankings.json','https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f22-projects/-/raw/main/p12/rankings.json')

# + tags=[]
# open 'rankings.json' with pd.read_json('rankings.json') and store in the variable 'rankings'
f = open('rankings.json')
rankings = pd.read_json('rankings.json')
f.close()

# + [markdown] deletable=false editable=false
# **Question 1:** How **many** countries do we have in our dataset?
#
# Your output **must** be an **int** representing the number of *unique* countries in the dataset.

# + tags=[]
# compute and store the answer in the variable 'num_countries', then display it
country_list = []
for country in rankings['Country']:
    country_list.append(country)
num_countries = len(set(country_list))
num_countries

# + deletable=false editable=false
grader.check("q1")

# + [markdown] deletable=false editable=false
# **Question 2:** Generate a `pandas` **DataFrame** containing **all** the statistics of the **highest-ranked** institution based on `World Rank` across all the years.
#
# Your output **must** be a pandas **DataFrame** with 3 rows and 10 columns. It **must** contain all the data for the institutions with `World Rank` of *1*. It **must** look like this:
# -

# <div><img src="attachment:highest_ranked.PNG" width="1000"/></div>

# + tags=[]
# compute and store the answer in the variable 'highest_ranked', then display it
b = rankings['World Rank'] == 1
highest_ranked = rankings[b]
highest_ranked

# + deletable=false editable=false
grader.check("q2")

# + [markdown] deletable=false editable=false
# **Question 3:** Generate a `pandas` **DataFrame** containing **all** the statistics of *University of Wisconsin–Madison*.
#
# Your output **must** be a pandas **DataFrame** with 3 rows and 10 columns. It **must** look like this:
# -

# <div><img src="attachment:uw_madison.PNG" width="1000"/></div>

# + tags=[]
# compute and store the answer in the variable 'uw_madison', then display it
b = rankings['Institution']=='University of Wisconsin–Madison'
uw_madison=rankings[b]
uw_madison

# + deletable=false editable=false
grader.check("q3")

# + [markdown] deletable=false editable=false
# **Question 4:** What is the `National Rank` of the *University of Wisconsin–Madison* in the `Year` *2021-2022*?
#
# Your output **must** be an **int**. You **must** use **Boolean indexing** on the variable `uw_madison` to answer this question.
#
# **Hint:** Use Boolean indexing on the DataFrame `uw_madison` to find the data for the year `2021-2022`. You may then extract the `National Rank` column from the subset DataFrame. Finally, use `iloc` to lookup the value in the DataFrame which contains only one row and one column.

# + tags=[]
# compute and store the answer in the variable 'uw_madison_nat_rank', then display it
b = uw_madison['Year'] == '2021-2022'
uwm_21_22 = uw_madison[b]
uw_madison_nat_rank = uwm_21_22['National Rank'].iloc[0]
uw_madison_nat_rank

# + deletable=false editable=false
grader.check("q4")

# + [markdown] deletable=false editable=false
# **Question 5:** What is the **average** `Score` of the *University of Wisconsin–Madison*?
#
# Your output **must** be a **float**. You **must** use the variable `uw_madison` to answer this question.
#
# **Hint:** You **must** extract the `Score` column of the **DataFrame** `uw_madison` as a **Series**. You can find the **average** of  all the scores in a **Series** with the `Series.mean` function.
# -

(uw_madison['Score']).mean()

# + tags=[]
# compute and store the answer in the variable 'uw_madison_avg_score', then display it
uw_madison_avg_score = uw_madison['Score'].mean()
uw_madison_avg_score

# + deletable=false editable=false
grader.check("q5")

# + [markdown] deletable=false editable=false
# **Question 6:** Generate a `pandas` **DataFrame** containing **all** the statistics of universities from the `Country` *Singapore* in the `Year` *2020-2021*.
#
# Your output **must** be a pandas **DataFrame** with 4 rows and 10 columns. It **must** look like this:
# -

# <div><img src="attachment:singapore_inst.PNG" width="1000"/></div>

# + [markdown] deletable=false editable=false
# **Hint:** When there are **multiple** conditions to filter a **DataFrame**, you can combine all the conditions with `&` as a logical operator between them. For example, you can extract the data for all the institutions with `Quality of Education Rank <= 10` and `Quality of Faculty Rank <= 10` with:
#
# ```python
# rankings[(rankings["Quality of Education Rank"] <= 10) & (rankings["Quality of Faculty Rank"] <= 10)]
# ```

# + tags=[]
# compute and store the answer in the variable 'singapore_inst', then display it
b=(rankings['Country']=='Singapore') & (rankings['Year']=='2020-2021')
singapore_inst=rankings[b]
singapore_inst

# + deletable=false editable=false
grader.check("q6")

# + [markdown] deletable=false editable=false
# **Question 7:** In the `Year` *2019-2020*, what was the **highest-ranked** institution in the `Country` *Germany*?
#
# Your output **must** be a **string** representing the **name** of this institution.
#
# **Hint:** The highest-ranked institution in *Germany* is the institution from Germany with a `National Rank` of *1*.

# + tags=[]
# compute and store the answer in the variable 'german_best_name', then display it
b=(rankings['Year']=='2019-2020')&(rankings['Country']=='Germany')&(rankings['National Rank']==1)
german_best=rankings[b]
german_best_name=german_best['Institution'].iloc[0]
german_best_name

# + deletable=false editable=false
grader.check("q7")

# + [markdown] deletable=false editable=false
# **Question 8:** In the `Year` *2019-2020*, list **all** the institutions in the *USA* that were ranked **better** than the highest-ranked institution in *Germany*.
#
# Your output **must** be a **list** containing the **names** of all universities from *USA* with a **better** `World Rank` than the institution `german_best_name` in the year 2019-2020. By **better** ranked, we refer to institutions with a **lower** value under the `World Rank` column.
#
# **Hint:** You could store the entire row of the highest ranked institution from Germany in a different variable in q6, and use it to extract its `World Rank`.

# + tags=[]
# compute and store the answer in the variable 'us_better_than_german_best', then display it
us_better_than_german_best =[]
b = (rankings['Year']=='2019-2020')&(rankings['Country']=='USA')
us_19_20 = rankings[b]
german_rank = german_best['World Rank'].iloc[0]
b = us_19_20['World Rank']<german_rank
us_19_20 = us_19_20[b]
us_better_than_german_best = list(us_19_20['Institution'])

us_better_than_german_best

# + deletable=false editable=false
grader.check("q8")

# + [markdown] deletable=false editable=false
# **Question 9:** What is the **highest-ranked** institution based on `Quality of Education Rank` in *China* for the `Year` *2021-2022*?
#
# Your output **must** be a **string** representing the **name** of this institution. You may **assume** there is only one institution satisfying these requirements. By the **highest-ranked** institution, we refer to the institution with the **least** value under the `Quality of Education Rank` column.
#
# **Hint:** You can find the **minimum** value in a **Series** with the `Series.min` method. You can find the documentation [here](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.min.html).

# + tags=[]
# compute and store the answer in the variable 'china_highest_qoe', then display it
b = (rankings['Country']=='China')&(rankings['Year']=='2021-2022')
china_21_22=rankings[b]

china_highest_qoe=china_21_22.sort_values('Quality of Education Rank',ascending = True).iloc[0]['Institution']
china_highest_qoe

# + deletable=false editable=false
grader.check("q9")

# + [markdown] deletable=false editable=false
# **Question 10:** What are the **top** *five* **highest-ranked** institutions based on `Research Performance Rank` in *India* for the `Year` *2020-2021*?
#
# Your output **must** be a **list** of institutions **sorted** in *increasing* order of their `Research Performance Rank`.
#
# **Hint:** For sorting a DataFrame based on the values of a particular column, you can use the `DataFrame.sort_values(by="column_name")` method (where `column_name` is the column on which you want to sort). You can find the documentation [here](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sort_values.html).

# + tags=[]
# compute and store the answer in the variable 'india_highest_research', then display it
b = (rankings['Country']=='India')&(rankings['Year']=='2020-2021')
india_20_21=rankings[b].sort_values('Research Performance Rank')
india_highest_research_df =india_20_21.head()
india_highest_research = list(india_highest_research_df['Institution'])

india_highest_research

# + deletable=false editable=false
grader.check("q10")

# + [markdown] deletable=false editable=false
# For the next few questions, we will be analyzing how the rankings of the institutions change across the three years in the dataset. As you might have already noticed, the list of institutions in each year's rankings are different. As a result, for several institutions in the dataset, we do not have the rankings for all three years. Since it will be more challenging to analyze such institutions, we will simply skip them.

# + [markdown] deletable=false editable=false
# **Question 11:** How **many** institutions have rankings for **all** three years?
#
# Your output **must** be an **integer**. To get started, you have been provided with a code snippet below.
#
# **Hint:** You could make **sets** of the institutions that appear in each **DataFrame**, and find their **intersection**. Look up how to find the intersection of two or more sets in Python, on the internet!

# + tags=[]
# replace the ... with your code

year_2019_ranking_df = rankings[rankings["Year"] == "2019-2020"]
year_2020_ranking_df = rankings[rankings["Year"] == "2020-2021"]
year_2021_ranking_df = rankings[rankings["Year"] == "2021-2022"]

# TODO: make sets of the institutions in each of the three years
institutions_2019 = set(year_2019_ranking_df["Institution"])
institutions_2020 = set(year_2020_ranking_df["Institution"])
institutions_2021 = set(year_2021_ranking_df["Institution"])
# TODO: find the intersection of the three sets
institutions_2019_2020_2021 = institutions_2019 & institutions_2020 & institutions_2021
# TODO: find the length of the intersection
num_institutions_2019_2020_2021 = len(institutions_2019_2020_2021)

num_institutions_2019_2020_2021
# TODO: make sets of the institutions in each of the three years
# TODO: find the length of the intersection of the three sets

# + deletable=false editable=false
grader.check("q11")

# + [markdown] deletable=false editable=false
# ### Data Structure 1: `institutions_df`
#
# You are now going to create a new **DataFrame** with a **unique** list of institutions which have featured in the rankings for **all** three years, along with their `World Ranking` across the three years. Specifically, the **DataFrame** would have the following four columns - `Institution`, `2019_ranking`, `2020_ranking`, and `2021_ranking`. To get started, you can use the following code snippet:

# + tags=[]
# define the variable 'institutions_df'
list_of_dicts =[]
institution_list = list(institutions_2019_2020_2021)
for i in range(len(institution_list)):
    school_dict ={}
    school_name = institution_list[i]
    rank_2019 = year_2019_ranking_df[year_2019_ranking_df['Institution']==school_name]['World Rank'].iloc[0]
    rank_2020 = year_2020_ranking_df[year_2020_ranking_df['Institution']==school_name]['World Rank'].iloc[0]
    rank_2021 = year_2021_ranking_df[year_2021_ranking_df['Institution']==school_name]['World Rank'].iloc[0]
    school_dict['Institution'] = school_name
    school_dict['2019_ranking']=rank_2019
    school_dict['2020_ranking']=rank_2020
    school_dict['2021_ranking']=rank_2021
    list_of_dicts.append(school_dict)

institutions_df= pd.DataFrame(list_of_dicts)
# TODO: initalize an empty list to store the list of institutions
# TODO: loop through the variable 'institutions_2019_2020_2021' defined above
    # TODO: create a new dictionary with the necessary key/value pairs
    # TODO: append the dictionary to the list
# TODO: create the DataFrame from the list of dictionaries

# + deletable=false editable=false
grader.check("institutions_df")

# + [markdown] deletable=false editable=false
# **Question 12:** Between the years *2019-2020* and *2021-2022*, **list** the institutions which have seen an **improvement** in their `World Rank` by **more than** *500* ranks.
#
# Your output **must** be a **list** of institution names. The **order** does **not** matter. You **must** use the DataFrame `institutions_df` to answer this question.
#
# **Hints:**
#
# 1. In pandas, subtraction of two columns can be simply done using subtraction(`-`) operator. For example,
# ``` python
# df["difference"] = df["column1"] - df["column2"]
# ```
# will create a *new column* `difference` with the difference of the values from the columns `column1` and `column2`.
# 2. Note that an *improved* ranking means that the `World Rank` has *decreased*.

# + tags=[]
# compute and store the answer in the variable 'improved_institutions', then display it
institutions_df['21-22 - 19-20']=institutions_df['2021_ranking']-institutions_df['2019_ranking']
b = institutions_df['21-22 - 19-20']<-500
institutions_df[b]
diff_institutions = institutions_df[b]
improved_institutions = list(diff_institutions['Institution'])

improved_institutions

# + deletable=false editable=false
grader.check("q12")

# + [markdown] deletable=false editable=false
# **Question 13:** Between the years 2019-2020 and 2021-2022, which institution had the **largest** change in its `World Rank`?
#
# Your output **must** be a **string** representing the name of the institution with the **greatest absolute difference** between its `World Rank` in 2019-2020 and 2021-2022. You **must** use the DataFrame `institutions_df` to answer this question.
#
# **Hint:** You can find maximum value in a Series with the `Series.max` method. You can find the documentation [here](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.max.html).

# + tags=[]
# compute and store the answer in the variable 'most_change_inst', then display it
institutions_df['abs 21-22 - 19-20']= abs(institutions_df['2021_ranking']-institutions_df['2019_ranking'])

most_change_inst=institutions_df.sort_values('abs 21-22 - 19-20').iloc[-1]['Institution']
most_change_inst

# + deletable=false editable=false
grader.check("q13")

# + [markdown] deletable=false editable=false
# **Question 14:** For all the three years, find the **number** of institutions that **improved** their `World Rank` **each year**.
#
# Your output **must** be an **integer** representing the number of institutions whose `World Rank` **strictly** increased each year. You **must** use the DataFrame `institutions_df` to answer this question.

# + tags=[]
# compute and store the answer in the variable 'strictly_improved', then display it
institutions_df['20-19']= institutions_df['2020_ranking']-institutions_df['2019_ranking']
institutions_df['21-20']=institutions_df['2021_ranking']-institutions_df['2020_ranking']
b = (institutions_df['21-20']<0)&(institutions_df['20-19']<0)
improved_df = institutions_df[b]
strictly_improved=len(improved_df)
strictly_improved

# + deletable=false editable=false
grader.check("q14")

# + [markdown] deletable=false editable=false
# **Question 15:** In the `Year` *2020-2021*, **list** the institutions which are within the **top** 10 in the world based on `Alumni Employment Rank` but do **not** feature in the top 10 of the `World Ranking`.
#
#
# Your output **must** be a **list** of institutions. The **order** does **not** matter. You **must** use the `year_2020_ranking_df` DataFrame that you created in q11 to answer this question.
# -



# + tags=[]
# compute and store the answer in the variable 'top_only_aer', then display it
b = (year_2020_ranking_df['Alumni Employment Rank']<=10)&(year_2020_ranking_df['World Rank']>10)
df_2020_2021 = year_2020_ranking_df[b]

top_only_aer= list(df_2020_2021['Institution'])
top_only_aer

# + deletable=false editable=false
grader.check("q15")

# + [markdown] deletable=false editable=false
# **Question 16:** **List** the universities which ranked in the **top** 100 of world rankings (`World Rank`) in the `Year` *2019-2020* but **failed** to do so in the `Year` *2021-2022*.
#
# Your output **must** be a **list** of institutions. The **order** does **not** matter. You **must** use the `year_2019_ranking_df` and `year_2021_ranking_df` DataFrames that you created in q11 to answer this question.
#
# **Hints:**
# 1. There could be institutions that are ranked in the **top** 100 in *2019-2020* but do not feature in *2021-2022*; you still want to include them in your list.
# 2. You can use `sort_values` to identify the **top** 100 institutions.
# 3. Given two *sets* `A` and `B`, you can find the elements which are in `A` but not in `B` using `A - B`. For example,
# ```python
# set_A = {10, 20, 30, 40, 50}
# set_B = {20, 40, 70}
# set_A - set_B == {10, 30, 50} # elements which are in set_A but not in set_B
# ```

# + tags=[]
# compute and store the answer in the variable 'top_only_2019', then display it
b1 = year_2019_ranking_df['World Rank']<=100
top_100_19_20 = year_2019_ranking_df[b1]
b2 = year_2021_ranking_df['World Rank']<=100
top_100_21_22 =year_2021_ranking_df[b2]
top_only_2019=set(top_100_19_20['Institution'])-set(top_100_21_22['Institution'])
top_only_2019 = list(top_only_2019)
top_only_2019

# + deletable=false editable=false
grader.check("q16")

# + [markdown] deletable=false editable=false
# **Question 17:** **List** the countries which have **at least** *10* institutions featuring in the **top** *100* of world rankings (`World Rank`) in the `Year` *2020-2021*.
#
# Your output **must** be a **list**.
#
# **Hints:**
#
# 1. In a **DataFrame**, to find the **number** of times each unique value in a column repeats, you can use the `DataFrame.value_counts` method. For example,
# ``` python
# rankings["Country"].value_counts()
# ```
# would output a `pandas` **Series** with the **indices** being the unique values of `Country` and the **values** being the **number** of times each country has featured in the `rankings` **DataFrame**. You can find the documentation [here](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.value_counts.html). You can adapt this code to find the number of institutions from each country that features in the `Year` *2020-2021*.
# 2. Just like with **DataFrames**, you can use Boolean indexing on **Series**. For example, try something like this in a separate cell below:
# ```python
# a = pd.Series([100, 200, 300])
# a[a > 100]
# ```
# 3. You can extract the **indices** of a **Series**, `s` with `s.index`.

# + tags=[]
# compute and store the answer in the variable 'top_countries', then display it
b = year_2020_ranking_df['World Rank']<=100
top_100_21_20 = year_2020_ranking_df[b]
top_100_counts=top_100_21_20['Country'].value_counts()
b=top_100_counts>=10
top_countries=list(top_100_counts[b].index)
top_countries

# + deletable=false editable=false
grader.check("q17")

# + [markdown] deletable=false editable=false
# ## Beautiful Soup

# + [markdown] deletable=false editable=false
# ## Setup
#
# In real life, you don't often have data in nice JSON format like `rankings.json`. Instead, data needs to be *scraped* from multiple webpages and requires some cleanup before it can be used.
#
# Most of the projects in CS220 have used data obtained via web scraping, including this one. For p12, as explained above, we obtained the data by scraping the following websites:
#
# * https://cwur.org/2021-22.php
# * https://cwur.org/2020-21.php
# * https://cwur.org/2019-20.php
#
# Our `rankings.json` file was created using data from these webpages. For the rest of this project, you will write the code to **recreate** `rankings.json` file from the tables in these html pages yourself! We also do **not** want all students in this class to be making multiple requests to the webpages above, as that could be very costly for the people managing the webpages. Instead, we have made **copies** of the webpages above, which can be found here:
#
# * https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f22-projects/-/raw/main/p12/2019-2020.html
# * https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f22-projects/-/raw/main/p12/2020-2021.html
# * https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f22-projects/-/raw/main/p12/2021-2022.html
#
# Before you can parse these html files, you must first *download* them. You **must** use your `download` function to download these files.

# + tags=[]
# use the 'download' function to download the data from the webpage
# 'https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f22-projects/-/raw/main/p12/2019-2020.html'
# to the file '2019-2020.html'
download('2019-2020.html','https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f22-projects/-/raw/main/p12/2019-2020.html')

# + tags=[]
# use the 'download' function to download the data from the webpage
# 'https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f22-projects/-/raw/main/p12/2020-2021.html'
# to the file '2020-2021.html'
download('2020-2021.html','https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f22-projects/-/raw/main/p12/2020-2021.html')

# + tags=[]
# use the 'download' function to download the data from the webpage
# 'https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f22-projects/-/raw/main/p12/2021-2022.html'
# to the file '2021-2022.html'
download('2021-2022.html','https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f22-projects/-/raw/main/p12/2021-2022.html')

# + [markdown] deletable=false editable=false
# **Question 18:** Use `BeautifulSoup` to **parse** `2019-2020.html`, and find the **table** containing the ranking data. What are the **column names** of this table?
#
# Your output **must** be a **list** of **column names** from this table. There are no restrictions on 'hardcoding' **indices** or **html tags**.
#
# **Hint:** You **must** use the `find` or `find_all` **methods** to identify the table and its header.

# + tags=[]
# compute and store the answer in the variable 'header', then display it
f = open('2019-2020.html',encoding='utf-8')
html_text = f.read()
f.close()
bs_obj = BeautifulSoup(html_text,'html.parser')
table_stuff = bs_obj.find('table')
th_stuff = table_stuff.find_all('th')
header = []
for i in range(len(th_stuff)):
    column = th_stuff[i].text
    header.append(column)
    
header

# + deletable=false editable=false
grader.check("q18")


# + [markdown] deletable=false editable=false
# ### Function 2: `parse_html(filename)`
#
# You **must** write this function which takes in a HTML file `filename` as its input, parses it, and returns a **list** of **dictionaries** containing all the data in the **table** stored in `filename`.
#
# There are **no** restrictions on 'hardcoding' html tags.
#
# For example, the output of the function call `parse_html("2019-2020.html")` **must** look like this:
#
# ```python
# [{'Year': '2019-2020',
#   'World Rank': 1,
#   'Institution': 'Harvard University',
#   'Country': 'USA',
#   'National Rank': 1,
#   'Quality of Education Rank': 2,
#   'Alumni Employment Rank': 1,
#   'Quality of Faculty Rank': 1,
#   'Research Performance Rank': 1,
#   'Score': 100},
#  {'Year': '2019-2020',
#   'World Rank': 2,
#   'Institution': 'Massachusetts Institute of Technology',
#   'Country': 'USA',
#   'National Rank': 2,
#   'Quality of Education Rank': 1,
#   'Alumni Employment Rank': 10,
#   'Quality of Faculty Rank': 2,
#   'Research Performance Rank': 5,
#   'Score': 96.7},
# ...]
# ```
#
# You can copy/paste this function from lab-p12 if you have already defined it there.

# + tags=[]
# define the function 'parse_html' here
def parse_html(filename):
    f = open(filename, encoding ='utf-8')                 # read file
    html_text = f.read()
    f.close()
    
    bs_obj=BeautifulSoup(html_text,'html.parser')         # create BeautifulSoup object
    
    table_stuff = bs_obj.find('table')                    # find table
    
    th_stuff = bs_obj.find_all('th')
    header = [th_stuff[i].text for i in range(len(th_stuff))] # create header
    
    
    tr_stuff=table_stuff.find_all('tr')                  # find rows
    
    
    rows = tr_stuff[1:]                                  # remove header from rows
    schools_list =[]
    
    for i in range(len(rows)):                           # parse over rows
        row_i = rows[i]
        td_list = row_i.find_all('td')                   # find cells create list
        schools_dict = {}
        for idx in range(len(td_list)):                  # interate over list
            value = td_list[idx].text                    # get value
            key = header[idx]                            # get key
            if value == '-':                             # check for missing
                value = None
            elif key=='Institution' or key=='Country':   # check to str, int, float value
                value = str(value)                            
            elif key =='Score':                             
                value = float(value)                    
            else:                                            
                value = int(value)                            
            schools_dict[key]=value                      # add to dict
        schools_dict['Year']= filename[:9]               # add year
        schools_list.append(schools_dict)                # append 
    return schools_list                                  # return


# + [markdown] deletable=false editable=false
# **Question 19:** List the **statistics** of the **first** 5 dictionaries institutions in the file `2019-2020.html`.
#
# Your output **must** be a **list** of **dictionaries**. You **must** use the `parse_html` function to parse the file, and **slice** the first five **lists** to answer this question.

# + tags=[]
# compute and store the answer in the variable 'rankings_2019_top_5', then display it
rankings_2019_top_5 = parse_html('2019-2020.html')[:5]
rankings_2019_top_5

# + deletable=false editable=false
grader.check("q19")


# + [markdown] deletable=false editable=false
# **Question 20:** Parse the contents of the **three** files `2019-2020.html`, `2020-2021.html`, and `2021-2022.html` and combine them to create a **single** file named `my_rankings.json`.
#
# You **must** create a **file** named `my_rankings.json` in your current directory. The contents of this file **must** be **identical** to `rankings.json`.
#
# **Hints:**
# 1. Using the logic from the question above, combine the data from these three files into a single list of dicts, and write it into the file `"my_rankings.json"`.
# 2. You can use the `write_json` function that was introduced in lecture.

# + tags=[]
# the 'write_json' function from lecture has been provided for you here

def write_json(path, data):
    with open(path, 'w', encoding = "utf-8") as f:
        json.dump(data, f, indent = 2)


# + tags=[]
# parse the three files and write the contents into 'my_rankings.json'
school_19_20 = parse_html('2019-2020.html')
school_20_21 = parse_html('2020-2021.html')
school_21_22 = parse_html('2021-2022.html')
complete_schools = []
complete_schools.extend(school_19_20)
complete_schools.extend(school_20_21)
complete_schools.extend(school_21_22)
write_json('my_rankings.json',complete_schools)



# + deletable=false editable=false
grader.check("q20")

# + [markdown] deletable=false editable=false
# ## Submission
# Make sure you have run all cells in your notebook in order before running the following cells, so that all images/graphs appear in the output.
# It is recommended that at this stage, you Restart and Run all Cells in your notebook.
# That will automatically save your work and generate a zip file for you to submit.
#
# If the last cell fails to run because of the file size, delete the images that we have provided in this notebook as examples, and run the last cell again.
#
# **SUBMISSION INSTRUCTIONS**:
# 1. **Upload** the zipfile to Gradescope.
# 2. Check **Gradescope otter** results as soon as the auto-grader execution gets completed. Don't worry about the score showing up as -/100.0. You only need to check that the test cases passed.

# + [code] deletable=false editable=false
# running this cell will create a new save checkpoint for your notebook
from IPython.display import display, Javascript
display(Javascript('IPython.notebook.save_checkpoint();'))

# + [code] deletable=false editable=false
# !jupytext --to py p12.ipynb

# + [code] deletable=false editable=false
p12_test.check_file_size("p12.ipynb")
grader.export(pdf=False, run_tests=True, files=[py_filename])

# + [markdown] deletable=false editable=false
#  
