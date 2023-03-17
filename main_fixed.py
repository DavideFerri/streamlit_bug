import streamlit as st
import requests
import json
from copy import deepcopy
import time
from typing import Literal

def app():
    st.title('Scenarios')

    # ----------------------------- LOAD EXISTING SCENARIO ---------------------------------- #

    st.markdown(
        "### Top-down expectations ###  \n"
    )

    # ----------------------------- SET RATES ----------------------------- #

    st.markdown("  \n"
                "  \n"
                "**Expected pace of cash flows**  \n")
    if 'rates' not in st.session_state:
        st.session_state['rates'] = {}
    rates = st.session_state['rates'] if 'rates' in st.session_state else {}
    cols = st.columns((2, 2))
    with cols[0]:
        options = ['fast', 'slow']
        default = options.index(rates['cash flow speed']) if 'cash flow speed' in rates else 0
        st.radio(label='cash flow speed',
                 options=['fast', 'slow'],
                 index=default,
                 key='cash_flow_speed',
                 on_change=update_cash_flow_speed,
                 args=('cash_flow_speed',)
                 )

    with st.expander('rate', expanded=False):
        rate_name = st.selectbox("Select rate name", options=['calls', 'dist', 'loss'], key='rate_name')
        default = rates[rate_name] if rate_name in rates else 0
        with st.form('Add'):
            st.slider(f"Expected {rate_name}",
                      min_value=float(-1 * 100),
                      max_value=float(1 * 100),
                      key=rate_name,
                      step=1.0, value=default * 100.0,
                      format="%.1f%%")
            submit = st.form_submit_button('Submit', on_click=update_rate, args=('rate_name',))
        if submit:
            placeholder = st.empty()
            try:
                placeholder.success('Override submitted successfully')
            except Exception as e:
                placeholder.error(e)
            finally:
                time.sleep(1)
                placeholder.empty()

    st.write(st.session_state['rates'])


def update_cash_flow_speed(component_key):
    value = st.session_state[component_key]
    st.session_state['rates']['cash_flow_speed'] = value
    return None


def update_rate(component_key):
    rate_name = st.session_state[component_key]
    print(rate_name)
    print(st.session_state)
    value = st.session_state[rate_name] / 100
    st.session_state['rates'][rate_name] = value
    return None

if __name__ == '__main__':
    app()
