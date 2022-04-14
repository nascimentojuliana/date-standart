import re
import io
import os
import streamlit as st
from date.online.predict import predict


st.image('image.jpg')

original_title = '<p style="font-family:Courier; color:Black; font-size: 30px;">*DATE STANDART*</p>'
st.markdown(original_title, unsafe_allow_html=True)   

date = st.text_input('Input date')

if st.button('Finish'):

    result = predict(date)

    st.write('The standart date is:', result)