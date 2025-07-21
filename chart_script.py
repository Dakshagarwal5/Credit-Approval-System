import plotly.express as px
import plotly.graph_objects as go

# Data for the pie chart - using more accurate abbreviated labels within 15 character limit
components = ["Payment History", "# Past Loans", "Current Year", "Approved Volume"]
weights = [40, 20, 20, 20]

# Brand colors in order
colors = ['#1FB8CD', '#DB4545', '#2E8B57', '#5D878F']

# Create pie chart
fig = go.Figure(data=[go.Pie(
    labels=components,
    values=weights,
    marker=dict(colors=colors),
    textinfo='label+percent',
    textposition='inside'
)])

# Update layout with pie chart specific settings and centered legend
fig.update_layout(
    title="Credit Scoring Components",
    uniformtext_minsize=14, 
    uniformtext_mode='hide',
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5)
)

# Save the chart
fig.write_image("credit_scoring_pie_chart.png")