import streamlit as st
import pandas as pd
from datetime import datetime


# Page configuration
st.set_page_config(page_title="Hotel Management Dashboard", layout="wide", page_icon="🏨")

# Application Title
st.title("🏨 Hotel Management Dashboard")
st.markdown("---")

# 1. MOCK DATA (डैशबोर्ड को लाइव दिखाने के लिए डमी डेटा)
if 'rooms' not in st.session_state:
    st.session_state.rooms = pd.DataFrame([
        {"Room No": "101", "Type": "Single", "Price ($)": 100, "Status": "Occupied"},
        {"Room No": "102", "Type": "Double", "Price ($)": 150, "Status": "Available"},
        {"Room No": "201", "Type": "Suite", "Price ($)": 300, "Status": "Available"},
        {"Room No": "202", "Type": "Deluxe", "Price ($)": 200, "Status": "Maintenance"}
    ])

if 'customers' not in st.session_state:
    st.session_state.customers = pd.DataFrame([
        {"Customer ID": "C001", "Name": "Amit Sharma", "Email": "amit@email.com", "Phone": "9876543210"},
        {"Customer ID": "C002", "Name": "Priya Patel", "Email": "priya@email.com", "Phone": "8765432109"}
    ])

if 'bookings' not in st.session_state:
    st.session_state.bookings = pd.DataFrame([
        {"Booking ID": "B501", "Customer Name": "Amit Sharma", "Room No": "101", "Check-in": "2026-10-25", "Check-out": "2026-10-28"}
    ])

# 2. TOP METRICS (मुख्य आंकड़े)
total_rooms = len(st.session_state.rooms)
available_rooms = len(st.session_state.rooms[st.session_state.rooms["Status"] == "Available"])
total_customers = len(st.session_state.customers)
total_bookings = len(st.session_state.bookings)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Rooms", total_rooms, "🏨")
with col2:
    st.metric("Available Rooms", available_rooms, "🟢")
with col3:
    st.metric("Registered Customers", total_customers, "👥")
with col4:
    st.metric("Total Bookings", total_bookings, "📅")

st.markdown("---")

# 3. SIDEBAR - NEW ACTIONS (नया डेटा जोड़ने के लिए फॉर्म)
st.sidebar.header("⚙️ Management Console")
action = st.sidebar.selectbox("Choose Action", ["View Dashboard", "Add Room", "Add Customer", "Create Booking"])

# --- ACTION: ADD ROOM ---
if action == "Add Room":
    st.subheader("➕ Add New Room")
    with st.form("room_form"):
        r_no = st.text_input("Room Number")
        r_type = st.selectbox("Room Type", ["Single", "Double", "Suite", "Deluxe"])
        r_price = st.number_input("Price per Night ($)", min_value=10)
        r_status = st.selectbox("Initial Status", ["Available", "Occupied", "Maintenance"])
        
        if st.form_submit_button("Save Room"):
            new_room = {"Room No": r_no, "Type": r_type, "Price ($)": r_price, "Status": r_status}
            st.session_state.rooms = pd.concat([st.session_state.rooms, pd.DataFrame([new_room])], ignore_index=True)
            st.success(f"Room {r_no} added successfully!")

# --- ACTION: ADD CUSTOMER ---
elif action == "Add Customer":
    st.subheader("➕ Register New Customer")
    with st.form("customer_form"):
        c_id = f"C00{len(st.session_state.customers) + 1}"
        c_name = st.text_input("Customer Name")
        c_email = st.text_input("Email Address")
        c_phone = st.text_input("Phone Number")
        
        if st.form_submit_button("Register"):
            new_cust = {"Customer ID": c_id, "Name": c_name, "Email": c_email, "Phone": c_phone}
            st.session_state.customers = pd.concat([st.session_state.customers, pd.DataFrame([new_cust])], ignore_index=True)
            st.success(f"Customer {c_name} registered successfully with ID: {c_id}")

# --- ACTION: CREATE BOOKING ---
elif action == "Create Booking":
    st.subheader("📅 Create New Booking")
    available_r_list = st.session_state.rooms[st.session_state.rooms["Status"] == "Available"]["Room No"].tolist()
    cust_list = st.session_state.customers["Name"].tolist()
    
    if not available_r_list:
        st.warning("No rooms available for booking right now.")
    elif not cust_list:
        st.warning("Please register a customer first.")
    else:
        with st.form("booking_form"):
            b_id = f"B50{len(st.session_state.bookings) + 1}"
            b_cust = st.selectbox("Select Customer", cust_list)
            b_room = st.selectbox("Select Room", available_r_list)
            b_in = st.date_input("Check-in Date")
            b_out = st.date_input("Check-out Date")
            
            if st.form_submit_button("Confirm Booking"):
                # Add booking record
                new_book = {"Booking ID": b_id, "Customer Name": b_cust, "Room No": b_room, "Check-in": str(b_in), "Check-out": str(b_out)}
                st.session_state.bookings = pd.concat([st.session_state.bookings, pd.DataFrame([new_book])], ignore_index=True)
                
                # Update room status to Occupied
                st.session_state.rooms.loc[st.session_state.rooms["Room No"] == b_room, "Status"] = "Occupied"
                st.success(f"Booking {b_id} confirmed for Room {b_room}!")

# --- DEFAULT VIEW: DASHBOARD TABS ---
if action == "View Dashboard":
    tab1, tab2, tab3 = st.tabs(["🔑 Rooms Directory", "👥 Customer Directory", "📖 Bookings Ledger"])
    
    with tab1:
        st.subheader("Live Room Status")
        st.dataframe(st.session_state.rooms, use_container_width=True)
        
    with tab2:
        st.subheader("Registered Customers List")
        st.dataframe(st.session_state.customers, use_container_width=True)
        
    with tab3:
        st.subheader("Active Bookings Log")
        st.dataframe(st.session_state.bookings, use_container_width=True)
