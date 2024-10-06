import streamlit as st
from src.graph_utils import graph_generation


def main():
    st.write("NOTE: Uploading more than 1000 nodes might cause delay. Will implement loading progress to display status")
    uploaded_file = st.file_uploader("Choose a file")

    if uploaded_file is not None:
        st.write("Succesfully uploaded file")
        G = graph_generation(uploaded_file)
        st.write(f"Number of nodes: {G.number_of_nodes()}")
        st.write(f"Edges: {G.edges()}")
        st.write(f"Number of edges: {G.number_of_edges()}")
        st.write(f"Weight: {G.size()}")
    else:
        st.write("Upload a file to read the graph.")


if __name__ == "__main__":
    main()
