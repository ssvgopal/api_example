import streamlit as st
import requests
from html import escape

st.title("Calculator App")
st.write("This app connects to a FastAPI calculator service.")

# Define the API base URL
api_url = "http://127.0.0.1:9321"

# Initialize session state to store the calculator display and current operation
if 'display' not in st.session_state:
    st.session_state.display = '0'
if 'first_number' not in st.session_state:
    st.session_state.first_number = None
if 'operation' not in st.session_state:
    st.session_state.operation = None
if 'expecting_second_number' not in st.session_state:
    st.session_state.expecting_second_number = False
if 'result' not in st.session_state:
    st.session_state.result = None
if 'api_response' not in st.session_state:
    st.session_state.api_response = None

st.markdown(
    """
    <style>
    .calculator-display {
        background: #f0f2f6;
        border: 1px solid #d9dee8;
        border-radius: 6px;
        min-height: 42px;
        padding: 10px 12px;
        font-size: 16px;
        line-height: 20px;
        color: #31333f;
    }
    .calculator-label {
        color: #808495;
        font-size: 14px;
        margin-bottom: 6px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
display_placeholder = st.empty()

# Function to handle number button clicks
def number_click(number):
    if st.session_state.expecting_second_number:
        st.session_state.display = str(number)
        st.session_state.expecting_second_number = False
    elif st.session_state.display == '0':
        st.session_state.display = str(number)
    else:
        st.session_state.display += str(number)

# Function to handle operation button clicks
def operation_click(op):
    st.session_state.first_number = float(st.session_state.display)
    st.session_state.operation = op
    st.session_state.expecting_second_number = True

# Function to clear the calculator
def clear_calculator():
    st.session_state.display = '0'
    st.session_state.first_number = None
    st.session_state.operation = None
    st.session_state.expecting_second_number = False
    st.session_state.result = None
    st.session_state.api_response = None

# Function to calculate result by calling the API
def calculate_result():
    try:
        if st.session_state.first_number is None or st.session_state.operation is None:
            return

        first_num = st.session_state.first_number
        second_num = float(st.session_state.display)

        # Construct the API request URL based on the selected operation
        endpoint = f"{api_url}/{st.session_state.operation}"

        # Make the API call
        # response = requests.get(endpoint, params={"a": first_num, "b": second_num})
        response = requests.post(endpoint, json={"a": first_num, "b": second_num}, timeout=10)

        # Check if the request was successful
        if response.status_code == 200:
            result = response.json()
            st.session_state.result = result['result']
            st.session_state.api_response = result
            st.session_state.display = str(result['result'])
        else:
            st.session_state.display = f"Error: {response.status_code}"

    except requests.exceptions.ConnectionError:
        st.session_state.display = "Connection Error"
    except Exception as e:
        st.session_state.display = f"Error: {str(e)[:10]}"

# Create the calculator layout with CSS Grid-like appearance
col1, col2, col3, col4 = st.columns(4)

# Row 1 of the calculator (7, 8, 9, +)
with col1:
    if st.button("7", key="num_7", use_container_width=True):
        number_click(7)
with col2:
    if st.button("8", key="num_8", use_container_width=True):
        number_click(8)
with col3:
    if st.button("9", key="num_9", use_container_width=True):
        number_click(9)
with col4:
    if st.button("Add (+)", key="op_add", use_container_width=True):
        operation_click("add")

# Row 2 of the calculator (4, 5, 6, -)
with col1:
    if st.button("4", key="num_4", use_container_width=True):
        number_click(4)
with col2:
    if st.button("5", key="num_5", use_container_width=True):
        number_click(5)
with col3:
    if st.button("6", key="num_6", use_container_width=True):
        number_click(6)
with col4:
    if st.button("Sub (-)", key="op_subtract", use_container_width=True):
        operation_click("subtract")

# Row 3 of the calculator (1, 2, 3, C)
with col1:
    if st.button("1", key="num_1", use_container_width=True):
        number_click(1)
with col2:
    if st.button("2", key="num_2", use_container_width=True):
        number_click(2)
with col3:
    if st.button("3", key="num_3", use_container_width=True):
        number_click(3)
with col4:
    if st.button("C", key="clear", use_container_width=True):
        clear_calculator()

# Row 4 of the calculator (0, ., =)
with col1:
    if st.button("0", key="num_0", use_container_width=True):
        number_click(0)
with col2:
    if st.button(".", key="decimal", use_container_width=True) and '.' not in st.session_state.display:
        st.session_state.display += '.'
with col3:
    if st.button("=", key="equals_button", use_container_width=True):
        calculate_result()

display_placeholder.markdown(
    f"""
    <div class="calculator-label">Calculator Display</div>
    <div class="calculator-display">{escape(st.session_state.display)}</div>
    """,
    unsafe_allow_html=True,
)

# Display API response if available
if st.session_state.api_response:
    with st.expander("View API Response"):
        st.json(st.session_state.api_response)

# Add information about how to run the FastAPI server
st.markdown("---")
st.subheader("How to use this calculator")
st.markdown("""
1. Make sure the FastAPI calculator service is running at http://127.0.0.1:9321
2. Use the calculator buttons to input numbers and operations
3. Click "=" to calculate the result by calling the API
4. Click "C" to clear the calculator
""")

# Run with: streamlit run streamlit_calculator.py
