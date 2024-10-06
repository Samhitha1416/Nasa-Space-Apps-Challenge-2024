from flask import Flask, render_template, request
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Initialize Flask App
app = Flask(__name__)

# Load the exoplanet CSV file
file_path = r'C:\Users\YASODHARA\Desktop\exoplanet_visualizer\exoplanet_data.csv'
data = pd.read_csv(file_path, on_bad_lines='skip')  # Skips problematic lines

# Print the first few rows of the dataset for debugging
print("Dataset Loaded:")
print(data.head())

# Function to generate and save visualizations for the given planet
def visualize_exoplanet(planet_name):
    # Filter the data for the specified planet name
    planet_data = data[data['pl_name'].str.contains(planet_name, case=False, na=False)]
    
    # Print the filtered data for debugging
    print(f"Filtered Data for {planet_name}:")
    print(planet_data)
    
    if planet_data.empty:
        return None
    
    # Drop rows with NaN values in the required columns
    planet_data = planet_data.dropna(subset=['pl_bmasse', 'pl_radj', 'pl_orbper', 'st_teff', 'sy_dist'])
    
    # Print the data after dropping NaN values
    print("Data after dropping NaN values:")
    print(planet_data)

    # Create visualizations and save them to static directory
    # 1. Planet Mass vs. Radius Scatter plot
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x='pl_bmasse', y='pl_radj', data=planet_data, color='b', alpha=0.6)
    plt.title(f'Planet Mass vs. Radius for {planet_name}')
    plt.xlabel('Planet Mass [Earth Mass]')
    plt.ylabel('Planet Radius [Jupiter Radius]')
    plot_file = f'static/{planet_name}_mass_radius.png'
    plt.savefig(plot_file)
    plt.close()
    
    return plot_file

# Route to render homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission
@app.route('/visualize', methods=['POST'])
def visualize():
    planet_name = request.form['planet_name']
    plot_file = visualize_exoplanet(planet_name)
    
    if plot_file:
        return render_template('index.html', planet_name=planet_name, plot_file=plot_file)
    else:
        error_msg = f"No data found for the planet '{planet_name}'"
        return render_template('index.html', error=error_msg)

# Run Flask App
if __name__ == '__main__':
    app.run(debug=True)
