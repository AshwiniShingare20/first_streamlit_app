import streamlit
import pandas
import requests 
import snowflake.connector
from urllib.error import URLError

streamlit.title("My Mom's New Healthy diner")
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 and Bleuberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list= pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list= my_fruit_list.set_index("Fruit")

#Let's put a pick list here so they can pick the fruit they want to include
fruits_selected=streamlit.multiselect("Pick some fruits :", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#display the table on the page
#streamlit.dataframe(my_fruit_list)
streamlit.dataframe(fruits_to_show)

#New action to display fruityvice API response 
# add a function

def get_fruityvicedata(this_fruit_choice):
  streamlit.write('The user entered', fruit_choice)
  fruityvoice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)
    #streamlit.text(fruityvoice_response.json()) #just writes data to the screen
    #take the json version of the response and normalize it
  fruityvice_normalized = pandas.json_normalize(fruityvoice_response.json())
  return fruityvice_normalized


streamlit.header('Fruityvice Fruit Advice')
try: 
  fruit_choice = streamlit.text_input('What Fruit would you like informtion about ? ')
  if not fruit_choice:
    streamlit.error('please select a fruit to get information ')
  else:
    back_from_function = get_fruityvicedata(fruit_choice)
    #output it the screen as a table
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()


#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")

streamlit.header("The fruit load list contains")
def get_fruitloadlist():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()

  # add a button
 # streamlit.button('get fruit load list')
  if streamlit.button('get fruit load list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruitloadlist()
    streamlit.dataframe(my_data_rows)
    
  # dont run anything past here while we troubleshoot
streamlit.stop()  
    
#Allow user to add a fruit in the list
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('from streamlit')")
    return "Thanks for adding " + new_fruit
 
fruit_to_add = streamlit.text_input('What Fruit would you like to add ? ')
if streamlit.button ('Add a fruit to the list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(fruit_to_add)
  streamlit.text(back_from_function)

#this will not work correctly , but you have to go for it
my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('from streamlit');")
