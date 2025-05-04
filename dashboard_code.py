import pandas as pd
import numpy as np
import plotly.express as px 
import plotly.graph_objects as go
import datetime
from PIL import Image
import streamlit as st

#page setting
st.set_page_config(layout = 'wide',page_title = 'Walmart Sales Dashboard',
                   page_icon = ':bar_chart:')
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',
            unsafe_allow_html=True)

# Importing cleaned data file 
df = pd.read_csv('walmartcleaned_datafile.csv')
df.columns = df.columns.str.lower().str.strip()

# sidebar logo 
st.sidebar.image('walmart-logo-png-27984.png',use_container_width=True,width = 150)

# clean columns for filter 

df['month'] = df['month'].astype(str).str.lower().str.strip()
df['month'] = df['month'].replace({'febuary':'february'})
df['payment_method'] = df['payment_method'].astype(str).str.strip().str.title()
df['category'] = df['category'].astype(str).str.strip().str.title()
df['city'] = df['city'].astype(str).str.strip().str.title()

#copy for filter
df_raw = df.copy()


# setting up side bars 
st.sidebar.header('Filter Options')

# city filter
city_options = ['All'] + sorted(df_raw['city'].dropna().unique().tolist())
selected_city = st.sidebar.selectbox('Select City 📋', options=city_options)

if selected_city != 'All':
    df = df[df['city'] == selected_city]

#Year Filter
year_options = ['All'] + sorted(df_raw['year'].dropna().unique().tolist())
selected_year = st.sidebar.selectbox('Select Year 📋', options=year_options)

if selected_year != 'All':
    df = df[df['year'] == selected_year]    

#Month filter
months_order = ['january', 'february', 'march', 'april', 'may', 'june',
                'july', 'august', 'september', 'october', 'november', 'december']
available_months = [month for month in months_order if month in df_raw['month'].unique()]
sorted_months = ['All'] + available_months
selected_month = st.sidebar.selectbox('Select Month 📋', options=sorted_months)

if selected_month != 'All':
    df = df[df['month'] == selected_month]    


#final filtered_df
filtered_df = df.copy()    


# main title 
st.title('📊 Walmart Sales Dashboard')
st.markdown('---')

#kpi boxes 
col1,col2,col3,col4 = st.columns(4)

# total quantity sold
with col1:
    total_sales = filtered_df['quantity'].sum() 
    st.markdown(f"""
        <div style="
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.05);
            text-align: center;
        ">
            <p style="margin:0; font-size: 18px;">🛒 <strong>Total Sales</strong></p>
            <p style="margin:0; font-size: 28px; font-weight: bold;">{total_sales:,.0f}</p>
        </div>
    """, unsafe_allow_html=True)

# total profit percentage 
with col2: 
    total_revenue = filtered_df['total_price'].sum()
    st.markdown(f"""
        <div style="
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.05);
            text-align: center;
        ">
            <p style="margin:0; font-size: 18px;">💰 <strong>Total Sales</strong></p>
            <p style="margin:0; font-size: 28px; font-weight: bold;">{total_revenue:,.0f}</p>
        </div>
    """, unsafe_allow_html=True)

# average rating 
with col3:
    average_rating = filtered_df['rating'].mean()
    st.markdown(f"""
        <div style="
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.05);
            text-align: center;
        ">
            <p style="margin:0; font-size: 18px;">⭐ <strong>Total Sales</strong></p>
            <p style="margin:0; font-size: 28px; font-weight: bold;">{average_rating:,.0f}</p>
        </div>
    """, unsafe_allow_html=True)

# number of transaction 
with col4:
    transaction = filtered_df.shape[0]
    st.markdown(f"""
        <div style="
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.05);
            text-align: center;
        ">
            <p style="margin:0; font-size: 18px;">📦 <strong>Total Sales</strong></p>
            <p style="margin:0; font-size: 28px; font-weight: bold;">{transaction:,.0f}</p>
        </div>
    """, unsafe_allow_html=True)
    
st.sidebar.markdown('---')    

st.sidebar.markdown("#### 🧠 Advanced Features Used")
st.sidebar.markdown("- ✅ Dynamic Configuration (City/Year Filters)")
st.sidebar.markdown("- ✅ Conditional Content (Expanders & Legend Toggle)")


st.markdown('---')

#panels 
col5,col6 = st.columns([1,1])

#horizontal Bar for units sold by top category 
with col5:
    top_category_bar = filtered_df.groupby('category')['quantity'].sum().sort_values().reset_index()
    fig1 = px.bar(
        top_category_bar,
        x='quantity',
        y='category',
        orientation='h',
        labels={'x': 'Units Sold', 'y': 'Category'},
        title='🔍 Units Sold by Category',
        text='quantity'
    )
    fig1.update_traces(textposition='auto')
    fig1.update_layout(
        margin=dict(l=100, r=40, t=40, b=60),
        height=420,
        title_font=dict(size=16, family='Arial', color='black'),
        title_x=0.0
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.expander('🔍 **View Total Sales by Category**').write(top_category_bar)
    st.download_button('📥 Download Data',
                       data=top_category_bar.to_csv().encode('utf-8'),
                       file_name='Total_Sales_by_Category.csv',
                       mime='text/csv')
    st.markdown('---')

# total transaction by each payment method 
with col6:
    payment_counts = filtered_df.groupby('payment_method')['invoice_id'].count().sort_values().reset_index()
    payment_counts.columns = ['payment_method', 'transaction_count']
    fig2 = px.pie(
        payment_counts,
        values='transaction_count',
        names='payment_method',
        hole=0.5,
        title='💳 Transactions by Payment Method'
    )
    fig2.update_traces(
        textposition='outside',
        showlegend=True,
        textinfo='percent+label',
        pull=[0.1 if val == 'Cash' else 0 for val in payment_counts['payment_method']]
    )
    fig2.update_layout(
        showlegend=False,
        margin=dict(t=40, l=40, r=40, b=40),
        height=420,
        title_font=dict(size=16, family='Arial', color='black'),
        title_x=0.0
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.expander('🔍 **View Total Transactions**').write(payment_counts)
    st.download_button('📥 Download Data',
                       data=payment_counts.to_csv().encode('utf-8'),
                       file_name='Total_Transactions.csv',
                       mime='text/csv')
    st.markdown('---')

# for line chart and scatter plot
col7, col8 = st.columns([1, 1])

# Expanders
exp_col1, exp_col2 = st.columns([1, 1])

# line chart
with col7:
    revenue_by_month = filtered_df.groupby('month')['total_price'].sum().reindex(months_order).dropna()

    fig_line = px.line(
        x=revenue_by_month.index,
        y=revenue_by_month.values,
        labels={'x': 'Month', 'y': 'Total Revenue'},
        title='📅 Revenue by Months',
        markers=True
    )

    fig_line.update_traces(marker=dict(size=8, color='black'))

    fig_line.update_layout(
        height=400,
        margin=dict(t=40, b=40, l=40, r=40),
        showlegend=False,
        title_font=dict(size=16, family='Arial', color='black'),
        title_x=0.0  # Align title to the left like the others
    )

    st.plotly_chart(fig_line, use_container_width=True)
    

# expander
with exp_col1:
    st.expander('🔍 **View Revenue by Month Report**').write(
        filtered_df.groupby('month')['total_price'].sum().reindex(months_order).dropna()
    )
    st.markdown("<hr style='border: 1px solid #ddd;'>", unsafe_allow_html=True)


# scatter plot
with col8:
    # Define color mapping for consistency
    category_color_map = {
        'Health And Beauty': '#1f77b4',
        'Electronic Accessories': '#ff7f0e',
        'Home And Lifestyle': '#2ca02c',
        'Sports And Travel': '#d62728',
        'Food And Beverages': '#9467bd',
        'Fashion Accessories': '#8c564b'
    }

    fig4 = px.scatter(
        filtered_df,
        x='quantity',
        y='total_price',
        color='category',
        color_discrete_map=category_color_map,
        title = '📅 Quantity VS Revenue',
        labels={'quantity': 'Units Sold', 'total_price': 'Total Revenue'}
    )

    fig4.update_traces(marker=dict(size=8, opacity=0.6))
    fig4.update_layout(
        height=400,
        margin=dict(t=40, b=40, l=40, r=40),
        showlegend=False
    )

    st.plotly_chart(fig4, use_container_width=True)

with exp_col2:
    with st.expander("🗂️ View Category Legend"):
        st.markdown("""
        <span style="color:#1f77b4;">● Health And Beauty</span>  
        <span style="color:#ff7f0e;">● Electronic Accessories</span>  
        <span style="color:#2ca02c;">● Home And Lifestyle</span>  
        <span style="color:#d62728;">● Sports And Travel</span>  
        <span style="color:#9467bd;">● Food And Beverages</span>  
        <span style="color:#8c564b;">● Fashion Accessories</span>  
        """, unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid #ddd;'>", unsafe_allow_html=True)


# clean data table 
st.markdown('### 📋 Detailed Transaction Data')
st.expander('🔍 **View Raw Data**').write(filtered_df)
st.download_button('📥 Download Data', 
                   data=filtered_df.to_csv().encode('utf-8'), 
                   file_name='Walmart_Data.csv', mime='text/csv')

        







