
import streamlit as st
import subprocess
import sys

# Function to install required packages
def install_package(package):
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        return True
    except Exception as e:
        st.error(f"Error installing {package}: {str(e)}")
        return False

# Install required packages
required_packages = ['plotly', 'pyteomics', 'numpy']
missing_packages = []

for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        missing_packages.append(package)

if missing_packages:
    st.warning("Some required packages are missing. Installing now...")
    for package in missing_packages:
        with st.spinner(f"Installing {package}..."):
            install_package(package)
    st.success("All required packages installed. Please restart the app.")
    st.stop()

# Import required libraries
import plotly.graph_objects as go
from pyteomics import mzxml
import numpy as np

# Main app
st.title("MZXML Viewer: Total Ion Chromatogram")

# File uploader
uploaded_file = st.file_uploader("Upload an MZXML file", type=["mzxml"])

if uploaded_file is not None:
    try:
        # Parse the MZXML file
        with mzxml.read(uploaded_file) as reader:
            times = []
            intensities = []

            # Show progress
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Extract scan times and total ion current (TIC)
            total_scans = sum(1 for _ in reader)  # Count total scans
            reader.reset()  # Reset the reader
            
            for i, scan in enumerate(reader):
                times.append(scan['retentionTime'])
                intensities.append(sum(scan['intensity array']))
                
                # Update progress
                progress = (i + 1) / total_scans
                progress_bar.progress(progress)
                status_text.text(f'Processing scan {i+1} of {total_scans}')

            # Convert times to minutes
            times = np.array(times) / 60.0  # Convert seconds to minutes

            # Create the TIC plot
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=times, y=intensities, mode='lines', name='TIC'))

            # Customize the layout
            fig.update_layout(
                title='Total Ion Chromatogram (TIC)',
                xaxis_title='Retention Time (minutes)',
                yaxis_title='Total Ion Current (a.u.)',
                template='plotly_white'
            )

            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()

            # Display the plot
            st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Error processing file: {str(e)}")

st.write("Upload an MZXML file to view the Total Ion Chromatogram.")
