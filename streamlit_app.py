# Import python packages
import streamlit as st
import requests
import pandas as pd

from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in Smoothie!
    """
)





name_on_order = st.text_input("Name on smoothies")
st.write("The name on smooties will be:", name_on_order)

#session = get_active_session()
cnx=st.connection("snowflake")
session=cnx.session()


my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

# convert to panda
pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredient_list = st.multiselect('Choose upto 5 ingrdients:',my_dataframe, max_selections=5)

if ingredient_list:
    #st.write(ingredient_list)
    ingredients_string=''
    for fruit_chosen in ingredient_list:
        ingredients_string += fruit_chosen + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
    #st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
            values ('""" + ingredients_string + """', '"""+name_on_order+"""')"""
    time_to_insert = st.button("Submit")
    st.write(my_insert_stmt)
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")



smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
##st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)


