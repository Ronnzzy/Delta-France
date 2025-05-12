import streamlit as st
import pandas as pd
from urllib.parse import quote

st.set_page_config(page_title="Email Preview Tool", layout="wide")
st.title("📧 Email Preview Tool (Streamlit Version)")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # Group by Account Number and Sum VAL 1
    grouped = df.groupby('ACCOUNT NO').agg({
        'NAME': 'first',
        'REJECT REASON': 'first',
        'VAL 1': 'sum',
        'EMAIL': 'first'
    }).reset_index()

    rappel_type = st.selectbox("Choose Rappel Type", ["Rappel 1", "Rappel 2", "Rappel 3"])

    def generate_email_body(row, type_):
        name = row['NAME'].title()
        greeting = f"Bonjour {name}," if name else "Chère Madame, Cher Monsieur,"

        if type_ == "Rappel 1":
            body = f"""{greeting}

Nous avons reçu un rejet de prélèvement sur votre compte relatif à votre contrat EMC cité en objet.

Motif du rejet : {row['REJECT REASON']}
Montant de l’échéance rejetée : {row['VAL 1']} EUR

Nous vous remercions de bien vouloir nous contacter au plus vite.

Cordialement,

Abhineet Nim
Credit Controller
ELSEVIER
"""
        elif type_ == "Rappel 2":
            body = f"""Chère Madame, Cher Monsieur,

Nous avons reçu plusieurs rejets de prélèvement consécutifs sur votre compte.

Nous vous invitons à nous contacter sans plus attendre.

Meilleures salutations,

Abhineet Nim
Credit Controller
ELSEVIER"""
        else:
            body = f"""Chère Madame, Cher Monsieur,

Nous avons cherché à vous joindre à plusieurs reprises. L'absence de régularisation entraînerait des conséquences.

Merci de nous contacter rapidement.

Meilleures salutations, 
Abhineet Nim
Credit Controller
ELSEVIER"""

        return body

    st.write("### Preview Emails")

    for i, row in grouped.iterrows():
        email = row["EMAIL"]
        subject = f"Message from Elsevier Collections Department_0{row['ACCOUNT NO']}_{row['NAME'].title()}_{rappel_type}"
        body = generate_email_body(row, rappel_type)
        mailto_link = f"mailto:{email}?subject={quote(subject)}&body={quote(body)}"

        with st.expander(f"{row['ACCOUNT NO']} - {row['NAME']}"):
            st.markdown(f"**To:** {email}")
            st.markdown(f"**Subject:** {subject}")
            st.text_area("Body:", body, height=200)
            st.markdown(f"[📧 Open Email Preview]({mailto_link})")

