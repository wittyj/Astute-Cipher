import streamlit as st
from utils import request

# Title
st.title("Astute Cipher")

st.markdown("## Text Encryption and Decryption")

text = st.text_area("Enter text to encrypt or decrypt", height=200)

algorithm = st.selectbox("Select algorithm", ("Caesar", "CRot13", "Rot13", "Atbash"))

if algorithm == "Astute":
    shift = st.number_input("Enter shift value", min_value=1, value=3)
    action = st.radio("Action", ("Encrypt", "Decrypt"))
    action = action.lower()
    if st.button("Submit"):
        st.markdown("### Output")
        st.write(request('astute', text, shift, action))

if algorithm == "CRot13":
    shift = st.number_input("Enter shift value", min_value=1, value=3)
    action = st.radio("Action", ("Encrypt", "Decrypt"))
    action = action.lower()
    if st.button("Submit"):
        st.markdown("### Output")
        st.write(request('crot13', text, shift, action))

if algorithm == "Rot13":
    if st.button("Submit"):
        st.markdown("### Output")
        st.write(request('rot13', text))

if algorithm == "Atbash":
    if st.button("Submit"):
        st.markdown("### Output")
        st.write(request('atbash', text))
