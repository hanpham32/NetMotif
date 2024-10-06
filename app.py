import streamlit as st
from src.graph_utils import Graph


def form_callback():
    """
    Handle form validation logic
    """

    if st.session_state['uploaded_file'] is None:
        st.warning("Please upload a file.")
    elif st.session_state['graph_type'] is None:
        st.warning("Please select a graph type.")
    else:
        st.write("Succesfully uploaded file.")
        G = Graph()
        G.generate_graph(file=st.session_state['uploaded_file'], graph_type=st.session_state['graph_type'])

        graph_properties = G.graph_properties()
        st.write(f"Number of nodes: {graph_properties['Number of nodes']}")
        # st.write(f"Edges: {graph_properties['Edges']}")
        st.write(f"Number of edges: {graph_properties['Number of edges']}")
        st.write(f"Weight: {graph_properties['Weight']}")

        G.draw()


def main():
    # Initialize global session state for user form submission
    if 'graph_type' not in st.session_state:
        st.session_state['graph_type'] = None
    if 'uploaded_file' not in st.session_state:
        st.session_state['uploaded_file'] = None

    with st.form(key="form"):
        col1, col2 = st.columns([1, 3])
        with col1:
            graph_type = st.radio(
                "Set Graph type:",
                key="graph",
                index=None,
                options=["Directed", "Undirected"],
            )
        with col2:
            uploaded_file = st.file_uploader("Choose a file")
            st.write(
                "NOTE: Uploading more than 1000 nodes might cause delay. Will implement loading progress to display status"
            )

        submitted = st.form_submit_button(label="Submit")

    if submitted:
        st.session_state['graph_type'] = graph_type
        st.session_state['uploaded_file'] = uploaded_file
        form_callback()


if __name__ == "__main__":
    main()
