import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
# streamlit.dataframe(my_fruit_list)
# show fruit selection
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice): 
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

try:
    #fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi') -- preloaded with Kiwi
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice: streamlit.error('Please select a fruit to get information')
    else: 
      fruit_data = get_fruityvice_data(fruit_choice)
      streamlit.dataframe(fruit_data)
except URLError as e:
      streamlit.error()
  
#don't run anything past this point while we troubleshoot 
streamlit.stop()
               
#test snowflake connection
streamlit.text("Hello from Snowflake!")
my_cnx = snowflake.connector.connect(**streamlit.secrets['snowflake'])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text(my_data_row)

#retrieve fruit list
my_cur.execute("select Fruit_Name from pc_rivery_db.public.fruit_load_list order by Fruit_Name")
#my_data_row = my_cur.fetchone() -- read the first row
my_data_row = my_cur.fetchall()

streamlit.header("The fruit list contains:")
streamlit.dataframe(my_data_row)

add_fruit = streamlit.text_input('What fruit would you like information about?','Jackfruit')
streamlit.write('The user entered ', add_fruit)

my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('from streamlit')")
