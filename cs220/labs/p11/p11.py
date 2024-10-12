#!/usr/bin/env python
# coding: utf-8
import otter
# nb_name should be the name of your notebook without the .ipynb extension
nb_name = "p11"
py_filename = nb_name + ".py"
grader = otter.Notebook(nb_name + ".ipynb")

import p11_test

# # Project 11: Analyzing Stars and Planets

# # Learning Objectives:
#
# In this project, you will demonstrate how to:
#     
# * analyze the data from p10,
# * make scatter plots using `matplotlib`,
# * remove outliers to make the plots more useful,
# * use recursion to gather new data.
#
# **Please go through [lab-p11](https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f22-projects/-/tree/main/lab-p11) before working on this project.** The lab introduces some important techniques related to this project.

# ## Note on Academic Misconduct:
#
# **IMPORTANT**: p10 and p11 are two parts of the same data analysis. You **cannot** switch project partners between these two projects. That is if you partnered up with someone for p10, you have to sustain that partnership until end of p11. Now may be a good time to review [our course policies](https://cs220.cs.wisc.edu/f22/syllabus.html).

# ## Testing your code:
#
# Along with this notebook, you must have downloaded the files `p11_test.py` and `p11_plots.json`. If you are curious about how we test your code, you can explore this file, and specifically the value of the variable `expected_json`, to understand the expected answers to the questions.

# ## Setup:
#
# In p11, you will be analyzing the same dataset that you parsed in p10. You can either copy/paste the `data` directory to your p11 directory, or download the `data.zip` file provided with this project, and extract it. In addition to the `data` directory, you will also need to download additional datasets for p11. You must download `broken_data.zip` and extract it. You must extract the contents of the directory `broken_data` into the same directory which contains the `data` directory, `p11.ipynb`, `p11_test.py`, and `p11_plots.json`.
#
# You need to make sure that the project files are stored in the following structure:
#
# ```
# +-- p11.ipynb
# +-- p11_test.py
# +-- p11_plots.json
# +-- data
# |   +-- .DS_Store
# |   +-- .ipynb_checkpoints
# |   +-- mapping_1.json
# |   +-- mapping_2.json
# |   +-- mapping_3.json
# |   +-- mapping_4.json
# |   +-- mapping_5.json
# |   +-- planets_1.csv
# |   +-- planets_2.csv
# |   +-- planets_3.csv
# |   +-- planets_4.csv
# |   +-- planets_5.csv
# |   +-- stars_1.csv
# |   +-- stars_2.csv
# |   +-- stars_3.csv
# |   +-- stars_4.csv
# |   +-- stars_5.csv
# +-- broken_data
# |   +-- .DS_Store
# |   +-- .ipynb_checkpoints
# |   +-- hds
# |   |   +-- .ipynb_checkpoints
# |   |   +-- hd_1000s
# |   |   |   +-- hd_10000s.json
# |   |   +-- others.json
# |   +-- k2s.json
# |   +-- keplers
# |   |   +-- kepler_100s
# |   |   |   +-- kepler_100s
# |   |   |   |   +-- kepler_100s
# |   |   |   |   |   +-- kepler_100s.json
# |   |   |   |   +-- others.json
# |   |   |   +-- kepler_200s
# |   |   |   |   +-- .ipynb_checkpoints
# |   |   |   |   +-- kepler_220s.json
# |   |   |   |   +-- kepler_290s.json
# |   |   |   |   +-- others
# |   |   |   |   |   +-- others.json
# |   |   |   +-- others.json
# |   |   +-- kepler_10s
# |   |   |   +-- kepler_80s
# |   |   |   |   +-- kepler_80s.json
# |   |   |   +-- others
# |   |   |   |   +-- kepler_20s.json
# |   |   |   |   +-- kepler_30s.json
# |   |   |   |   +-- others.json
# |   |   +-- others
# |   |   |   +-- .DS_Store
# |   |   |   +-- others.json
# |   +-- others
# |   |   +-- .DS_Store
# |   |   +-- gjs.json
# |   |   +-- others.json
# |   |   +-- tois
# |   |   |   +-- tois.json
# ```
#
# Make sure that **all** files are stored in this **exact** file structure. Otherwise, then there is a possibility that your code will **fail on Gradescope** even after passing local tests.

# ## Project Description:
#
# You have already parsed the data in the `data` directory in p10. You will now dive deeper by analyzing this data and arrive at some exciting conclusions about various planets and stars outside our Solar System. You will also use recursion to retrieve data from the broken JSON file in the `data` directory, and ask some interesting questions about the data.

# ## Project Requirements:
#
# You **may not** hardcode indices in your code, unless the question explicitly. If you open your `.csv` files with Excel, manually count through the rows and use this number to loop through the dataset, this is also considered as hardcoding. We'll **manually deduct** points from your autograder score on Gradescope during code review.
#
# **Store** your final answer for each question in the **variable specified for each question**. This step is important because Otter grades your work by comparing the value of this variable against the correct answer.
#
# For some of the questions, we'll ask you to write (then use) a function to compute the answer. If you compute the answer **without** creating the function we ask you to write, we'll **manually deduct** points from your autograder score on Gradescope, even if the way you did it produced the correct answer.
#
# Required Functions:
# - `get_all_paths_in`
# - `get_surface_gravity`
# - `get_distances_to_star`
# - `get_liquid_water_distances`
# - `get_surface_temperatures`
#
# In this project, you will also be required to define certain **data structures**. If you do not create these data structures exactly as specified, we'll **manually deduct** points from your autograder score on Gradescope, even if the way you did it produced the correct answer.
#
# Required Data Structures:
# - `Star` (**namedtuple**)
# - `stars_dict` (**dictionary** mapping **strings** to `Star` objects)
# - `Planet` (**namedtuple**)
# - `planets_list` (**list** of `Planet` objects)
# - `star_classes` (**dictionary**)
# - `all_planets_list` (**list** of `Planet` objects)
#
# In addition, you are also **required** to follow the requirements below:
#
# * You are **not** allowed to use **modules** like `pandas` to answer the questions in this project.
# * You **must** properly **label** the axes of all your **plots**.
# * Do **not** use meaningless names for variables or functions (example of what **not** to do: `uuu = "my name"`).
# * Do **not** write the exact same code in multiple places. Instead, wrap this code into a function and call that function whenever the code should be used.
# * Avoid **inappropriate** use of data structures. For example, using a for loop to search for a corresponding value in a dictionary with a given key instead of using `dictname[key]` directly.
# * Do **not** use python keywords or built-in functions as variable names (example of what **not** to do: `str = "23"`).
# * Do **not** define multiple functions with the same name or define multiple versions of one function with different names. Just keep the best version.
# * Do **not** leave in irrelevant output or test code that we didn't ask for.
#
# We will **manually deduct** points if you do **not** follow these guidelines.
#
# For more details on what will cause you to lose points during code review and specific requirements, please take a look at the [Grading rubric](https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f22-projects/-/blob/main/p11rubric.md).

# ## Questions and Functions:
#
# Let us start by importing all the modules we will need for this project.

# it is considered a good coding practice to place all import statements at the top of the notebook
# please place all your import statements in this cell if you need to import any more modules for this project
import csv
import json
import os
from collections import namedtuple
import statistics
import matplotlib.pyplot as plt
import math

# ### Loading in the Stars and Planets:
#
# Before we can analyze the data in the `data` directory, you must first copy/paste all the functions and data strucutres you created in p10 to parse the data.

# +
all_files = os.listdir('data')
files_in_data= []
for file in all_files:
    if not file.startswith('.'):
        files_in_data.append(file)
files_in_data.sort()

stars_paths =[]
for file in files_in_data:
    if file.startswith('stars'):
        path = os.path.join('data',file)
        stars_paths.append(path)    
stars_paths.sort()

planet_paths =[]
for file in files_in_data:
    if file.startswith('planets'):
        path = os.path.join('data',file)
        planet_paths.append(path)
planet_paths.sort()

json_paths =[]
for file in files_in_data:
    if file.endswith('json'):
        path = os.path.join('data',file)
        json_paths.append(path)
json_paths.sort()

# -

# copy/paste the definition of the namedtuple 'Star' here
star_stuff =['spectral_type','stellar_effective_temperature','stellar_radius','stellar_mass','stellar_luminosity','stellar_surface_gravity','stellar_age']
Star = namedtuple('Star',star_stuff)


# copy/paste the definition of the function 'process_csv' here
def process_csv(filename):
    example_file = open(filename, encoding="utf-8")
    example_reader = csv.reader(example_file)
    example_data = list(example_reader)
    example_file.close()
    return example_data


# copy/paste the definition of the function 'star_cell' here
def star_cell(row_idx, col_name, stars_rows, header):
    col_idx = header.index(col_name)
    val = stars_rows[row_idx][col_idx]
    if val == '':
        return None
    else:
        if col_name =='Spectral Type' or col_name =='Name':
            return str(val)
        else:
            return float(val)


# copy/paste the definition of the function 'get_stars' here
def get_stars(star_file):
    star_list = process_csv(star_file)
    star_header = star_list[0]
    star_rows = star_list[1:]
    length = len(star_rows)
    star_dict = {}
    for row_idx in range(length):
        star_name = star_cell(row_idx, 'Name', star_rows,star_header)
        spectral_type = star_cell(row_idx, 'Spectral Type', star_rows,star_header)
        stellar_effective_temperature = star_cell(row_idx, 'Stellar Effective Temperature [K]', star_rows,star_header)
        stellar_radius = star_cell(row_idx, 'Stellar Radius [Solar Radius]', star_rows,star_header)
        stellar_mass = star_cell(row_idx, 'Stellar Mass [Solar mass]', star_rows,star_header)
        stellar_luminosity = star_cell(row_idx, 'Stellar Luminosity [log(Solar)]', star_rows,star_header)
        stellar_surface_gravity = star_cell(row_idx, 'Stellar Surface Gravity [log10(cm/s**2)]', star_rows,star_header)
        stellar_age = star_cell(row_idx, 'Stellar Age [Gyr]', star_rows, star_header)

        star = Star(spectral_type, stellar_effective_temperature, stellar_radius, \
                      stellar_mass, stellar_luminosity, \
                      stellar_surface_gravity, stellar_age)
        star_dict[star_name]=star
    
    return star_dict


# copy/paste the definition of the dictionary 'stars_dict' here
stars_dict = {}
for i in range(len(stars_paths)):
    stars_dict.update(get_stars(stars_paths[i]))

# copy/paste the definition of the namedtuple 'Planet' here
planet_stuff=['planet_name','host_name','discovery_method','discovery_year','controversial_flag','orbital_period','planet_radius','planet_mass','semi_major_radius','eccentricity','equilibrium_temperature','insolation_flux']
Planet = namedtuple('Planet',planet_stuff)


# copy/paste the definition of the function 'read_json' here
def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# copy/paste the definition of the function 'planet_cell' here
def planet_cell(row_idx, col_name, planets_rows, header):
    col_idx = header.index(col_name) 
    val = planets_rows[row_idx][col_idx] 
    if val == '':
        return None
    elif col_name in ["Controversial Flag"]:
        if val == "1":
            return True
        else:
            return False
    elif col_name =='Planet Name' or col_name == 'Discovery Method':
        return str(val)
    elif col_name == 'Discovery Year':
        return int(val)
    else:
        return float(val)


# copy/paste the definition of the function 'get_planets' here
def get_planets(planet_file, mapping_file):
    try:
        mapping=read_json(mapping_file)
    except json.JSONDecodeError:
        return []
    data = process_csv(planet_file)
    planets_header = data[0]
    planets_rows = data[1:]
    length = len(planets_rows)
    planets_list = []
    for row_idx in range(length):
        try:
            planet_name = planet_cell(row_idx, 'Planet Name', planets_rows,planets_header)
            host_name = mapping[planet_name]
            discovery_method = planet_cell(row_idx, 'Discovery Method', planets_rows,planets_header)
            discovery_year = planet_cell(row_idx, 'Discovery Year', planets_rows,planets_header)
            controversial_flag = planet_cell(row_idx, 'Controversial Flag', planets_rows,planets_header)
            orbital_period = planet_cell(row_idx, 'Orbital Period [days]', planets_rows,planets_header)
            planet_radius = planet_cell(row_idx, 'Planet Radius [Earth Radius]', planets_rows,planets_header)
            planet_mass = planet_cell(row_idx, 'Planet Mass [Earth Mass]', planets_rows,planets_header)
            semi_major_radius = planet_cell(row_idx, 'Orbit Semi-Major Axis [au]', planets_rows,planets_header)
            eccentricity = planet_cell(row_idx, 'Eccentricity', planets_rows,planets_header)
            equilibrium_temperature = planet_cell(row_idx, 'Equilibrium Temperature [K]', planets_rows,planets_header)
            insolation_flux = planet_cell(row_idx,'Insolation Flux [Earth Flux]',planets_rows,planets_header)
            new_planet = Planet(planet_name, host_name, discovery_method, discovery_year,\
                              controversial_flag, orbital_period, planet_radius, planet_mass,\
                              semi_major_radius, eccentricity, equilibrium_temperature, insolation_flux)
            planets_list.append(new_planet)
        except (IndexError, ValueError, KeyError,TypeError) as e:
            continue
    return planets_list


# copy/paste the definition of the list 'planets_list' here
planets_list=[]
for i in range(len(planet_paths)):
    json_i = json_paths[i]
    csv_i = planet_paths[i]
    planet_i = get_planets(csv_i,json_i)
    for i in range(len(planet_i)):
        planets_list.append(planet_i[i])


# You used two functions `plot_scatter` and `plot_scatter_multiple` in lab-p11 to create your **scatter plots**. These functions are again provided for you here to use in p11.

# +
# remember to import matplotlib.pyplot as plt at the top of the notebook to make these functions work

def plot_scatter(x_data, y_data, x_label='x axis', y_label='y axis', c=None, s=7):
    plt.scatter(x_data, y_data, c=c, s=s)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    
def plot_scatter_multiple(x_data_dict, y_data_dict, x_label='x axis', y_label='y axis'):
    legend_values = list(x_data_dict.keys())
    for key in x_data_dict:
        plt.scatter(x_data_dict[key], y_data_dict[key], s=7)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend(legend_values)


# -

# ### Verifying Laws of Nature:
#
# We will now use our dataset to verify some well-known laws of nature.

# #### Kepler's Third Law:
#
# We will first verify [Kepler's Third Law](https://en.wikipedia.org/wiki/Kepler%27s_laws_of_planetary_motion#Third_law). This law states that the **square** of the `orbital_period` of each planet in a solar system is directly proportional to the **cube** of the `semi_major_radius` of its orbit around its host star.
#
# Since this law relates only to planets that orbit the same host star, we will verify this law using the several planets orbiting around a star named *GJ 9827*.

# **Question 1:** Compute the **ratio** of the **square** of the `orbital_period` to the **cube** of the `semi_major_radius` of each planet orbiting the star *GJ 9827*.
#
# Your output **must** be a **list** of **floats**. You may **assume** that the planets orbiting this star do not have any missing `orbital_period` or `semi_major_radius` data.

# compute and store the answer in the variable 'ratios_gj9827', then display it
ratios_gj9827=[]
for planet in planets_list:
    if planet.host_name == 'GJ 9827':
        op = planet.orbital_period
        smr = planet.semi_major_radius
        val = op**2/smr**3
        ratios_gj9827.append(val)
ratios_gj9827

grader.check("q1")

# The **ratios** of the three stars in this system appear to be very close to each other. It will be useful if we could quantify exactly how close these ratios are to each other. One way to do that would to be compute the [coefficient of variance](https://en.wikipedia.org/wiki/Coefficient_of_variation), which is defined as the **standard deviation** divided by the **mean** of a sequence of numbers. A low value would imply that the numbers are very **close** to each other.

# **Question 2:** Compute the **coefficient of variance** of the **list** `ratios_gj9827`.
#
# **Hint:** You can compute the **standard deviation** and the **mean** of a **list** of numbers using the `statistics.stdev` and `statistics.mean` functions inside the `statistics` module. To do this, you must first **import** the `statistics` module. You can read the documentation for the `statistics.stdev` function [here](https://docs.python.org/3.9/library/statistics.html#statistics.stdev), and the documentation for `statistics.mean` [here](https://docs.python.org/3.9/library/statistics.html#statistics.mean).

# compute and store the answer in the variable 'coeff_gj9827', then display it
coeff_gj9827 = 0
mean_ratio = statistics.mean(ratios_gj9827)
sd_ratio = statistics.stdev(ratios_gj9827)
coeff_gj9827 = sd_ratio/mean_ratio
coeff_gj9827

grader.check("q2")

# As we can see, the **coefficient of variance** is indeed very low. This lends credibility to Kepler's Third Law. However, there is yet more we can do with this data. After we adjust for the units used in the project, we find that Kepler's Third Law predicts the following:
#
# $$\texttt{stellar mass} = \frac{133408}{\texttt{ratio}}$$
#
# where $\texttt{ratio}$ is the **mean** of the ratios of the **square** of the `orbital_period` to the **cube** of the `semi_major_radius` computed above, and $\texttt{stellar mass}$ is the mass of the planets' host star.
#
# We can therefore check how close this **predicted** `stellar_mass` is to the **actual** `stellar_mass` of the star.

# **Question 3:** Compute the percentage change of the **predicted** `stellar_mass` from the **actual** `stellar_mass` of the star *GJ 9827*.
#
# You **must** compute the **predicted** `stellar_mass` as the number *133408* divided by the **mean** of the ratios of the three planets computed in q1. You **must** find the **actual** `stellar_mass` by accessing the correct attribute of the `Star` object of *GJ 9827*. The percentage change can be computed as:
#
# $$\texttt{percent change} = \frac{\texttt{predicted stellar mass} - \texttt{actual stellar mass}}{\texttt{actual stellar mass}} \times 100$$

# +
# compute and store the answer in the variable 'percentage_change', then display it
predicted = 133408/mean_ratio
actual = stars_dict['GJ 9827'].stellar_mass
percentage_change = (predicted-actual)/actual*100

percentage_change 
# -

grader.check("q3")

# #### Stefan-Boltzmann Law:
#
# We will now verify the [Stefan-Boltzmann Law](https://en.wikipedia.org/wiki/Stefan%E2%80%93Boltzmann_law). This law states that the `insolation_flux` of a *black body* is directly proportional to the **fourth** power of the `equilibrium_temperature`. In our dataset, we have the `insolation_flux` and `equilibrium_temperature` data of the `Planet` objects. So, we can verify how well this law is obeyed by our dataset.

# **Question 4:** Create a **scatter plot** representing the `insolation_flux` (on the **x-axis**) against the **fourth power** of the `equilibrium_temperature` (on the **y-axis**) of each `Planet` object in `planets_list`.
#
# You **must** ignore all `Planet` objects with **missing** `insolation_flux`, or `equilibrium_temperature` data.
#
# You **must** first compute two **lists** containing the **insolation_flux**, and the **equilibrium_temperature** of each `Planet` object (which has all the data available). Then, you **must** use `plot_scatter` to plot the **insolation_flux** against the fourth power of the **equilibrium_temperature**.
#
# **Important Warning:** `p11_test.py` can check that the **lists** are correct, but it **cannot** check if your plot appears on the screen, or whether the axes are correctly labelled. Your plots will be **manually graded**, and you will **lose points** if your plot is not visible, or if it is not properly labelled.
#
# Your plot should look like this:

# <div><img src="attachment:insolation_temp.PNG" width="400"/></div>

# first compute and store the lists 'flux_list', and 'temp_4th_power_list'
# then create the scatter plot using the lists
flux_list =[]
temp_4th_power_list = []
for planet in planets_list:
    If = planet.insolation_flux
    eq = planet.equilibrium_temperature
    if If == None or eq == None:
        continue
    else:
        flux_list.append(If)
        temp_4th_power_list.append(eq**4)
plot_scatter(flux_list,temp_4th_power_list,'Insolation Flux','(Equilibrium Temperature)**4')

grader.check("q4")

# **Food for thought:** Why does this graph look so strange with all the points bunched up near the bottom-left corner?

# **Question 5:** Excluding planets with `insolation_flux` **greater than** *7000*, create a **scatter plot** representing the `insolation_flux` (on the **x-axis**) against the **fourth power** of the `equilibrium_temperature` (on the **y-axis**) of each `Planet` object in `planets_list`.
#
# You **must** ignore all `Planet` objects with **missing** `insolation_flux`, or `equilibrium_temperature` data.
#
# You **must** first compute two **lists** containing the **insolation_flux**, and the **star equilibrium_temperature** of each `Planet` object (which has all the data available). Then, you **must** use `plot_scatter` to plot the **insolation_flux** against the fourth power of the **equilibrium_temperature**.
#
# **Important Warning:** `p11_test.py` can check that the **lists** are correct, but it **cannot** check if your plot appears on the screen, or whether the axes are correctly labelled. Your plots will be **manually graded**, and you will **lose points** if your plot is not visible, or if it is not properly labelled.
#
# Your plot should look like this:

# <div><img src="attachment:insolation_temp_wo_outliers.PNG" width="400"/></div>

# first compute and store the lists 'flux_list_no_outliers', and 'temp_4th_power_list_no_outliers'
# then create the scatter plot using the lists
flux_list_no_outliers =[]
temp_4th_power_list_no_outliers = []
for planet in planets_list:
    If = planet.insolation_flux
    eq = planet.equilibrium_temperature
    if If == None or eq == None or If>7000:
        continue
    else:
        flux_list_no_outliers.append(If)
        temp_4th_power_list_no_outliers.append(eq**4)
plot_scatter(flux_list_no_outliers,temp_4th_power_list_no_outliers,'Insolation Flux','(Equilibrium Temperature)**4')

grader.check("q5")

# **Food for thought:** Does the relationship between **insolation flux** and the **fourth power of the equilibrium temperature** appear to be **linear** as predicted by the Stefan-Boltzmann Law? Can you explain why the graph isn't perfectly linear?

# ### Stellar Evolution:
#
# [Stellar Evolution](https://en.wikipedia.org/wiki/Stellar_evolution) is a description of the way that stars change with time. The primary factor determining how a star evolves is its `stellar_mass`. Depending on the `stellar_mass` of each `Star`, astronomers can predict how the `Star` will end up. A `Star` whose `stellar_mass` is $\geq 0.3$ and $< 8$ times the mass of the Sun will become a [Red Giant](https://en.wikipedia.org/wiki/Red_giant), while a `Star` whose `stellar_mass` is $\geq 8$ and $< 10.5$ times the mass of the Sun will become a [White Dwarf](https://en.wikipedia.org/wiki/White_dwarf). A `Star` that is even bigger will end up as a [Neutron Star](https://en.wikipedia.org/wiki/Neutron_star).

# ### Data Structure 1: `star_classes`
#
# You **must** now classify the `Star` objects in `stars_dict` using their `stellar_mass`. You **must** create a **dictionary** `star_classes` with the **keys**: `Red Giant`, `White Dwarf`, and `Neutron Star`. The **value** of each **key** must be a **list** of **strings** containing the **names** of the `Star` objects.
#
# You **must** **ignore** `Star` objects for which we do not have `stellar_mass` data or have `stellar_mass` **less** than *0.3* Solar masses.
#
# **Hint:** Recall that the `stellar_mass` data already uses units of *Solar masses*. So, a `stellar_mass` of *1* means that the `Star` object has the same mass as the Sun, and a `stellar_mass` of 2 means the `Star` object has twice the mass of the Sun, and so on.

# define the variable 'star_classes' here
# but do NOT display
star_classes = {}
star_classes['Red Giant']=[]
star_classes['White Dwarf']=[]
star_classes['Neutron Star']=[]
for star in stars_dict:
    sm = stars_dict[star].stellar_mass
    if sm == None or sm < 0.3:
        continue
    elif 0.3<=sm<8:
        star_classes['Red Giant'].append(star)
    elif 8<=sm<10.5:
        star_classes['White Dwarf'].append(star)
    elif 10.5<=sm:
        star_classes['Neutron Star'].append(star)

# You can **verify** that you have defined `star_classes` correctly by checking that there are *3756* Red Giants, *3* White Dwarfs, and *1* Neutron Star in `star_classes`.

# **Question 6:** What is the **average** `stellar_luminosity` of each class of `Star` objects in `star_classes`?
#
# Your output **must** be a **dictionary** mapping the class of the star to the **average** `stellar_luminosity` value of all `Star` objects of that class. You **must** ignore the `Star` objects with **missing** `stellar_luminosity` data.
#
# The expected output of this question is:
#
# ```python
# {'Red Giant': -0.01901339529797699,
#  'White Dwarf': 2.787333333333333,
#  'Neutron Star': 2.86}
# ```

# +
# compute and store the answer in the variable 'star_classes_avg_lum', then display it
star_classes_avg_lum = {}
for star_class in star_classes:
    sl_list = []
    for star in star_classes[star_class]:
        sl = stars_dict[star].stellar_luminosity
        if sl == None:
            continue
        else:
            sl_list.append(sl)
    class_mean = statistics.mean(sl_list)
    star_classes_avg_lum[star_class] = class_mean
star_classes_avg_lum
# TODO: initialize 'star_classes_avg_lum'
# TODO: loop through each 'star_class' in 'star_classes'
    # TODO: loop through each 'star' in the 'star_class'
        # TODO: skip 'star' if 'stellar_luminosity' data is missing
        # TODO: for the remaining stars, compute the mean of the 'stellar_luminosity'
    # TODO: add the mean luminosity to 'star_classes_avg_lum'
    
# TODO: display 'star_classes_avg_lum'
# -

grader.check("q6")

# **Food for thought:** Recall that the `stellar_luminosity` values of the `Star` objects are represented in units of the logarithm of the Sun's luminosity. What does this difference in `stellar_luminosity` signify?

# Just as the different classes of `Star` objects have different **average luminosities**, they also have different **average densities**. This difference will be easier to visualize as a **scatter plot**.
#
# However, before you can do that, there is a minor hurdle you need to overcome - we do **not** have the *stellar density* data available for the `Star` objects in our dataset. However, we do have `stellar_mass` and `stellar_radius` data, which allows us to **compute** the *stellar density*. Since the `stellar_mass` and `stellar_radius` data is stored in units of the Sun's mass and radius respectively, we can compute the *stellar density* (i.e., density of the `Star` in units of the Sun's density) as follows:
#
# $$\texttt{stellar density} = \frac{\texttt{stellar mass}}{(\texttt{stellar radius})^{3}}.$$

# **Question 7:** Create a **scatter plot** representing the *stellar density* (on the **x-axis**) against the `stellar_luminosity` (on the **y-axis**) of each `Star` object of **each class** in `star_classes`.
#
# You **must** ignore all `Star` objects with **missing** `stellar_mass`, `stellar_radius`, or `stellar_luminosity` data.
#
# You **must** first compute two **dictionaries**. The **keys** of both dictionaries must be the different **star classes**, and the corresponding values must be the **list** of **densities** and **list** of **luminosities** of `Star` objects of that **star class**. Then, you **must** use `plot_scatter_multiple` to plot the **density** against the **luminosity** of each **star class**.
#
# **Important Warning:** `p11_test.py` can check that the **dictionaries** are correct, but it **cannot** check if your plot appears on the screen, or whether the axes are correctly labelled. Your plots will be **manually graded**, and you will **lose points** if your plot is not visible, or if it is not properly labelled.
#
# Your plot should look like this:

# <div><img src="attachment:density_luminosity.PNG" width="400"/></div>

# +
# first compute and store the dictionaries 'density_dict', and 'lum_dict'
# then create the scatter plot using the dictionaries
density_dict={}
lum_dict ={}

for star_class in star_classes:
    density_dict[star_class]=[]
    lum_dict[star_class]=[]
    for star in star_classes[star_class]:
        sm = stars_dict[star].stellar_mass
        sr = stars_dict[star].stellar_radius
        sl = stars_dict[star].stellar_luminosity
        if sm == None or sr == None or sl == None:
            continue
        else:
            lum_dict[star_class].append(sl)
            sd =sm/sr**3
            density_dict[star_class].append(sd)

plot_scatter_multiple(density_dict,lum_dict, 'Density','Luminosity')

# TODO: initialize the two dictionaries 'density_dict', and 'lum_dict'
# TODO: loop through each 'star_class' in 'star_classes'
    # TODO: add the 'star_class' to 'density_dict' and 'lum_dict'
    # TODO: loop through each 'star' in the 'star_class'
        # TODO: skip 'star' if mass, radius, or luminosity data is missing
        # TODO: otherwise add the luminosity to the correct key of 'lum_dict'
        # TODO: compute the density and add to the correct key of 'density_dict'
    
# TODO: use the 'plot_scatter_multiple' function to create the plot
# -

grader.check("q7")

# **Food for thought:** As you can see, there are **two** extreme outliers with a very high density. If you are interested, you can try to find out the names of these stars, and why they have such extremely high densities (and low luminosities). What (incorrect) assumption did we make when we classified the `Star` objects in `star_classes`? Can you suggest a more accurate way of classifying the stars now?

# As you can see, almost all the `Star` objects have low *stellar density*, and the presence of a few extreme outliers is obscuring our view of the other `Star` objects. In fact, it turns out that there are only *10* `Star` objects in the dataset with a *stellar density* **greater than** *25*. We could get a much clearer view of the relationship between *stellar density* and `stellar_luminosity` if we did **not** plot these outliers.

# **Question 8:** **Excluding** stars with *stellar density* **greater than** *25*, create a **scatter plot** representing the *stellar density* (on the **x-axis**) against the `stellar_luminosity` (on the **y-axis**) of each `Star` object of **each class** in `star_classes`.
#
# You **must** ignore all `Star` objects with **missing** `stellar_mass`, `stellar_radius`, or `stellar_luminosity` data.
#
# You **must** first compute two **dictionaries**. The **keys** of both dictionaries must be the different **star classes**, and the corresponding values must be the **list** of **densities** and **list** of **luminosities** of `Star` objects of that **star class**. Then, you **must** use `plot_scatter_multiple` to plot the **density** against the **luminosity** of each **star class**.
#
# **Important Warning:** `p11_test.py` can check that the **dictionaries** are correct, but it **cannot** check if your plot appears on the screen, or whether the axes are correctly labelled. Your plots will be **manually graded**, and you will **lose points** if your plot is not visible, or if it is not properly labelled.
#
# Your plot should look like this:

# <div><img src="attachment:density_luminosity_wo_outliers.PNG" width="400"/></div>

# +
# first compute and store the dictionaries 'density_dict_no_outliers', and 'lum_dict_no_outliers'
# then create the scatter plot using the dictionaries
density_dict_no_outliers={}
lum_dict_no_outliers ={}

for star_class in star_classes:
    density_dict_no_outliers[star_class]=[]
    lum_dict_no_outliers[star_class]=[]
    for star in star_classes[star_class]:
        sm = stars_dict[star].stellar_mass
        sr = stars_dict[star].stellar_radius
        sl = stars_dict[star].stellar_luminosity
        if sm == None or sr == None or sl == None:
            continue
        sd =sm/sr**3
        if sd>25:
            continue
        else:
            lum_dict_no_outliers[star_class].append(sl)
            
            density_dict_no_outliers[star_class].append(sd)

plot_scatter_multiple(density_dict_no_outliers,lum_dict_no_outliers, 'Density','Luminosity')
# -

grader.check("q8")

# **Food for thought:** Can you guess the relationship between **density** and **luminosity**? Can you spot the `Star` objects in this graph which will end up as White Dwarfs and Neutron Stars? Do they appear to follow the same relationship as the Red Giants? How do they compare to the outliers you found in q7?

# ### Hertzsprung–Russell Diagram:
#
# The [Hertzsprung–Russell diagram](https://en.wikipedia.org/wiki/Hertzsprung%E2%80%93Russell_diagram) is a scatter plot of stars showing the relationship between the stars' `stellar_luminosity` versus their `stellar_effective_temperature`. The diagram is exceedingly useful for understanding the stellar evolution of stars. We will now use the data we have available to plot this diagram ourselves, so we can better understand stellar evolution.
#
# We want to plot the `stellar_effective_temperature` against the `stellar_luminosity`, but more importantly, we will use the **color** and **size** parameters to represent the `stellar_age` and `stellar_mass` of the `Star` objects as well. This will allow us to see the effects of `stellar_age` and `stellar_mass` on `stellar_effective_temperature` and `stellar_luminosity`.

# **Question 9**: Create a **scatter plot** representing the `stellar_effective_temperature` (on the **x-axis**) against the `stellar_luminosity` (on the **y-axis**) of each `Star` object in `stars_dict`. Moreover, represent the `stellar_age` of each `Star` object using the **color** and represent the `stellar_mass` of each `Star` object using the **size** of the star.
#
# You **must** first compute four **lists** containing the `stellar_effective_temperature`, `stellar_luminosity`, `stellar_age` and the `stellar_mass` of each `Star` object (which has **all** the data available). You **must** ignore any `Star` object which has any of these four attributes **missing**. Then, you **must** use `plot_scatter` to plot the `stellar_effective_temperature` against the `stellar_luminosity` with the `stellar_age` as the **color** and the `stellar_mass` as the **size** of the points.
#
# **Important Warning:** `p11_test.py` can check that the **lists** are correct, but it **cannot** check if your plot appears on the screen, or whether the axes are correctly labelled. Your plots will be **manually graded**, and you will **lose points** if your plot is not visible, or if it is not properly labelled.
#
# Your plot should look like this:

# <div><img src="attachment:hr_diagram.PNG" width="400"/></div>

# first compute and store the lists 'temp_list', 'lum_list', 'age_list', and 'mass_list'
# then create the scatter plot using the lists
temp_list =[]
lum_list=[]
age_list=[]
mass_list=[]
for star in stars_dict:
    st = stars_dict[star].stellar_effective_temperature
    sl = stars_dict[star].stellar_luminosity
    sa = stars_dict[star].stellar_age
    sm = stars_dict[star].stellar_mass
    if st == None or sl == None or sa == None or sm == None:
        continue
    else:
        temp_list.append(st)
        lum_list.append(sl)
        age_list.append(sa)
        mass_list.append(sm)
plot_scatter(temp_list,lum_list,'Effective Temperature','Luminosity',c=age_list,s=mass_list)
print(len(temp_list))

grader.check("q9")


# **Food for thought:** Can you tell if there is any relationship between the **temperature**, **luminosity**, **age**, and **mass** of the stars? You might want to remove the outliers with the extremely high `stellar_effective_temperature` to get a better view of the diagram. What effect does the **age** seem to have on the **temperature**? Recall that a **lighter** color implies that the value is higher, while a **darker** color implies that the value is lower. What effect does the **mass** have on **luminosity** and **temperature**? Are stars of all masses distributed evenly across the plot? Where are the heavier stars concentrated?
#
# **Food for thought:** Notice that there are **two distinct** *clusters* of points in this diagram. If you are interested, look up more information on the Hertzsprung–Russell Diagram to understand what these clusters are. 

# ### Recursion:
#
# You are not done exploring the dataset, and you have more questions left to answer. However, something more important has happened! We have managed to find the data from the corrupted json file (`mapping_5.json`)!
#
# If you will recall, when we were parsing the files in p10, we found that `mapping_5.json` was **broken**, and we couldn't read it. Therefore, we had no choice but to leave all the planets in `planets_5.csv` out of our analysis. Luckily for you now, the data has shown up intact in the directory `broken_data`. Unfortunately, the data is now no longer stored in a single file, but has been **split up** into **multiple files** and stored in **different subdirectories**.
#
# You will now create a function to help parse all the data stored within this directory.

# ### Function 1:  `get_all_paths_in(directory)`
#
# You **must** write this function that takes in the **relative path** of a `directory` as its input, and returns a **list** of **relative paths** of all the **files** inside `directory` and its subdirectories.
#
# In other words, if a directory `small_data` looks like this:
# ```
# +-- sample_data
# |   +-- .DS_Store
# |   +-- file_1.json
# |   +-- sample_1
# |   |   +-- .ipynb_checkpoints
# |   |   +-- file_2.json
# |   |   +-- file_3.json
# |   +-- sample_2
# |   |   +-- file_4.json
# |   |   +-- sample_3
# |   |   |   +-- .DS_Store
# |   |   |   +-- file_5.json
# ```
#
# then the output of the function call `get_all_paths_in("sample_data")` **must** be a **list** containing the **relative paths** of the files `file_1.json`, `files_2.json`, `file_3.json`, `file_4.json`, and `file_5.json`.
#
# You **must** **ignore** all files that start with `"."`, and your output **must** be **explicitly** sorted in **alphabetical** order.
#
# **Important Warning:** You **must** write a **recursive** function here. You are **only allowed** to use the functions from the `os` module, which have been covered in lecture. Here is a list of these functions (you will only need a few of these functions to define `get_all_paths_in`):
# * `os.mkdir`
# * `os.path.join`
# * `os.listdir`
# * `os.path.exists`
# * `os.path.isfile`
# * `os.path.isdir`

# +
# define the function 'get_all_paths_in' here

def get_all_paths_in(directory):
    paths_list = []
    for content in os.listdir(directory):
        if content.startswith('.'):
            continue
        if os.path.isdir(os.path.join(directory,content)):
            x =get_all_paths_in(os.path.join(directory,content))
            paths_list.extend(x)
        else:
            paths_list.append(os.path.join(directory,content))
            
    return sorted(paths_list)
    '''get_all_paths_in(directory) recursively 
    explores that directory for any files, 
    and returns a list of paths to 
    files inside that directory'''
    pass # replace with your code


# -
# **Question 10:** What are the **paths** of the files in the `others` directory of the `broken_data` directory?
#
# Your output **must** be a **list** of **relative paths**. You **must** answer this question by calling the `get_paths_in` function.
#
# **Warning:** Remember that you **must** only use `os.path.join` to create paths.

# compute and store the answer in the variable 'broken_data_others', then display it
broken_data_others = get_all_paths_in(os.path.join('broken_data','others'))
broken_data_others
grader.check("q10")

# **Question 11:** What are the **paths** of the files in the `kepler_100s` directory of the `keplers` directory of the `broken_data` directory?
#
# Your output **must** be a **list** of **relative paths**. You **must** answer this question by calling the `get_all_paths_in` function.
#
# **Hint:** You can pass multiple **strings** as arguments to `os.path.join` to join them together at the same time. For example, to get the path of the required directory here, you could say
# ```python
# os.path.join("broken_data", "keplers", "kepler_100s")
# ```

# compute and store the answer in the variable 'broken_data_keplers_kepler_100s', then display it
broken_data_keplers_kepler_100s= get_all_paths_in(os.path.join('broken_data','keplers','kepler_100s'))
broken_data_keplers_kepler_100s.sort()
broken_data_keplers_kepler_100s
grader.check("q11")

# **Question 12:** What are the **paths** of the files in the `others` directory of the `kepler_10s` directory of the `keplers` directory of the `broken_data` directory?
#
# Your output **must** be a **list** of **relative paths**. You **must** answer this question by calling the `get_all_paths_in` function.

# compute and store the answer in the variable 'broken_data_keplers_kepler_10s_others', then display it
broken_data_keplers_kepler_10s_others= get_all_paths_in(os.path.join('broken_data','keplers','kepler_10s','others'))
broken_data_keplers_kepler_10s_others.sort()
broken_data_keplers_kepler_10s_others
grader.check("q12")

# **Question 13:** What are the **paths** of the files in the `broken_data` directory?
#
# Your output **must** be a **list** of **relative paths**. You **must** answer this question by calling the `get_paths_in` function.

# compute and store the answer in the variable 'broken_data', then display it
broken_data = get_all_paths_in('broken_data')
broken_data.sort()
broken_data
grader.check("q13")

# ### Data Structure 2: `all_planets_list`
#
# We want to read the data that is stored inside the directory `broken_data`. We already have a function `get_planets` (from p10) which can read a CSV file and a JSON file and combine them to create a **list** of `Planet` objects. So, we can repeatedly call `get_planets` on the CSV file `planets_5.csv` and each of the JSON files inside `broken_data` to get a **list** of `Planet` objects of **all** the planets in `planets_5.csv`.
#
# You **must** **create** the **list** `all_planets_list` by adding in all `Planet` objects from `planets_list`, and then also adding in the `Planet` objects in `planets_5.csv` and the directory `broken_data`.
#
# **Hint:** You **must** loop through every file in the list `broken_data`, and use `get_planets` on `planets_5.csv` (inside the `data` directory), and this file (from the loop) to create a list of `Planet` objects, and then **extend** `all_planets_list` by the list of new `Planet` objects.
#
# **Warning:** Do **not** update the value of the **list** `planets_list` when you do this. Otherwise, your answers to some of the previous questions will become incorrect. Instead, make sure that the new `Planet` objects are only added to `all_planets_list` and **not** to `planets_list`.

planet_paths

# create the variable 'all_planets_list' here,
# but do NOT display the variable at the end
all_planets_list = []
all_planets_list.extend(planets_list)
for file in broken_data:
    planet_i = get_planets(planet_paths[4],file)
    all_planets_list.extend(planet_i)
# TODO: initialize 'all_planets_list'
# TODO: add the planets in 'planets_list' to 'all_planets_list'
# TODO: loop through all paths in 'broken_data'
    # TODO: use 'get_planets' to get the planets in this file and add them to 'all_planets_list'

len(all_planets_list)


# You can verify that you have not made any mistakes by confirming that `all_planets_list` now has *5174* `Planet` objects in it.

# ### Exploring habitability of exoplanets:
#
# Now that we have gathered the data on all the `Planet` objects, we are ready to have some fun with this dataset. Over the course of the rest of this project, we will try to find out if there are any planets in our dataset which could potentially support human habitation. Naturally, we cannot say with any certainty that any particular planet is habitable, but we can say with some confidence when a planet is **not** habitable (notwithstanding major technological gains). That is exactly what we will do now.

# #### Surface Gravitational Force:
#
# It seems reasonable to expect that for humans to be able to survive on a planet, the gravitational force of the planet on its surface is not too different from that of the Earth.
#
# We note that this is because the `planet_mass` and `planet_radius` attributes of the `Planet` objects already stores these values in units of the mass of the Earth, and the radius of the Earth respectively. So, the **ratio** of the gravitational force experienced on the surface of a given planet to the force experienced on the surface of the Earth can be computed as:
#
# $$\frac{g_{\texttt{planet}}}{g_{\texttt{earth}}} = \frac{\texttt{planet mass}}{\texttt{planet radius}^{2}}$$
#
# So, a **ratio** greater than 1 would imply that a person on the planet's surface would experience a greater force due to gravity than on Earth, while a value lower than 1 would imply that a person on the planet's surface would experience a lesser force due to gravity than on Earth.

# ### Function 2: `get_surface_gravity(planet)`
#
# You **must** define this function which takes in a `Planet` object as its input, and then **returns** the **ratio** of the gravitational force experienced on the surface of a given planet to the force experienced on the surface of the Earth. If either the `planet_mass` or `planet_radius` data is **missing**, then your function **must** return `None`.

# define the function 'get_surface_gravity' here
def get_surface_gravity(planet):
    pm = planet.planet_mass
    pr = planet.planet_radius
    if pm == None or pr == None:
        return None 
    return pm/pr**2
     


# **Question 14:** What is the **ratio** of gravitational force experienced on the surface of the planet *GJ 674 b* to the gravitational force experienced on the surface of the Earth?
#
# **Hint:** You will have to first loop through `all_planets_list` to identify the correct `Planet` object. Remember to `break` out of your loop after you identify the correct `Planet` object.

# compute and store the answer in the variable 'gj_674_b_gravity', then display it
for planet in all_planets_list:
    if planet.planet_name == 'GJ 674 b':
        gj_674_b = planet
        break
gj_674_b_gravity = get_surface_gravity(gj_674_b)
gj_674_b_gravity


grader.check("q14")


# #### Distance to the star:
#
# Planets follow **elliptical** orbits around their host star. The `eccentricity` of a planet's orbit is a number that measures *how* elliptical the orbit is. An eccentricity of *0* would imply that the orbit is in fact perfectly circular, while an eccentricity close to *1* would imply that the orbit is very skewed and elliptical. As you may expect, if a planet has a highly eccentric orbit, its distance to its host star would vary wildly, leading to a highly variable climate. To determine if a planet could support human habitation, it is therefore important to know the closest and shortest distances between the planet and its host star.
#
# We can compute these quantities using the attributes `eccentricity` and `semi_major_radius` of each `Planet` object. These distances can be computed as:
#
# $$\texttt{shortest distance} = \texttt{semi major radius} \times (1 - \texttt{abs}(\texttt{eccentricity}))$$
#
# $$\texttt{longest distance} = \texttt{semi major radius} \times (1 + \texttt{abs}(\texttt{eccentricity}))$$

# ### Function 3: `get_distances_to_star(planet)`
#
# You **must** define this function which takes in a `Planet` object as its input, and then **returns** a **list** of two **floats**. The first float should be the **shortest distance** of the `Planet` object to its host star, and the second float should be the **longest distance** to its host star. If either the `eccentricity` or `semi_major_radius` data of the `Planet` is missing, then the function **must** return `None`.

# define the function 'get_distances_to_star' here
def get_distances_to_star(planet):
    distance_list = []
    e = planet.eccentricity
    smr = planet.semi_major_radius
    if e == None or smr == None:
        return None
    else:
        short = smr*(1-abs(e))
        long = smr*(1+abs(e))
        distance_list.append(short)
        distance_list.append(long)
    return distance_list
    


# **Question 15:** Find the **shortest** and **longest** distances for the planet *b Cen AB b* to its host star.
#
# Your output **must** be a **list** of two **floats** representing the **shortest** and **longest** distances to its host star.

# compute and store the answer in the variable 'distances_to_star_b_cen_ab_b', then display it
for planet in all_planets_list:
    if planet.planet_name == 'b Cen AB b':
        b_cen_ab_b = planet
        break
distances_to_star_b_cen_ab_b = get_distances_to_star(b_cen_ab_b)
distances_to_star_b_cen_ab_b


grader.check("q15")


# #### Presence of Liquid Water :
#
# It is safe to say that planets which cannot sustain liquid are inhabitable. While we do not have any data on whether the `Planet` objects in our dataset have naturally occurring water, we are able to determine whether the planet can *support* liquid water based on its distance to its host star, and the luminosity of this star. 
#
# Astronomers have [computed](https://pubmed.ncbi.nlm.nih.gov/11536936/) that for Earth-like planets, there is a certain range of distances that a planet can have to its host star, which depends on the `luminosity` of the star, within which, water on the planet's surface can stay in liquid form. These distances are as follows:
#
# $$\texttt{liquid water shortest dist} = \sqrt{\frac{\texttt{absolute luminosity}}{1.15}}$$
#
# $$\texttt{liquid water longest dist} = \sqrt{\frac{\texttt{absolute luminosity}}{0.53}}$$
#
# In our dataset, the `stellar_luminosity` is stored in units of the logarithm of the absolute luminosity. So, the distances can be computed from our dataset as follows:
#
# $$\texttt{liquid water shortest dist} = \sqrt{\frac{10^{\texttt{stellar luminosity}}}{1.15}}$$
#
# $$\texttt{liquid water longest dist} = \sqrt{\frac{10^{\texttt{stellar luminosity}}}{0.53}}$$

# ### Function 4: `get_liquid_water_distances(planet)`
#
# You **must** define this function which takes in a `Planet` object as its input, and then **returns** a **list** of two **floats**. The first float should be the **shortest distance** the `Planet` object can be to its host star while being able to support liquid water, and the second float should be the **longest distance** it can be to its host star while being able to support liquid water. If the `stellar_luminosity` data of the host `Star` object is missing, then the function **must** return `None`.

# +
# define the function 'get_liquid_water_distances' here
def get_liquid_water_distances(planet):
    water_list = []
    star_name = planet.host_name
    star = stars_dict[star_name]
    sl = star.stellar_luminosity
    if sl == None:
        return None
    short = math.sqrt(10**sl/1.15)
    long = math.sqrt(10**sl/0.53)
    water_list.append(short)
    water_list.append(long)
    return water_list
    
  
# -

# **Question 16:** Find the **shortest** and **longest** distances for the planet *Kepler-197 e* from its host star, at which it can support liquid water.
#
# Your output **must** be a **list** of two **floats** representing the **shortest** and **longest** distances that the planet can be from its host star and still support liquid water.

# +
# compute and store the answer in the variable 'liquid_water_distances_kepler_197_e', then display it
for planet in all_planets_list:
    if planet.planet_name == 'Kepler-197 e':
        kepler_197_e = planet
        break

liquid_water_distances_kepler_197_e = get_liquid_water_distances(kepler_197_e)
liquid_water_distances_kepler_197_e
# -

grader.check("q16")

# **Question 17:** **List** the `planet_name` of all the `Planet` objects which can support liquid water when they are at **both** their **shortest** and **longest** distances to their host star.
#
# Your output **must** be a **list**. You **must** ignore `Planet` objects with missing `eccentricity`, or `semi_major_radius` data and planets whose host `Star` has missing `stellar_luminosity` data.
#
# **Hint:** You can find the actual shortest and longest distances of the planet with the `get_distances_to_star` function, and the shortest and longest distances at which liquid water can be supported with the `get_liquid_water_distances` function. You must consider `Planet` objects for which the actual distances to their host star lie **within** the distances at which liquid water can be supported.

# compute and store the answer in the variable 'planets_with_liquid_water', then display it
planets_with_liquid_water = []
for planet in all_planets_list:
    distance = get_distances_to_star(planet)
    water = get_liquid_water_distances(planet)
    if distance ==None or water == None:
        continue
    if water[0]<distance[0]<water[1] and water[0]<distance[1]<water[1]:
        planets_with_liquid_water.append(planet.planet_name)
planets_with_liquid_water


grader.check("q17")


# #### Surface temperature:
#
# The temperature on the surface of the planet is another important criteria for deciding whether a planet is habitable. The `equilibrium_temperature` of a `Planet` is the temperature that the planet if it were a [black body](https://en.wikipedia.org/wiki/Black_body), i.e., if it were able to absorb all the radiation it receives from its host star. However, most planets are not perfect black bodies and reflect some of the radiation that they receive from their host star. Astronomers use the quantity [albedo](https://en.wikipedia.org/wiki/Albedo) to measure how much radiation is reflected by the planet. An albedo of *0* implies that the planet is a perfect black body which absorbs all its radiation, while an albedo of *1* implies that the planet is perfectly reflective, and does not retain any radiation. In the real world, most planets have an albedo value between *0* and *0.5*.
#
# Using the albedo of a planet, we can compute the temperature on the surface of a planet as follows
#
# $$ \texttt{surface temperature} = \left(1- \texttt{albedo}\right) ^{1/4} \times \texttt{equilibrium temperature}$$
#
# Unfortunately, we do **not** have the albedo values of the `Planet` objects in our dataset. So, we will instead make some educated guesses and find the **maximum** and **minimum** surface temperatures, assuming that the albedo is within the range of *0* to *0.5* (which is known to be the case for most planets).

# ### Function 5: `get_surface_temperatures(planet)`
#
# You **must** define this function which takes in a `Planet` object as its input, and then **returns** a **list** of two **floats**. The first float should be the **minimum surface temperature** of the `Planet` object (which can be computed by assuming a **albedo** value of *0.5*), and the second float should be the **maximum surface temperature** (which can be computed by assuming a **albedo** value of *0.0*). If the `equilibrium_temperature` data of the `Planet` is missing, then the function **must** return `None`.

# define the function 'get_surface_temperatures' here
def get_surface_temperatures(planet):
    temp_list = []
    eq = planet.equilibrium_temperature
    if eq == None:
        return None
    min_temp = (1-0.5)**0.25*eq
    max_temp = (1-0)**0.25*eq
    temp_list.append(min_temp)
    temp_list.append(max_temp)
    return temp_list


# **Question 18:** Find the **minimum** and **maximum** surface temperatures for the planet *HD 20794 d*.
#
# Your output **must** be a **list** of two **floats** representing the **minimum** and **maximum** surface temperatures.

# compute and store the answer in the variable 'surface_temp_hd_20794_d', then display it
for planet in all_planets_list:
    if planet.planet_name == 'HD 20794 d':
        hd_20794_d = planet
surface_temp_hd_20794_d = get_surface_temperatures(hd_20794_d)
surface_temp_hd_20794_d   
    

grader.check("q18")

# **Question 19:** **List** the `planet_name` of all the `Planet` objects whose **minimum surface temperature** is **greater** than *263* (Kelvin) and **maximum surface temperature** is **less** than *323* (Kelvin).
#
# Your output **must** be a **list**. You **must** ignore `Planet` objects with missing `equilibrium_temperature` data.

# compute and store the answer in the variable 'pleasant_planets', then display it
pleasant_planets = []
for planet in all_planets_list:
    surface_temp = get_surface_temperatures(planet)
    if surface_temp == None:
        continue
    if surface_temp[0]>263 and surface_temp[1]<323:
        pleasant_planets.append(planet.planet_name)
pleasant_planets

grader.check("q19")

# #### Putting it all together:
#
# We are finally ready to combine all our various criteria of habitability to make a list of planets which satisfy all the criteria above, and could potentially be habitable. Unsurprisingly, if we are too strict with our expectations, no planets in the dataset will meet them. So, allowing for some technological improvements in the future, we will make more modest requests of the planets in our dataset.

# **Question 20:** List the `planet_name` of all the `Planet` objects which satisfy the criteria below:
#
# 1. The gravitational force experienced on the surface of the `Planet` must be **greater** than *0.75* and **less** than *1.25* times that of the Earth.
# 2. The planet must always **lie within** the range at which it is able to support liquid water.
# 3. The **minimum** surface temperature must be **greater** than *200* and the **maximum** surface temperature must be **less** than *350*.
#
# Your output **must** be a **list** of **strings**. You **must** ignore any `Planet` objects for which you cannot determine if any of these criteria are met.

# +
# compute and store the answer in the variable 'habitable_planets', then display it
habitable_planets=[]
for planet in all_planets_list:
    gravitational_force = get_surface_gravity(planet)
    liquid_water = get_liquid_water_distances(planet)
    distance_to_star = get_distances_to_star(planet)
    surface_temp = get_surface_temperatures(planet)
    if gravitational_force == None or liquid_water == None or distance_to_star == None or surface_temp == None:
        continue 
    elif 0.75< gravitational_force<1.25 and surface_temp[0]>200 and surface_temp[1]<350 \
    and liquid_water[0]<distance_to_star[0]<liquid_water[1] and liquid_water[0]<distance_to_star[1]<liquid_water[1]:
        habitable_planets.append(planet.planet_name)

habitable_planets
# -

grader.check("q20")

# **Food for thought:** If you are interested, you can play around these values more, and introduce more stringent requirements to try and find the single **most** habitable planet.

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

# running this cell will create a new save checkpoint for your notebook
from IPython.display import display, Javascript
display(Javascript('IPython.notebook.save_checkpoint();'))

# !jupytext --to py p11.ipynb

p11_test.check_file_size("p11.ipynb")
grader.export(pdf=False, run_tests=True, files=[py_filename])

#  
