import os
import streamlit as st
import streamlit.config as config

from pathlib import Path
from rich.console import Console

console = Console()

def streamlit_graphs():
    st.set_page_config(
        page_title="GitHub Dashboard",
        page_icon="📊",
        layout="centered",
        initial_sidebar_state="auto",
    )
    config.set_option("server.enableCORS", False)
    config.set_option("global.developmentMode", False)

    console.print("[bold green]\nStreamlit server is running on port 8501[/bold green]")
    console.print('Press CTRL+C or close terminal anytime to terminate streamlit server', style='bold yellow')
    console.print("[link]Please visit my GitHub repository to see all of my projects:\nhttps://github.com/yousefabuz17[/link]")
    
    graph_path = Path(__file__).resolve().parent.parent / 'Figures'
    graph_files = sorted(os.listdir(graph_path), key=lambda x: os.path.getmtime(os.path.join(graph_path, x)), reverse=True)

    console.print(f"\nThere are a total of {len(graph_files)} graphs being displayed on the dashboard", style='bold white')
    st.title("GitHub Dashboard")
    for idx, graph in enumerate(graph_files, start=1):
        st.header(f"Graph {idx}")
        image_path = str(graph_path / graph)
        st.image(image_path, use_column_width=True)

if __name__ == '__main__':
    streamlit_graphs()
