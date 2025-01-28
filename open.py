# openms_app.py

import streamlit as st
import pandas as pd
import numpy as np
from openms import *

# Load the OpenMS library
ms = OpenMS()

# Define a function to upload and process mzXML/mzML files
def process_file(file):
    # Read the file using OpenMS
    exp = ms.readExperiment(file)
    
    # Get the total chromatogram
    chromatogram = exp.getChromatogram()
    
    # Return the chromatogram as a Pandas DataFrame
    return pd.DataFrame(chromatogram)

# Define a function to perform peak picking
def peak_picking(chromatogram):
    # Use OpenMS to perform peak picking
    peaks = ms.peakPick(chromatogram)
    
    # Return the peaks as a Pandas DataFrame
    return pd.DataFrame(peaks)

# Define a function to match MS2 spectra to a library
def match_ms2_spectra(ms2_spectra, library):
    # Use OpenMS to match the MS2 spectra to the library
    matches = ms.matchSpectra(ms2_spectra, library)
    
    # Return the matches as a Pandas DataFrame
    return pd.DataFrame(matches)

# Create the Streamlit app
st.title("OpenMS App")

# Upload file
uploaded_file = st.file_uploader("Choose a file", type=["mzXML", "mzML"])

if uploaded_file is not None:
    # Process the file
    chromatogram = process_file(uploaded_file)
    
    # Display the chromatogram
    st.write("Total Chromatogram:")
    st.write(chromatogram)
    
    # Perform peak picking
    peaks = peak_picking(chromatogram)
    
    # Display the peaks
    st.write("Peaks:")
    st.write(peaks)
    
    # Match MS2 spectra to a library
    ms2_spectra = pd.DataFrame(chromatogram)
    library = pd.DataFrame(chromatogram)
    matches = match_ms2_spectra(ms2_spectra, library)
    
    # Display the matches
    st.write("Matches:")
    st.write(matches)
