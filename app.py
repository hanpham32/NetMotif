import streamlit as st
from src.graph_utils import Graph
import src.esu as esu


def form_callback():
    """
    Handle form validation logic
    """

    if st.session_state['uploaded_file'] is None:
        st.warning("Please upload a file.")
    elif st.session_state['graph_type'] is None:
        st.warning("Please select a graph type.")
    else:
        G = Graph()
        G.generate_graph(file=st.session_state['uploaded_file'], graph_type=st.session_state['graph_type'])

        graph_properties = G.graph_properties()
        st.write(f"Number of nodes: {graph_properties['Number of nodes']}")
        # st.write(f"Edges: {graph_properties['Edges']}")
        st.write(f"Number of edges: {graph_properties['Number of edges']}")
        st.write(f"Weight: {graph_properties['Weight']}")
        st.write(esu.esu(G,3))

        G.draw(st.session_state["graph_type"])


def main():
    # Initialize global session state for user form submission
    if 'graph_type' not in st.session_state:
        st.session_state['graph_type'] = None
    if 'uploaded_file' not in st.session_state:
        st.session_state['uploaded_file'] = None
    if 'prev_uploaded_file' not in st.session_state:
        st.session_state['prev_uploaded_file'] = None

    uploaded_file = st.file_uploader("Upload a file")
    if uploaded_file:
        if uploaded_file != st.session_state['prev_uploaded_file']:
            st.session_state['uploaded_file'] = uploaded_file
            st.session_state['prev_uploaded_file'] = uploaded_file
            st.toast("Succesfully uploaded file", icon="✅")

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
            st.write(
                "NOTE: Uploading more than 1000 nodes might consume more processing time."
            )

        submitted = st.form_submit_button(label="Submit")

    if submitted:
        st.session_state['graph_type'] = graph_type
        st.session_state['uploaded_file'] = uploaded_file
        form_callback()
    '''
    [![Repo](https://badgen.net/badge/icon/GitHub?icon=github&label)](https://github.com/hanpham32/NetMotif) 

    '''
    st.markdown("<br>",unsafe_allow_html=True)


if __name__ == "__main__":
    main()
