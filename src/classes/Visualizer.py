import graphviz
import re
import textwrap

GROUP_COLORS = [
    ('#4e79a7', '#ffffff'),
    ('#f28e2b', '#000000'),
    ('#e15759', '#ffffff'),
    ('#76b7b2', '#000000'),
    ('#59a14f', '#ffffff'),
    ('#edc948', '#000000'),
    ('#b07aa1', '#ffffff'),
    ('#ff9da7', '#000000'),
    ('#9c755f', '#ffffff'),
    ('#bab0ac', '#000000'),
    ('#d37295', '#ffffff'),
    ('#a0cbe8', '#000000'),
    ('#ffbe7d', '#000000'),
    ('#8cd17d', '#000000'),
    ('#b6992d', '#ffffff'),
]

class Visualizer:
  def __init__(self, disciplines_df):
    self.df = disciplines_df

  def format_label(self, name, width=20):
    return textwrap.fill(name, width=width, break_long_words=False)

  def _build_group_color_map(self):
    groups = self.df['code'].str[:3].unique()
    return {
        group: GROUP_COLORS[i % len(GROUP_COLORS)]
        for i, group in enumerate(sorted(groups))
    }

  def generate_visualization(self):
    group_color_map = self._build_group_color_map()

    dot = graphviz.Digraph(
        node_attr={
            'shape': 'box', 
            'fontname': 'Helvetica',
            'fontsize': '12',
            'style': 'filled',
            'width': '2.0', 
            'height': '0.8'
        },
        graph_attr={
            'rankdir': 'TB',
            'splines': 'ortho',
            'nodesep': '0.3',
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
          node_group = row['code'][0:3]
          fillcolor, fontcolor = group_color_map.get(node_group, ('#e1e1e1', '#000000'))

          subgraph.node(
            row['code'], 
            self.format_label(row['name']), 
            group=node_group,
            style='filled',
            fillcolor=fillcolor,
            fontcolor=fontcolor,
            fontname='Helvetica-Bold'
          )

    code_to_color = {
        row['code']: group_color_map.get(row['code'][0:3], ('#555555', '#000000'))[0]
        for _, row in df.iterrows()
    }

    for index, row in df.iterrows():
      for activity in row['neededActivities']:
        if not re.match(r".*\-.*", activity):
          parsed_activity = activity.split(',')[0]
          edge_color = code_to_color.get(parsed_activity, '#555555')
          dot.edge(parsed_activity, row['code'], penwidth='1.0', constraint='false', color=edge_color)

    dot.render(
      "visualizacao",
      directory="visualizations",
      format="png",
      view=False
    )