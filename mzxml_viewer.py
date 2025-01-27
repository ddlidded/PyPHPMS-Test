
import streamlit as st
from pyteomics import mzxml
import plotly.graph_objects as go
import numpy as np

# Streamlit app
st.title("MZXML Viewer: Total Ion Chromatogram")

# File uploader
uploaded_file = st.file_uploader("Upload an MZXML file", type=["mzxml"])

if uploaded_file is not None:
    # Parse the MZXML file
    with mzxml.read(uploaded_file) as reader:
        times = []
        intensities = []

        # Extract scan times and total ion current (TIC)
        for scan in reader:
            times.append(scan['retentionTime'])
            intensities.append(sum(scan['intensity array']))

        # Convert times to minutes (if needed)
        times = np.array(times) / 60.0  # Assuming times are in seconds

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

        # Display the plot
        st.plotly_chart(fig)

st.write("Upload an MZXML file to view the Total Ion Chromatogram.")
