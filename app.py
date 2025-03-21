import streamlit as st
import time
from src.graph_with_subgraph import GraphWithSubgraph
from src.graph_types import GraphType
import src.random_graph as rg
import src.motif_statistics as stat

st.set_page_config(page_title="NEMO motif detection program")
st.title('NEMO motif detection program')

def form_callback(start_time):
    """
    Handle form validation logic
    """

    if st.session_state["uploaded_file"] is None:
        st.warning("Please upload a file.")
        return

    if st.session_state["graph_type"] is None:
        st.warning("Please select a graph type.")
        return

    if st.session_state["number_of_random_graphs"] is None:
        st.warning("Please select a number of random graphs between 5-100.")
        return

    # create graph from file
    G = GraphWithSubgraph(
        graph_type=st.session_state["graph_type"],
        input=st.session_state["uploaded_file"],
        motif_size=st.session_state["motif_size"],
    )

    # display graph properties
    graph_properties = G.get_graph_properties()
    st.write(f"Number of nodes: {graph_properties['Number of nodes']}")
    # st.write(f"Edges: {graph_properties['Edges']}")
    st.write(f"Number of edges: {graph_properties['Number of edges']}")
    st.write(f"Weight: {graph_properties['Weight']}")
    st.write(f"Number of subgraphs: {graph_properties['Number of subgraphs']}")

    # visualize the full graph if selected
    if st.session_state["is_visualize_graph"]:
        st.markdown("### Full Graph Visualization")
        G.draw_graph()

    # Visualize subgraphs if selected
    if st.session_state["is_visualize_subgraph"]:
        st.markdown("### Subgraph Visualization")
        G.draw_subgraph()

    #Generate random graphs
    random_graphs = rg.generate_random_graphs(G, st.session_state['number_of_random_graphs'])

    stats = stat.process_statistics(G, random_graphs)

    end_time = time.time()
    elapsed_time = end_time - start_time
    st.write(f"Time elapsed: {elapsed_time:.2f} seconds")

    #Visualize statistics
    st.markdown("### Statistics Table")
    stat.draw_statistics(stats)

    # Download button if nemo count option is selected to subgraph collection
    if st.session_state["nemo_count_option"] is "NemoCount":
        G.generate_nemo_count()

    # Download button if nemo count option is selected to subgraph collection
    if st.session_state["nemo_count_option"] is "SubgraphProfile":
        G.generate_subgraph_profile()

    # Download button if nemo count option is selected to subgraph collection
    if st.session_state["nemo_count_option"] is "SubgraphCollection":
        G.generate_subgraph_collection()

def main():
    # Initialize global session state for user form submission
    if "graph_type" not in st.session_state:
        st.session_state["graph_type"] = None
    if "uploaded_file" not in st.session_state:
        st.session_state["uploaded_file"] = None
    if "prev_uploaded_file" not in st.session_state:
        st.session_state["prev_uploaded_file"] = None

    uploaded_file = st.file_uploader("Upload a file")
    if uploaded_file:
        if uploaded_file != st.session_state["prev_uploaded_file"]:
            st.session_state["uploaded_file"] = uploaded_file
            st.session_state["prev_uploaded_file"] = uploaded_file
            st.toast("Succesfully uploaded file", icon="✅")

    demo = st.button("Use Demo File")
    if demo:
        st.session_state["uploaded_file"] = "./NetMotif/data/bestGraph.txt"
        st.session_state["prev_uploaded_file"] = "./NetMotif/data/bestGraph.txt"
        st.toast("Succesfully uploaded demo file", icon="✅")

    with st.form(key="form"):
        col1, col2 = st.columns([1, 2])
        with col1:
            graph_type = st.radio(
                "Set Graph type:",
                key="graph",
                options=[GraphType.UNDIRECTED, GraphType.DIRECTED],
                format_func=lambda x: x.value,
            )

            motif_size = st.number_input(
                "Size of motif",
                value=3,
                placeholder="Input motif size...",
                min_value=1,
                max_value=5,
            )

            number_of_random_graphs = st.number_input(
                "Number of random graphs",
                value=20,
                placeholder="Input number of graphs...",
                min_value=5,
                max_value=100,
            )

            nemo_count_type = st.radio(
                "Nemo Data Options",
                key="nemo_option",
                options=["NemoCount", "SubgraphProfile", "SubgraphCollection"],
            )

        with col2:
            st.write(
                "NOTE: Uploading more than 1000 nodes might consume more processing time."
            )
            st.write("Visualize Options:")
            is_visualize_graph = st.checkbox("Visualize graph")
            is_visualize_subgraph = st.checkbox("Visualize subgraph")

        submitted = st.form_submit_button(label="Submit")

    if submitted:
        st.session_state["is_visualize_graph"] = False
        st.session_state["is_visualize_subgraph"] = False

        if is_visualize_graph:
            st.session_state["is_visualize_graph"] = True
        if is_visualize_subgraph:
            st.session_state["is_visualize_subgraph"] = True

        st.session_state["graph_type"] = graph_type
        st.session_state["uploaded_file"] = uploaded_file
        st.session_state["motif_size"] = motif_size
        st.session_state["number_of_random_graphs"] = number_of_random_graphs
        st.session_state["nemo_count_option"] = nemo_count_type
        start_time = time.time()
        form_callback(start_time)
    """
    [![Repo](https://badgen.net/badge/icon/GitHub?icon=github&label)](https://github.com/hanpham32/NetMotif)

    """
    st.markdown("<br>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
