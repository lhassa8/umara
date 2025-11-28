"""Comprehensive test for Data Display components"""
import umara as um

um.set_page_config(page_title="Data Display Test", layout="wide")

um.title("Data Display Components Test")

# Sample data
sample_data = [
    {"name": "Alice", "age": 28, "city": "New York", "salary": 75000},
    {"name": "Bob", "age": 34, "city": "San Francisco", "salary": 95000},
    {"name": "Charlie", "age": 45, "city": "Chicago", "salary": 120000},
    {"name": "Diana", "age": 29, "city": "Boston", "salary": 82000},
    {"name": "Eve", "age": 31, "city": "Seattle", "salary": 105000},
]

# dataframe()
um.subheader("1. dataframe()")
um.dataframe(sample_data)

um.divider()

# table()
um.subheader("2. table()")
um.table(sample_data)

um.divider()

# metric()
um.subheader("3. metric()")
with um.columns(3):
    with um.column():
        um.metric("Total Users", "1,234", delta="+12%")
    with um.column():
        um.metric("Revenue", "$45,678", delta="+5.2%")
    with um.column():
        um.metric("Bounce Rate", "32%", delta="-2%", delta_color="inverse")

um.divider()

# stat_card()
um.subheader("4. stat_card()")
with um.columns(3):
    with um.column():
        um.stat_card("Active Users", "2,847", icon="users", trend="+15%", delta_type="positive")
    with um.column():
        um.stat_card("Revenue", "$125K", icon="dollar", trend="+8%", delta_type="positive")
    with um.column():
        um.stat_card("Issues", "23", icon="alert", trend="-5%", delta_type="negative")

um.divider()

# json_viewer() / json()
um.subheader("5. json_viewer() / json()")
sample_json = {
    "name": "Umara",
    "version": "0.3.0",
    "features": ["components", "themes", "state"],
    "config": {
        "debug": True,
        "port": 8501
    }
}
um.json_viewer(sample_json)

um.divider()

# progress()
um.subheader("6. progress()")
um.progress(0.3, text="Step 1/3: Loading...")
um.progress(0.6, text="Step 2/3: Processing...")
um.progress(0.9, text="Step 3/3: Finalizing...")

um.divider()

# spinner()
um.subheader("7. spinner()")
um.spinner(text="Loading data...")

um.divider()

# loading_skeleton()
um.subheader("8. loading_skeleton()")
um.loading_skeleton(height="20px", width="100%")
um.loading_skeleton(height="100px", width="50%")

um.divider()

# empty_state()
um.subheader("9. empty_state()")
um.empty_state(
    title="No Data Found",
    description="There are no items to display. Try adding some data.",
    icon="inbox"
)

um.divider()

um.success("Data display components test completed!")
