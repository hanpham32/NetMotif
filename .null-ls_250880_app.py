import streamlit as st
from src.graph_utils import Graph
import src.esu as esu


def form_callback():
    """
    Handle form validation logic
    """

    if st.session_state['uploaded_file'] is None:
        st.warning("Please upload a file.")
        return

    if st.session_state['graph_type'] is None:
        st.warning("Please select a graph type.")
        return

    # create graph from file
    G = Graph()
    G.generate_graph(file=st.session_state['uploaded_file'], graph_type=st.session_state['graph_type'])

    # display graph properties
    graph_properties = G.graph_properties()
    st.write(f"Number of nodes: {graph_properties['Number of nodes']}")
    # st.write(f"Edges: {graph_properties['Edges']}")
    st.write(f"Number of edges: {graph_properties['Number of edges']}")
    st.write(f"Weight: {graph_properties['Weight']}")

    # visualize the full graph if selected
    if st.session_state['is_visualize_graph']:
        st.markdown("### Full Graph Visualization")
        G.draw_graph(st.session_state["graph_type"])

    # Visualize subgraphs if selected
    if st.session_state['is_visualize_subgraph']:
        st.markdown("### Subgraph Visualization")
        G.draw_subgraph(st.session_state["graph_type"], st.session_state["motif_size"])


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

            motif_size = st.number_input("Size of motif", value=3, placeholder="Input motif size...", min_value=1, max_value=5)

            nemo_count_type = st.radio(
                "Nemo Data Options",
                key="nemo_option",
                index=None,
                options=["NemoCount", "NemoProfile", "NemoCollect"],
            )

        with col2:
            st.write("NOTE: Uploading more than 1000 nodes might consume more processing time.")
            st.write("Visualize Options:")
            is_visualize_graph = st.checkbox("Visualize graph")
            is_visualize_subgraph = st.checkbox("Visualize subgraph")

        submitted = st.form_submit_button(label="Submit")

    if submitted:
        st.session_state['is_visualize_graph'] = False
        st.session_state['is_visualize_subgraph'] = False

        if is_visualize_graph:
            st.session_state['is_visualize_graph'] = True
        if is_visualize_subgraph:
            st.session_state['is_visualize_subgraph'] = True

        st.session_state['graph_type'] = graph_type
        st.session_state['uploaded_file'] = uploaded_file
        st.session_state['motif_size'] = motif_size
        form_callback()
    '''
    [![Repo](https://badgen.net/badge/icon/GitHub?icon=github&label)](https://github.com/hanpham32/NetMotif) 

    '''
    st.markdown("<br>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()