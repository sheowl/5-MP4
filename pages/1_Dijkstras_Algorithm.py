import sys
import streamlit as st
import graphviz
from heapq import heappop, heappush

# Directed graph as an adjacency list
graph = {
    'A': {'B': 5, 'C': 2},
    'B': {'C': 1, 'D': 4, 'E': 2},
    'C': {'E': 7},
    'D': {'E': 6, 'F': 3},
    'E': {'F': 1},
    'F': {}
}

def dijkstra(graph, start, destination):
    inf = sys.maxsize
    node_data = {node: {'cost': inf, 'pred': []} for node in graph}
    node_data[start]['cost'] = 0

    visited = set() # visited nodes
    priority_queue = [(0, start)] # priority queue of (cost, node)

    while priority_queue:
        current_cost, current_node = heappop(priority_queue)

        if current_node in visited:
            continue
        visited.add(current_node)

        for neighbor in graph[current_node]:
            if neighbor not in visited:
                new_cost = current_cost + graph[current_node][neighbor]

                if new_cost < node_data[neighbor]['cost']:
                    node_data[neighbor]['cost'] = new_cost
                    node_data[neighbor]['pred'] = node_data[current_node]['pred'] + [current_node]
                    heappush(priority_queue, (new_cost, neighbor))

                elif new_cost == node_data[neighbor]['cost']:
                    if current_node not in node_data[neighbor]['pred']:
                        node_data[neighbor]['pred'].append(current_node)

    return node_data

# display the Streamlit app
st.set_page_config(page_title="Dijkstra's Algorithm", layout="wide")
st.title("📍 Dijkstra's Algorithm")
st.write("Dijkstra’s Algorithm is one of the techniques used to search for the shortest path between two" \
" nodes in weighted graphs. The algorithm is named after its creator, Dutch computer scientist Edsger W. Dijkstra, " \
" who introduced it in 1956 (W3Schools, 2024). The process of finding the shortest path works by repeatedly selecting " \
"the nearest unvisited vertex and updating the distances to all its unvisited neighboring vertices. The search begins at a " \
"source node and iteratively expands until all nodes have been visited, ultimately producing a shortest-path tree.")

# select nodes
nodes = list(graph.keys())
source = st.selectbox("Select Start Node", nodes)
destination = st.selectbox("Select Destination Node", nodes, index=len(nodes)-1)

# graph visualization
if "show_graph" not in st.session_state:
    st.session_state.show_graph = False

if st.button("Find Shortest Path"):
    if source == destination:
        st.warning("Source and destination must be different.")
    else:
        st.session_state.show_graph = True
        result = dijkstra(graph, source, destination)
        cost = result[destination]['cost']

        if cost == sys.maxsize:
            st.error(f"No path found from {source} to {destination}.")
        else:
            st.session_state.path = result[destination]['pred'] + list(destination)
            st.session_state.cost = cost
            st.success(f"Shortest path from {source} to {destination}:")
            st.code(" -> ".join(st.session_state.path), language="text")
            st.write(f"Total cost: **{cost}**")
            st.balloons()

# display the graph 
if st.session_state.show_graph:
    st.subheader("Graph Visualization")

    dot = graphviz.Digraph(engine="dot")
    dot.attr(rankdir='LR', splines='polyline', overlap='false', fontname='Arial')

    # node colors
    for node in graph.keys():
        if 'path' in st.session_state:
            if node == source:
                fill = '#23e79e'  # Green for start
            elif node == destination:
                fill = '#e65c38'  # Red-Orange for end
            else:
                fill = '#f0f0f0'  # Default
        else:
            fill = '#f0f0f0'  # Default if no path selected

        dot.node(node, shape='circle', style='filled', fillcolor=fill, color='#555555')

    # B–C and D–E on same horizontal level
    dot.body += ['{ rank=same; B; C; }']
    dot.body += ['{ rank=same; D; E; }']

    # Edges with weights
    edges = {
        'A': [('B', 5), ('C', 2)],
        'B': [('C', 1), ('D', 4), ('E', 2)],  
        'C': [('E', 7)],
        'D': [('E', 6),('F', 3)],
        'E': [('F', 1)],
    }

    # Highlight edges in the path
    highlight_edges = set()
    if 'path' in st.session_state and len(st.session_state.path) > 1:
        highlight_edges = set(zip(st.session_state.path, st.session_state.path[1:]))

    for src, targets in edges.items():
        for dst, weight in targets:
            if (src, dst) in highlight_edges:
                dot.edge(src, dst, label=str(weight), fontsize='10', color='#fdd835', penwidth='2')
            else:
                dot.edge(src, dst, label=str(weight), fontsize='10')

    col1, col2 = st.columns([1.2, 0.8])
    with col1:
        st.graphviz_chart(dot, use_container_width=True)
