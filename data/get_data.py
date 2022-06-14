import pandas as pd
import streamlit as st

DATA_DICT = {
    "rea":"Reanimation",
    "hosp": "hospitalisation",
    "rad": "retour au domicile",
    "dc": "mort"
}

@st.cache(allow_output_mutation=True)
def get_covid_data():
    covid_url = "https://www.data.gouv.fr/fr/datasets/r/63352e38-d353-4b54-bfd1-f1b3ee1cabd7"
    df = pd.read_csv(covid_url, sep=";", parse_dates=True)
    return df
    
# documentation
# sexe = 0 ( toute personne confondu )
# sexe = 1 ( homme)
# sexe = 2 ( femme)
