import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots



df = pd.read_csv('Sleep_Efficiency.csv')
# Convert bedtime and wakeup time columns to datetime format
df['Bedtime'] = pd.to_datetime(df['Bedtime'])
df['Wakeup time'] = pd.to_datetime(df['Wakeup time'])
df['DayOfWeek'] = df['Bedtime'].dt.day_name()
# "DayType" column based on weekdays and weekends
df['DayType'] = df['DayOfWeek'].apply(lambda x: 'Weekday' if x in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'] else 'Weekend')
# Convert 'Wakeup time' column to datetime format
df['Wakeup time'] = pd.to_datetime(df['Wakeup time'])
# Extract the hour number into a new column
df['Wakeup Hour'] = df['Wakeup time'].dt.hour
df['Sleep efficiency'] = pd.to_numeric(df['Sleep efficiency'], errors='coerce')


st.set_page_config(page_title="How does sleep efficiency vary by age, sex, or other variables?",
                   page_icon=":bar_chart:")
st.title('How does sleep efficiency vary by age, sex, or other variables?')


#First Graph
st.subheader('Sleep Efficiency by Wakeup Hour')
# Filter the data based on the selected gender
selected_gender = st.selectbox('Select Gender', ['Male', 'Female'])
filtered_data = df[df['Gender'] == selected_gender]

# Create the box plot using plotly express
fig = px.box(filtered_data, x='Wakeup Hour', y='Sleep efficiency', color='Wakeup Hour', hover_data=['Wakeup time'],
            category_orders={'Wakeup Hour': sorted(df['Wakeup Hour'].unique())})
fig.update_traces(hovertemplate="<b>Wakeup Hour:</b> %{x}<br><b>Sleep Efficiency:</b> %{y}<br><b>Wakeup Time:</b> %{customdata[0]}")


# Show the plot
st.plotly_chart(fig)


#Second Graph
st.subheader('Sleep Type by Average Percentage')
# Get the age range from the user using number input fields
min_age = st.number_input('Minimum Age', min_value=int(df['Age'].min()), max_value=int(df['Age'].max()), value=int(df['Age'].min()), step=10)
max_age = st.number_input('Maximum Age', min_value=int(df['Age'].min()), max_value=int(df['Age'].max()), value=int(df['Age'].max()), step=10)

# Filter the dataframe based on the selected age range
filtered_df = df[(df['Age'] >= min_age) & (df['Age'] <= max_age)]

# Calculate the average percentage of each type of sleep
avg_sleep_perc = filtered_df[[ 'REM sleep percentage', 'Deep sleep percentage',
    'Light sleep percentage' ]].mean()
# Define a custom color palette for the bars
color_scale = ["purple", "skyblue", "orange"]
# Create a bar plot using Plotly Express
fig = px.bar(avg_sleep_perc, y=avg_sleep_perc.index, x=avg_sleep_perc.values,
             labels={'x': 'Sleep Type', 'y': 'Average Percentage'},
             color=avg_sleep_perc.index, color_discrete_sequence=color_scale)


# Customize the plot as needed
fig.update_layout(yaxis_title='Sleep Type',
                  xaxis_title='Average Percentage')

# Display the plot
st.plotly_chart(fig, use_container_width=True)

#Third Graph
# Define the columns for the line plot
st.subheader('Sleep Efficiency by Number of Sleep Hours and weekly Habits')
x_column = 'Sleep duration'
y_column = 'Sleep efficiency'

# Get unique values for the condition columns
awakenings_values = df['Awakenings'].unique()
alcohol_values = df['Alcohol consumption'].unique()
smoking_values = df['Smoking status'].unique()
exercise_values = df['Exercise frequency'].unique()

# User inputs for conditions
#selected_awakenings = st.selectbox('Select Awakenings', awakenings_values)
selected_alcohol = st.selectbox('Select Alcohol Consumption', alcohol_values)
selected_smoking = st.selectbox('Select Smoking Status', smoking_values)
selected_exercise = st.selectbox('Select Exercise Frequency', exercise_values)

# Filter the dataframe based on user-selected conditions
filtered_df = df[(df['Alcohol consumption'] == selected_alcohol) &
                (df['Smoking status'] == selected_smoking) &
                (df['Exercise frequency'] == selected_exercise)]

# Create a scatter plot using Plotly Express
fig = px.density_heatmap(filtered_df, x=x_column, y=y_column,
                labels={'x': 'Sleep Duration', 'y': 'Sleep Efficiency'})

# Customize the plot as needed
fig.update_layout(legend_title_text='Conditions')

# Display the plot
st.plotly_chart(fig, use_container_width=True)


# Sleep efficiency comparison between weekdays and weekends
st.subheader('Density Sleep Efficiency Comparison: Weekdays vs. Weekends')

# Get unique values for the 'DayType' column
day_values = df['DayType'].unique()

# User selects the weekdays and weekends
selected_days = st.multiselect('Select Weekdays/Weekends', day_values)

# Filter the data based on the selected days
selected_data = df[df['DayType'].isin(selected_days)]
fig, ax = plt.subplots()
for day in selected_days:
    data = selected_data[selected_data['DayType'] == day]
    density = data['Sleep efficiency'].plot.kde()
    density.set_label(day)

ax.set_xlabel('Sleep Efficiency')
ax.set_ylabel('Density')
# ax.set_title('Sleep Efficiency Distribution: Weekdays vs. Weekends')
ax.legend()
st.pyplot(fig)
















