
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healty Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruit_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruit_selected]
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
    fruityvice_response  = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalize = pandas.json_normalize(fruityvice_response.json())
    fruityvice_normalize = fruityvice_normalize.set_index('name')
    return fruityvice_normalize

streamlit.header('Fruityvice Fruit Advice!')
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)
except URLError as e:
    streamlit.error()
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_cur = my_cnx.cursor()
    my_cur.execute("SELECT * FROM fruit_load_list")
    my_data_row = my_cur.fetchall()
    streamlit.header("The fruit load list contains:")
    streamlit.dataframe(my_data_row)

    add_my_fruit = streamlit.text_input('What fruit would you like to add?', 'Jackfruit')
    my_cur.execute(
        "INSERT INTO PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST (FRUIT_NAME) "
        "VALUES (%s)", (
            add_my_fruit
        ))
    streamlit.write('Thanks for adding', add_my_fruit)
    my_cur.execute("SELECT * FROM fruit_load_list")
    my_data_row = my_cur.fetchall()
    streamlit.header("The fruit load list contains:")
    streamlit.dataframe(my_data_row)