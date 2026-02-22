import graphviz
import re
import textwrap

class Visualizer:
  def __init__(self, disciplines_df):
    self.df = disciplines_df

  def format_label(self, name, width=20):
    return textwrap.fill(name, width=width, break_long_words=False)

  def generate_visualization(self):
    dot = graphviz.Digraph(
        node_attr={
            'shape': 'box', 
            'fontname': 'Helvetica',
            'fontsize': '9',
            'style': 'filled',
            'fillcolor': '#e1e1e1',
            'width': '2.0', 
            'height': '0.8'
        },
        graph_attr={
            'rankdir': 'TB',
            'splines': 'ortho',
            'nodesep': '0.5',
            'ranksep': '1.0',
            'concentrate': 'true',
            'newrank': 'true'
        }
    )

    df = self.df

    df_sorted = self.df.sort_values(['semester', 'code'])
    df_sorted['sem_index'] = df_sorted.groupby('semester').cumcount()

    max_classes = df_sorted['sem_index'].max()
    for col in range(max_classes + 1):
        col_nodes = df_sorted[df_sorted['sem_index'] == col].sort_values('semester')
        node_list = col_nodes['code'].tolist()
        for i in range(len(node_list) - 1):
            dot.edge(node_list[i], node_list[i+1], style='invis')

    for name, group in df.groupby('semester'):
      with dot.subgraph() as subgraph:
        subgraph.attr(
          rank='same' if name != 10 else 'sink',
        )
        for index, row in group.iterrows():

          subgraph.node(
            row['code'], 
            self.format_label(row['name']), 
            group=row['code'][0:3],
            style='filled', 
            fontname='Helvetica-Bold'
          )

    for index, row in df.iterrows():
      for activity in row['neededActivities']:
        if not re.match(r".*\-.*", activity):
          parsed_activity = activity.split(',')[0]
          dot.edge(parsed_activity, row['code'], penwidth='1.8', constraint='false', color='#555555')

    dot.render(
      "visualizacao",
      directory="visualizations",
      format="png",
      view=False
    )