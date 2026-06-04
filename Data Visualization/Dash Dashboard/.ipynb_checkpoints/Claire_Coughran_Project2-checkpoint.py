import pandas as pd
import numpy as np
import matplotlib as mpl 
from matplotlib import pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.tools import mpl_to_plotly
from dash import Dash, dcc, html, Input, Output
from sklearn.preprocessing import MultiLabelBinarizer
from plotly.subplots import make_subplots
pio.renderers.default = "notebook_connected"

def clean_data(df):
    plots_df = df[['gender', 'location', 'primary_tech_field', 'job_title', 'employment_type', 'work_arrangement', 'experience_years_in_field', 
                   'education_level', 'primary_skill', 'company_size', 'annual_salary_usd', 'hourly_rate_usd', 'annual_bonus_usd', 
                   'equity_total_value_usd', 'equity_vesting_years', 'annual_net_salary_usd', 'annual_savings_usd','is_actively_looking', 
                   'annual_total_expenses_usd']]
    
    plots_df["is_actively_looking"] = plots_df["is_actively_looking"].astype(str)
    
    return plots_df

# plot: hourly rate facet by location
def build_fig1(plots_df):
    fig1 = px.violin(
        plots_df.sort_values("location"),
        x="hourly_rate_usd",
        y="location",
        color="location",
        color_discrete_sequence=px.colors.sequential.Viridis)
    
    fig1.update_layout(title='Industry Hourly Rate Across Tech Hubs', 
                       showlegend=False, margin=dict(l=0, r=0, t=30, b=0), template='simple_white')
    
    fig1.update_xaxes(title_text='Hourly Rate (usd)', showgrid=True, gridcolor='lightgray')
    fig1.update_yaxes(title_text='Tech Hub', showgrid=True, gridcolor='lightgray')
    return fig1

# plot: hourly rate of primary skill bar chart
def build_fig2(plots_df):
    fig2_df = pd.DataFrame(plots_df.groupby('primary_skill')['hourly_rate_usd'].mean()).reset_index().sort_values('hourly_rate_usd')
    fig2_df = fig2_df[~fig2_df['hourly_rate_usd'].between(70, 106)]
    
    fig2 = px.bar(fig2_df, 
                  y='primary_skill', 
                  x='hourly_rate_usd', 
                  title='Hourly Rate for Highest and Lowest Paid Skills', 
                  color_discrete_sequence=px.colors.sequential.Viridis,
                  labels={'primary_skill': 'Expertise', 'hourly_rate_usd': 'Hourly Rate (usd)'})
    
    fig2.update_layout(margin=dict(l=0, r=0, t=30, b=0), template='simple_white')
    
    fig2.update_xaxes(title_text='USD', showgrid=True, gridcolor='lightgray', tickvals=[0, 25, 50, 75, 100, 125, 150])
    fig2.update_yaxes(title_text='Counts')
    return fig2

#plot: hist of annual and net annual salary
def build_fig3(plots_df):
    fig3 = go.Figure()
    
    fig3.add_trace(go.Histogram(
        x=plots_df['annual_salary_usd'],
        name='Annual Salary',
        opacity=0.6,
        marker_color='#31688e', 
        hovertemplate= 'Salary Range: $%{x:,.0f}<br>' + 'Count: %{y}<extra></extra>')) 
    
    fig3.add_trace(go.Histogram(
        x=plots_df['annual_net_salary_usd'],
        name='Annual Net Salary',
        opacity=0.6,
        marker_color='#35b779',
        hovertemplate= 'Net Salary Range: $%{x:,.0f}<br>' + 'Count: %{y}<extra></extra>')) 
    
    fig3.update_layout(title='Annual and Net Annual Salary Frequency',
                       barmode='overlay', 
                       margin=dict(l=0, r=0, t=30, b=0), template='simple_white')
    
    fig3.update_xaxes(title_text='USD', showgrid=True, gridcolor='lightgray')
    fig3.update_yaxes(title_text='Counts', showgrid=True, gridcolor='lightgray')
    return fig3

# plot: scatter annual total expenses vs annual earnings
def build_fig4(plots_df):
    fig4_df = plots_df.copy()
    fig4_df['tot_annual_earnings'] = fig4_df['annual_net_salary_usd'] + fig4_df['annual_bonus_usd'] + (
         fig4_df['equity_total_value_usd'] / fig4_df['equity_vesting_years'])
    
    fig4 = px.scatter(fig4_df, 
                      x='annual_total_expenses_usd', 
                      y='tot_annual_earnings',
                      title='Earnings and Savings Coverage of Expenses',
                      color='annual_savings_usd', 
                      hover_data=['job_title'],
                      color_continuous_scale=px.colors.sequential.Viridis[::-1],
                      labels={'tot_annual_earnings': 'Total Annual Earnings (usd)', 
                              'annual_total_expenses_usd': 'Annual Expenses (usd)', 
                              'annual_savings_usd': 'Annual Savings (usd)',
                              'job_title': 'Job Title'})
    
    max_val = plots_df['annual_total_expenses_usd'].max()
    
    fig4.add_scatter(
        x=[0, 200000, 300000, 400000, 500000, 600000, max_val],
        y=[0, 200000, 300000, 400000, 500000, 600000, max_val],
        mode='lines',
        line=dict(color='lightgrey'),
        hovertemplate='Single Income<extra></extra>',
        showlegend=False)
    
    fig4.add_scatter(
        x=[0, 200000, 300000, 400000, 500000, 600000, max_val],
        y=[0, 200000/2, 300000/2, 400000/2, 500000/2, 600000/2, max_val/2],
        mode='lines',
        line=dict(color='black'),
        hovertemplate='Dual Income Equal Earners<extra></extra>',
        showlegend=False)
    
    fig4.add_scatter(
        x=[0, 100000, 200000, 300000, 400000, 500000, 600000, max_val],
        y=[0, 100000/1.5, 200000/1.5, 300000/1.5, 400000/1.5, 500000/1.5, 600000/1.5, max_val/1.5],
        mode='lines',
        line=dict(color='grey'),
        hovertemplate='Dual Income Other Partner 50% Earner<extra></extra>',
        showlegend=False)
    
    fig4.update_traces(marker=dict(size=3))
    fig4.update_layout(margin=dict(l=0, r=0, t=30, b=0), template='simple_white')
    return fig4

def build_fig5(plots_df):
    fig5 = px.scatter(plots_df, 
                      y='hourly_rate_usd', 
                      x='experience_years_in_field', 
                      title='Hourly Rate and Equity by Experience', 
                      color='equity_total_value_usd',
                      size='annual_bonus_usd', 
                      size_max=13,
                      color_continuous_scale=px.colors.sequential.Viridis,
                      labels={'hourly_rate_usd': 'Hourly Rate (usd)', 'experience_years_in_field': 'Years of Experience in Tech Field', 
                              'equity_total_value_usd': 'Equity Total Value (usd)', 'annual_bonus_usd': 'Annual Bonus'})
    
    fig5.update_layout(margin=dict(l=0, r=0, t=30, b=0), template='simple_white')
    fig5.update_xaxes(showgrid=True, gridcolor='lightgray')
    fig5.update_yaxes(showgrid=True, gridcolor='lightgray')
    return fig5

def apply_filters(plots_df, field=None, job=None, employment=None, company_size=None,
                  gender=None, looking=None, education=None, work_arrangement=None):

    df = plots_df.copy()

    if field: df = df[df["primary_tech_field"] == field]

    if job: df = df[df["job_title"] == job]

    if employment: df = df[df["employment_type"] == employment]

    if company_size: df = df[df["company_size"] == company_size]

    if gender: df = df[df["gender"] == gender]

    if looking: df = df[df["is_actively_looking"] == looking]

    if education: df = df[df["education_level"].isin(education)]

    if work_arrangement: df = df[df["work_arrangement"].isin(work_arrangement)]

    return df

df = pd.read_csv('tech_salary_dataset.csv')
plots_df = clean_data(df)

intro = '''
This dashboard provides an overview of compensation trends in the tech industry for job seekers, employees, and hiring managers. 
Explore earnings across locations, skills, experience levels, education backgrounds, and other workforce characteristics.
'''

fig1_desc = '''
This violin plot shows the distribution of hourly rates across major tech hubs. The width represents the concentration of observations,
while Q1, the median, and Q3 summarize the spread of earnings. Outliers are shown as individual points.
'''

fig2_desc = '''
This bar chart compares the average hourly rate across primary technical skills, highlighting the highest- and lowest-paying specialties.
'''

fig4_desc = '''
The chart above shows the proportion of annual expenses covered by total compensation, calculated as net salary, annual bonus, and annualized equity.
The light gray line represents a single-income household, the dark gray line represents a dual-income household where the second earner makes
50% of the primary income, and the black line represents two equal earners.
'''

fig5_desc = '''
This bubble chart above displays hourly rate as a function of years of experience. Bubble size represents annual bonus, while color represents equity compensation.
'''

fig1 = build_fig1(plots_df)
fig2 = build_fig2(plots_df)
fig3 = build_fig3(plots_df)
fig4 = build_fig4(plots_df)
fig5 = build_fig5(plots_df)

app = Dash()

app.layout = html.Div([
    # Heading
    html.H1("Tech Industry Salary", style={"gridColumn": "1 / span 3", "textAlign": "center"}),
    html.P(intro, style={"gridColumn": "1 / span 3", "textAlign": "center", "padding": "0 50px"}), 
    html.H3('Filters:'),
    # Filters 
    # drop downs: 'primary_tech_field', 'job_title', 'employment_type', company_size
    # radio buttons: 'gender', 'is_looking'
    # checklists: 'education_level', 'work_arrangement'
    html.Div([
        html.Div([
            html.Label("Primary Tech Field"),
            dcc.Dropdown(
                id="field-dropdown",
                options=[{"label": x, "value": x}
                         for x in sorted(plots_df["primary_tech_field"].dropna().unique())],
                placeholder="Primary Tech Field")]),

        html.Div([
            html.Label("Job Title"),
            dcc.Dropdown(
            id="job-dropdown",
            options=[{"label": x, "value": x}
                     for x in sorted(plots_df["job_title"].dropna().unique())],
            placeholder="Job Title")]),

        html.Div([
            html.Label("Employment Type"),
            dcc.Dropdown(
            id="employment-dropdown",
            options=[{"label": x, "value": x}
                     for x in sorted(plots_df["employment_type"].dropna().unique())],
            placeholder="Employment Type")]),

        html.Div([
            html.Label("Company Size"),
            dcc.Dropdown(
            id="company-size-dropdown",
            options=[{"label": x, "value": x}
                     for x in sorted(plots_df["company_size"].dropna().unique())], 
            placeholder="Company Size")]),

        html.Div([
            html.Label("Gender"),
            dcc.RadioItems(
            id="gender-radio",
            options=[{"label": x, "value": x}
                     for x in sorted(plots_df["gender"].dropna().unique())],
            inline=True)]),

        html.Div([
            html.Label("Looking For New Job"),
            dcc.RadioItems(
            id="looking-radio",
            options=[{"label": x, "value": x}
                     for x in sorted(plots_df["is_actively_looking"].dropna().unique())],
            inline=True)]),

        html.Div([
            html.Label("Education Level"),
            dcc.Checklist(
            id="education-checklist",
            options=[{"label": x, "value": x}
                     for x in sorted(plots_df["education_level"].dropna().unique())],
            inline=True)]),
              
        html.Div([
            html.Label("Work Arrangement"),
            dcc.Checklist(
            id="work-arrangement-checklist",
            options=[{"label": x, "value": x}
                     for x in sorted(plots_df["work_arrangement"].dropna().unique())],
            inline=True)])], 
             
        style={"gridColumn": "1 / span 3", "display": "grid", "gridTemplateColumns": "325px 325px 325px 325px", "gap": "0px", "padding": "10px"}),
    
    # Column 1
    html.Div([
        dcc.Graph(id="plot1", figure=fig1, 
                  style={"height": "800px","width": "450px"}), 
        html.P(fig1_desc)]),

    # Column 2
    html.Div([
        dcc.Graph(id="plot2", figure=fig2, 
                  style={"height": "800px","width": "450px"}), 
        html.P(fig2_desc)]),
        

    # Column 3
    html.Div([
        dcc.Graph(id="plot3", figure=fig3, 
              style={"width": "600px"}),
        dcc.Graph(id="plot4", figure=fig4, 
              style={"width": "600px"}),
        html.P(fig4_desc),
        dcc.Graph(id="plot5", figure=fig5, 
              style={"width": "600px"}),
        html.P(fig5_desc)], 
             
        style={"display": "grid", "gridTemplateRows":  "200px 240px 100px 300px 100px", "gap": "0px"})], 
                      
        style={"display": "grid", "gridTemplateColumns": "450px 450px 650px", "gap": "0px", "height": "100vh"})

@app.callback(
    Output('plot1', 'figure'), 
    Output('plot2', 'figure'),
    Output('plot3', 'figure'),
    Output('plot4', 'figure'),
    Output('plot5', 'figure'),
    Input('field-dropdown', 'value'),
    Input('job-dropdown', 'value'),
    Input('employment-dropdown', 'value'),
    Input('company-size-dropdown', 'value'),
    Input('gender-radio', 'value'),
    Input('looking-radio', 'value'),
    Input("education-checklist", "value"),
    Input("work-arrangement-checklist", "value") 
)
def update_plots(field=None, job=None, employment=None, company_size=None,
                  gender=None, looking=None, education=None, work_arrangement=None):
    
    new_df = apply_filters(plots_df, field, job, employment, company_size, gender, looking, education, work_arrangement)
    
    fig1 = build_fig1(new_df)
    fig2 = build_fig2(new_df)
    fig3 = build_fig3(new_df)
    fig4 = build_fig4(new_df)
    fig5 = build_fig5(new_df)

    return fig1, fig2, fig3, fig4, fig5

if __name__ == "__main__":
    app.run(debug=True, port=8051)