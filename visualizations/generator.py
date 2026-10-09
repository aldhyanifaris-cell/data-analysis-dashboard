"""
Dynamic Chart Generator.
Creates interactive Plotly JSON specs and Matplotlib/Seaborn static images.
"""
import os
import io
import json
import base64
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, Optional

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from django.core.files.base import ContentFile

class ChartGenerator:
    """Multi-engine chart generator supporting interactive Plotly and static images."""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def generate_plotly_spec(
        self,
        chart_type: str,
        x: Optional[str] = None,
        y: Optional[str] = None,
        z: Optional[str] = None,
        color: Optional[str] = None,
        size: Optional[str] = None,
        title: Optional[str] = None,
        template: str = 'plotly_white',
    ) -> Dict[str, Any]:
        """Generate full Plotly Figure JSON dictionary."""
        color_col = color if color in self.df.columns else None
        size_col = size if size in self.df.columns else None

        fig = None

        if chart_type == 'line':
            fig = px.line(self.df, x=x, y=y, color=color_col, title=title, template=template)
        elif chart_type == 'bar':
            fig = px.bar(self.df, x=x, y=y, color=color_col, title=title, template=template)
        elif chart_type == 'scatter':
            fig = px.scatter(self.df, x=x, y=y, color=color_col, size=size_col, title=title, template=template, trendline="ols" if not color_col else None)
        elif chart_type == 'scatter3d':
            fig = px.scatter_3d(self.df, x=x, y=y, z=z, color=color_col, size=size_col, title=title, template=template)
        elif chart_type == 'histogram':
            fig = px.histogram(self.df, x=x, color=color_col, title=title, template=template, marginal="box")
        elif chart_type == 'box':
            fig = px.box(self.df, x=x, y=y, color=color_col, title=title, template=template, points="all")
        elif chart_type == 'violin':
            fig = px.violin(self.df, x=x, y=y, color=color_col, box=True, points='all', title=title, template=template)
        elif chart_type == 'pie':
            fig = px.pie(self.df, names=x, values=y, title=title, template=template, hole=0.3)
        elif chart_type == 'heatmap':
            numeric_df = self.df.select_dtypes(include=[np.number])
            corr = numeric_df.corr().round(2)
            fig = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale='RdBu_r', title=title or "Correlation Heatmap", template=template)
        elif chart_type == 'treemap':
            fig = px.treemap(self.df, path=[x] if x else None, values=y, color=color_col, title=title, template=template)
        elif chart_type == 'bubble':
            fig = px.scatter(self.df, x=x, y=y, size=size_col, color=color_col, hover_name=x, title=title, template=template)
        else:
            # Fallback bar
            fig = px.bar(self.df, x=x, y=y, title=title, template=template)

        fig.update_layout(
            margin=dict(l=40, r=40, t=50, b=40),
            font=dict(family="Inter, sans-serif"),
            hoverlabel=dict(bgcolor="white", font_size=13),
        )

        return json.loads(fig.to_json())

    def export_static_image(
        self,
        chart_type: str,
        x: Optional[str] = None,
        y: Optional[str] = None,
        title: Optional[str] = None,
        palette: str = 'viridis',
        format: str = 'png'
    ) -> bytes:
        """Render high-resolution static chart using Seaborn/Matplotlib."""
        plt.figure(figsize=(10, 6), dpi=150)
        sns.set_theme(style="whitegrid", palette=palette)

        if chart_type == 'bar':
            sns.barplot(data=self.df, x=x, y=y)
            plt.xticks(rotation=45, ha='right')
        elif chart_type == 'line':
            sns.lineplot(data=self.df, x=x, y=y, marker='o')
        elif chart_type == 'scatter':
            sns.scatterplot(data=self.df, x=x, y=y)
        elif chart_type == 'histogram':
            sns.histplot(data=self.df, x=x, kde=True)
        elif chart_type == 'box':
            sns.boxplot(data=self.df, x=x, y=y)
        elif chart_type == 'violin':
            sns.violinplot(data=self.df, x=x, y=y)
        elif chart_type == 'heatmap':
            numeric_df = self.df.select_dtypes(include=[np.number])
            sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
        else:
            sns.barplot(data=self.df, x=x, y=y)

        plt.title(title or f"{chart_type.capitalize()} Chart", fontsize=14, pad=15)
        plt.tight_layout()

        buffer = io.BytesIO()
        plt.savefig(buffer, format=format, bbox_inches='tight')
        plt.close()
        buffer.seek(0)
        return buffer.getvalue()
