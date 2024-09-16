import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Function to calculate resources based on weekly capacity
def calculate_resources(weekly_capacity):
    if weekly_capacity <= 70000:
        manual_scanners = 2
        automated_scanners = 1
        people = 2 * manual_scanners + 2 * automated_scanners  # 2 people per manual scanner
    else:
        # Base resources
        manual_scanners = 2
        automated_scanners = 1
        people = 2 * manual_scanners + 2 * automated_scanners

        # Calculate additional resources
        additional_capacity = weekly_capacity - 70000
        additional_scanners = additional_capacity // 20000
        manual_scanners += additional_scanners
        people += additional_scanners * 2  # 2 people per additional scanner

    return manual_scanners, automated_scanners, people

# Function to plot the graph
def plot_graph(weekly_capacity):
    books_per_week = weekly_capacity / 300
    books_per_month = books_per_week * 4  # assuming 4 weeks per month

    # Time period for prediction (in months)
    months = np.arange(1, 241)  # Looking at 20 years (240 months)

    # Cumulative number of books based on this adjusted capacity
    cumulative_books_corrected = np.cumsum(np.full(months.shape, books_per_month))

    # Plotting the cumulative number of books over time
    plt.figure(figsize=(10, 6))
    plt.plot(months / 12, cumulative_books_corrected, label=f'Cumulative Number of Books ({weekly_capacity:,} Pages per Week)', color='teal', linewidth=2)

    # Milestones for books
    milestones_books = [50000, 100000, 150000, 200000, 300000]
    for milestone in milestones_books:
        plt.axhline(y=milestone, color='red', linestyle='--', label=f'{milestone} books milestone')

    # Adding titles and labels
    plt.title(f'Cumulative Number of Books Scanned Over Time ({weekly_capacity:,} Pages per Week)', fontsize=14)
    plt.xlabel('Time (Years)', fontsize=12)
    plt.ylabel('Cumulative Number of Books', fontsize=12)
    plt.grid(True)

    # Limiting the y-axis to 300,000 books and x-axis to 20 years
    plt.ylim(0, 300000)
    plt.xlim(0, 20)

    # Setting x-axis ticks with yearly intervals
    plt.xticks(np.arange(0, 21, 2), labels=[f'{x}' for x in np.arange(0, 21, 2)])

    plt.legend()

    # Display the plot
    st.pyplot(plt)

# Streamlit app layout
st.title("Book Scanning Capacity Estimator")

# User input for adjustable capacity (starting from 70k pages per week)
weekly_capacity = st.slider("Adjust Weekly Capacity (Pages per Week)", min_value=70000, max_value=350000, value=70000, step=20000)

# Calculate resources needed
manual_scanners, automated_scanners, people = calculate_resources(weekly_capacity)

# Display resources information
st.subheader("Required Resources")
st.write(f"**Manual Scanners**: {manual_scanners}")
st.write(f"**Automated Scanners**: {automated_scanners}")
st.write(f"**People**: {people}")

# Plot the graph with the updated capacity
plot_graph(weekly_capacity)
