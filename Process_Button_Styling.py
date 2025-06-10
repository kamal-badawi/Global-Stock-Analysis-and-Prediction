# Process-Button Style
import streamlit as st


def run_process_button_style():
    process_button_style = """
        <style>
        .stButton > 
        button {
        width: 100% !important;
        color: black   !important;
        background-color:   #D3D3D3 !important;
        border-color: #D3D3D3 !important;
        font-weight: bolder !important;
        border-style: solid !important;
        border-width: 2px !important;
        border-radius: 0% !important;
        }
        /*Button underline nach rechts*/
        button::after {
        color: #009999    !important;
        position: absolute!important;
        content: ''!important;
        height: 2px!important;
        bottom: 0!important;
        left: 50%!important;
        width: 0!important;
        transition: all .3s linear!important;
      }

        button:hover::after {
        background-color: #009999 !important;
        width: 50%!important;
      }
        /*Button HOVER Underline nach links*/
        button::before {
        color: #009999    !important;
        position: absolute!important;
        content: ''!important;
        height: 2px!important;
        bottom: 0!important;
        right: 50%!important;
        width: 0!important;
        transition: all .3s linear!important;
      }

        button:hover::before {
        background-color: #009999 !important;
        width: 50%!important;
      }
        </style>
        """
    # Css-Style auf Process Button anwenden
    st.markdown(process_button_style,
                unsafe_allow_html=True)