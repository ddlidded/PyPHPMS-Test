
import streamlit as st
import sys
import subprocess

def install_packages():
    try:
        import plotly
        import pyteomics
        import numpy
        return True
    except ImportError:
        st.warning("Installing required packages...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "plotly==5.18.0"])
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyteomics==4.6.2"])
            st.success("Packages installed successfully!")
            st.info("Please restart the app to proceed.")
            st.stop()
        except Exception as e:
            st.error(f"Failed to install packages: {str(e)}")
            st.info("Please try installing manually using:")
            st.code("pip install plotly==5.18.0 pyteomics==4.6.2")
            st.stop()
        return False

# Try to install packages if needed
if not install_packages():
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
