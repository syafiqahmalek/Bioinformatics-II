import streamlit as st
import pandas as pd
from Bio import Entrez, SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis

# Replace this with your own email
Entrez.email = "syafiqah-05@graduate.utm.my"


# Function to retrieve protein sequence data
def retrieve_data(id):
    handle = Entrez.efetch(
        db="protein",
        id=id,
        rettype="fasta",
        retmode="text"
    )

    record = SeqIO.read(handle, "fasta")
    handle.close()

    return record


# Function to perform basic protein analysis
def get_basic_analysis(sequence):
    analysis = ProteinAnalysis(str(sequence))

    length = len(sequence)
    composition = analysis.count_amino_acids()
    molecular_weight = analysis.molecular_weight()
    isoelectric_point = analysis.isoelectric_point()

    return length, composition, molecular_weight, isoelectric_point


# ------------------ Streamlit UI ------------------

st.set_page_config(page_title="Lab 1", page_icon="🧬")

st.title("🧬 Lab 1 - Nur Syafiqah")
st.write("Retrieve protein sequence and perform basic protein analysis.")

protein_id = st.text_input("Enter UniProt ID")

retrieve = st.button("Retrieve")

if retrieve:

    if protein_id != "":

        try:
            record = retrieve_data(protein_id)

            length, composition, molecular_weight, isoelectric_point = get_basic_analysis(record.seq)

            st.success("Protein retrieved successfully!")

            st.subheader("Protein Information")

            st.write("**Name:**", record.name)
            st.write("**Description:**", record.description)

            st.write("**Sequence:**")
            st.code(str(record.seq), language="text")

            st.subheader("Basic Protein Analysis")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Sequence Length", length)

            with col2:
                st.metric("Molecular Weight", f"{molecular_weight:.2f} Da")

            with col3:
                st.metric("Isoelectric Point", f"{isoelectric_point:.2f}")

            st.subheader("Amino Acid Composition")

            composition_df = pd.DataFrame(
                composition.items(),
                columns=["Amino Acid", "Count"]
            )

            st.table(composition_df)

        except Exception:
            st.error("Protein not found. Please enter a valid UniProt ID.")

    else:
        st.warning("Please enter a UniProt ID.")