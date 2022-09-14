
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Medhu Vada with sambar')
streamlit.text('Scrabled eggs and toast with some hashbrowns')  
streamlit.text('Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = streamlit.multiselect("Pick Some Fruits:", list(my_fruit_list.index), ['Avocado', 'Watermelon'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

# New section to display fruityvice api response
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
   
streamlit.header('Fruityvice Fruit Advice!')
try:
   #fruit_choice = streamlit.text_input('What fruit would you like information about?', 'Kiwi')
   fruit_choice = streamlit.text_input('What fruit would you like information about?')
   if not fruit_choice:
      streamlit.error("Please select a fruit to get information.")
   else:
      ### fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
      ### fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      back_from_function = get_fruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)     
except URLError as e: 
  streamlit.error()
    
streamlit.write('The user entered', fruit_choice)

## fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# streamlit.text(fruityvice_response.json()) # just writes the data to the screen

# take the json version of the response and narmalize it.
##fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

# output it to the screen as a table
## streamlit.dataframe(fruityvice_normalized)

### streamlit.stop()

# Connecting to snowflake
## my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
## my_cur = my_cnx.cursor()
# my_cur.execute("SELECT current_user(), current_account(), current_region()")
## my_cur.execute("select * from fruit_load_list")
## my_data_row = my_cur.fetchall()

streamlit.header("The fruit load list contains:")
#Snowflake related functions...
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()
  
# Add abutton to load the fruit
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_row = get_fruit_load_list()
    streamlit.dataframe(my_data_row)

### streamlit.stop() 

# Allow the ednd user to add a fruit to the list...
def insert_row_snowflake(new_fruit):
    with my_cnx.curesor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('"+ new_fruit +"')")
        return "Thanks for adding " + new_fruit
        
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a fruit to the list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)

