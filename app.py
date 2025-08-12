import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# ===================
# Page Configuration
# ===================
st.set_page_config(
    page_title="Startup Funding Dashboard",
    page_icon="🚀",
    layout="wide"
)

# ===================
# CSS for Better Styling
# ===================
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ===================
# Data Loading Function
# ===================
@st.cache_data(show_spinner=False)
def load_and_clean_data():
    """Load startup funding data"""
    try:
        # Get absolute path dynamically
        current_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(current_dir, "data", "startup_funding.csv")
        
        # Alternative path
        base_directory = r"C:\Users\ADITYA\Desktop\Indian startup funding dashboard"
        csv_path_alternative = os.path.join(base_directory, "data", "startup_funding.csv")
        
        # Try both paths
        for path in [csv_path, csv_path_alternative]:
            if os.path.exists(path):
                try:
                    df = pd.read_csv(path, encoding='utf-8')
                    break
                except:
                    try:
                        df = pd.read_csv(path, encoding='latin-1')
                        break
                    except:
                        continue
        else:
            return create_sample_data()
        
        # Clean column names
        df.columns = [col.strip() for col in df.columns]
        
        # Auto-map columns
        column_mapping = {}
        for col in df.columns:
            col_lower = col.lower()
            if 'date' in col_lower:
                column_mapping['Date'] = col
            elif 'startup' in col_lower or ('company' in col_lower and 'investor' not in col_lower):
                column_mapping['Startup_Name'] = col
            elif 'industry' in col_lower or 'vertical' in col_lower:
                column_mapping['Industry'] = col
            elif 'city' in col_lower or 'location' in col_lower:
                column_mapping['City'] = col
            elif 'investor' in col_lower:
                column_mapping['Investor'] = col
            elif 'amount' in col_lower or 'funding' in col_lower:
                column_mapping['Amount'] = col
            elif 'type' in col_lower and 'investment' in col_lower:
                column_mapping['Investment_Type'] = col
        
        # Rename columns
        df = df.rename(columns={v: k for k, v in column_mapping.items()})
        
        # Clean data
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df['Year'] = df['Date'].dt.year
            df = df.dropna(subset=['Date'])
        else:
            df['Year'] = 2023
        
        if 'Amount' in df.columns:
            df['Amount'] = df['Amount'].astype(str)
            df['Amount'] = df['Amount'].str.replace(r'[\$,₹€£¥]', '', regex=True)
            df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
            df = df[df['Amount'] > 0]
        else:
            df['Amount'] = np.random.randint(100000, 10000000, len(df))
        
        # Clean text columns
        text_columns = ['Startup_Name', 'Industry', 'City', 'Investor', 'Investment_Type']
        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
                df[col] = df[col].replace(['nan', 'NaN', 'null', ''], 'Unknown')
                df[col] = df[col].fillna('Unknown')
            else:
                if col == 'Startup_Name':
                    df[col] = [f"Startup_{i}" for i in range(len(df))]
                elif col == 'Industry':
                    df[col] = np.random.choice(['FinTech', 'E-commerce', 'HealthTech'], len(df))
                elif col == 'City':
                    df[col] = np.random.choice(['Mumbai', 'Delhi', 'Bangalore'], len(df))
                elif col == 'Investor':
                    df[col] = np.random.choice(['Sequoia', 'Accel', 'Matrix'], len(df))
                else:
                    df[col] = 'Unknown'
        
        # Final cleanup
        df = df.drop_duplicates(subset=['Startup_Name', 'Year', 'Amount'])
        df = df.dropna(subset=['Amount'])
        
        return df
        
    except Exception as e:
        return create_sample_data()

def create_sample_data():
    """Create realistic sample data"""
    np.random.seed(42)
    
    startups = [
        'Zomato', 'Swiggy', 'PhonePe', 'Paytm', 'Flipkart', 'Ola', 'BYJU\'S',
        'Unacademy', 'Lenskart', 'Nykaa', 'BigBasket', 'Urban Company',
        'PolicyBazaar', 'Razorpay', 'Zerodha', 'CRED', 'Dream11', 'Meesho',
        'Cars24', 'Practo', 'MakeMyTrip', 'Pine Labs', 'Cult.fit'
    ]
    
    industries = [
        'E-commerce', 'FinTech', 'HealthTech', 'EdTech', 'FoodTech', 
        'Transportation', 'Enterprise Software', 'Consumer Internet',
        'Logistics', 'InsurTech', 'PropTech', 'Gaming'
    ]
    
    cities = [
        'Bangalore', 'Mumbai', 'Delhi', 'Gurugram', 'Hyderabad', 
        'Chennai', 'Pune', 'Noida', 'Kolkata', 'Ahmedabad'
    ]
    
    investors = [
        'Sequoia Capital', 'Accel Partners', 'Matrix Partners', 
        'Kalaari Capital', 'Blume Ventures', 'Tiger Global',
        'SoftBank Vision Fund', 'Lightspeed India', 'SAIF Partners'
    ]
    
    investment_types = ['Seed', 'Series A', 'Series B', 'Series C', 'Growth Stage']
    
    # Generate 600 records
    data = {
        'Startup_Name': np.random.choice(startups, 600),
        'Industry': np.random.choice(industries, 600),
        'City': np.random.choice(cities, 600),
        'Investor': np.random.choice(investors, 600),
        'Investment_Type': np.random.choice(investment_types, 600),
        'Amount': np.random.lognormal(14, 1.5, 600).astype(int),
        'Year': np.random.choice([2019, 2020, 2021, 2022, 2023, 2024], 600)
    }
    
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(f'{df["Year"]}-{np.random.randint(1, 13, 600)}-{np.random.randint(1, 29, 600)}', errors='coerce')
    df = df.drop_duplicates(subset=['Startup_Name', 'Year', 'Amount'])
    
    return df.sample(n=min(500, len(df))).reset_index(drop=True)

# ===================
# Load Data
# ===================
with st.spinner("🔄 Loading dashboard..."):
    df = load_and_clean_data()

# ===================
# Sidebar Filters
# ===================
st.sidebar.header("🔍 **Dashboard Filters**")
st.sidebar.markdown("---")

# Year filter
years = sorted(df['Year'].unique())
selected_years = st.sidebar.multiselect(
    "📅 **Years**", 
    years, 
    default=years
)

# Industry filter
industries = sorted(df['Industry'].unique())
selected_industries = st.sidebar.multiselect(
    "🏭 **Industries**", 
    industries, 
    default=industries[:6] if len(industries) > 6 else industries
)

# City filter
cities = sorted(df['City'].unique())
selected_cities = st.sidebar.multiselect(
    "🌍 **Cities**", 
    cities, 
    default=cities[:6] if len(cities) > 6 else cities
)

# Apply filters
filtered_df = df.copy()
if selected_years:
    filtered_df = filtered_df[filtered_df['Year'].isin(selected_years)]
if selected_industries:
    filtered_df = filtered_df[filtered_df['Industry'].isin(selected_industries)]
if selected_cities:
    filtered_df = filtered_df[filtered_df['City'].isin(selected_cities)]

st.sidebar.markdown("---")
st.sidebar.metric("📊 **Records**", len(filtered_df))

# ===================
# Main Dashboard
# ===================
st.markdown('<h1 class="main-header">🚀 Startup Funding Dashboard</h1>', unsafe_allow_html=True)
st.markdown("### 📊 **Indian Startup Ecosystem Analysis**")

if filtered_df.empty:
    st.warning("⚠️ **No data matches your filters**")
    st.stop()

# ===================
# Key Metrics
# ===================
col1, col2, col3, col4, col5 = st.columns(5)

total_funding = filtered_df['Amount'].sum()
num_startups = filtered_df['Startup_Name'].nunique()
num_deals = len(filtered_df)
avg_funding = filtered_df['Amount'].mean()
num_investors = filtered_df['Investor'].nunique()

with col1:
    st.metric("💰 **Total Funding**", f"${total_funding/1e6:.1f}M")
with col2:
    st.metric("🏢 **Startups**", f"{num_startups:,}")
with col3:
    st.metric("📋 **Deals**", f"{num_deals:,}")
with col4:
    st.metric("📈 **Avg Deal**", f"${avg_funding/1e6:.1f}M")
with col5:
    st.metric("👥 **Investors**", f"{num_investors:,}")

st.markdown("---")

# ===================
# 3 TABS - NO TRENDS TAB
# ===================
tab1, tab2, tab3 = st.tabs(["🏭 **Industries**", "💰 **Investors & Startups**", "🌍 **Geography & Analysis**"])

# ===================
# TAB 1: INDUSTRIES
# ===================
with tab1:
    st.header("🏭 **Industry Analysis**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔝 **Top Industries by Funding**")
        industry_funding = filtered_df.groupby('Industry')['Amount'].sum().nlargest(10).reset_index()
        
        fig1 = px.bar(
            industry_funding,
            x='Amount',
            y='Industry',
            orientation='h',
            title="Top 10 Industries by Total Funding",
            color='Amount',
            color_continuous_scale='Blues',
            text='Amount'
        )
        fig1.update_traces(texttemplate='$%{text:.2s}', textposition='outside')
        fig1.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.subheader("📊 **Industry Deal Distribution**")
        industry_deals = filtered_df['Industry'].value_counts().head(8).reset_index()
        industry_deals.columns = ['Industry', 'Deal_Count']
        
        fig2 = px.pie(
            industry_deals,
            values='Deal_Count',
            names='Industry',
            title="Deal Distribution by Industry",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig2.update_layout(height=500)
        st.plotly_chart(fig2, use_container_width=True)
    
    # Full width chart
    st.subheader("💼 **Investment Types by Industry**")
    if 'Investment_Type' in filtered_df.columns:
        investment_industry = filtered_df.groupby(['Industry', 'Investment_Type']).size().reset_index(name='Count')
        top_industries = filtered_df['Industry'].value_counts().head(6).index
        investment_industry = investment_industry[investment_industry['Industry'].isin(top_industries)]
        
        fig3 = px.bar(
            investment_industry,
            x='Industry',
            y='Count',
            color='Investment_Type',
            title="Investment Types Distribution Across Top Industries",
            barmode='stack'
        )
        fig3.update_layout(height=400, xaxis_tickangle=45)
        st.plotly_chart(fig3, use_container_width=True)
    
    # Industry performance table
    st.subheader("📈 **Industry Performance Summary**")
    industry_summary = filtered_df.groupby('Industry').agg({
        'Amount': ['sum', 'mean', 'count'],
        'Startup_Name': 'nunique'
    }).round(0)
    
    industry_summary.columns = ['Total Funding', 'Avg Funding', 'Deals', 'Unique Startups']
    industry_summary['Total Funding'] = industry_summary['Total Funding'].apply(lambda x: f"${x/1e6:.1f}M")
    industry_summary['Avg Funding'] = industry_summary['Avg Funding'].apply(lambda x: f"${x/1e6:.1f}M")
    industry_summary = industry_summary.sort_values('Deals', ascending=False).head(10)
    
    st.dataframe(industry_summary, use_container_width=True)

# ===================
# TAB 2: INVESTORS & STARTUPS
# ===================
with tab2:
    st.header("💰 **Investor & Startup Analysis**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👥 **Top Active Investors**")
        investor_analysis = filtered_df.groupby('Investor').agg({
            'Amount': 'sum',
            'Startup_Name': 'count'
        }).reset_index()
        investor_analysis.columns = ['Investor', 'Total_Investment', 'Deal_Count']
        investor_analysis = investor_analysis.nlargest(10, 'Total_Investment')
        
        fig4 = px.scatter(
            investor_analysis,
            x='Deal_Count',
            y='Total_Investment',
            size='Total_Investment',
            color='Investor',
            title="Investor Activity: Investment vs Deal Count",
            hover_data=['Investor'],
            size_max=50
        )
        fig4.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig4, use_container_width=True)
    
    with col2:
        st.subheader("🌟 **Top Funded Startups**")
        startup_funding = filtered_df.groupby('Startup_Name')['Amount'].sum().nlargest(10).reset_index()
        
        fig5 = px.bar(
            startup_funding,
            x='Amount',
            y='Startup_Name',
            orientation='h',
            title="Top 10 Funded Startups",
            color='Amount',
            color_continuous_scale='Reds',
            text='Amount'
        )
        fig5.update_traces(texttemplate='$%{text:.2s}', textposition='outside')
        fig5.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig5, use_container_width=True)
    
    # Investment rounds analysis
    st.subheader("🎯 **Investment Rounds Analysis**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'Investment_Type' in filtered_df.columns:
            investment_rounds = filtered_df['Investment_Type'].value_counts().reset_index()
            investment_rounds.columns = ['Investment_Type', 'Count']
            
            fig6 = px.funnel(
                investment_rounds,
                x='Count',
                y='Investment_Type',
                title="Investment Stages Distribution"
            )
            fig6.update_layout(height=400)
            st.plotly_chart(fig6, use_container_width=True)
    
    with col2:
        # Deal size analysis
        filtered_df['Deal_Size_Range'] = pd.cut(
            filtered_df['Amount'], 
            bins=[0, 1e6, 5e6, 10e6, 50e6, float('inf')], 
            labels=['<$1M', '$1M-$5M', '$5M-$10M', '$10M-$50M', '>$50M']
        )
        
        deal_sizes = filtered_df['Deal_Size_Range'].value_counts().reset_index()
        deal_sizes.columns = ['Deal_Size', 'Count']
        
        fig7 = px.bar(
            deal_sizes,
            x='Deal_Size',
            y='Count',
            title="Deal Size Distribution",
            color='Count',
            color_continuous_scale='Greens'
        )
        fig7.update_layout(height=400)
        st.plotly_chart(fig7, use_container_width=True)

# ===================
# TAB 3: GEOGRAPHY & ANALYSIS
# ===================
with tab3:
    st.header("🌍 **Geographic & Advanced Analysis**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏙️ **Funding by City**")
        city_funding = filtered_df.groupby('City')['Amount'].sum().nlargest(8).reset_index()
        
        fig8 = px.pie(
            city_funding,
            values='Amount',
            names='City',
            title="Funding Distribution by City",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig8.update_traces(textposition='inside', textinfo='percent+label')
        fig8.update_layout(height=500)
        st.plotly_chart(fig8, use_container_width=True)
    
    with col2:
        st.subheader("📈 **City Startup Ecosystem**")
        city_ecosystem = filtered_df.groupby('City').agg({
            'Startup_Name': 'nunique',
            'Investor': 'nunique',
            'Amount': 'sum'
        }).reset_index()
        city_ecosystem.columns = ['City', 'Startups', 'Investors', 'Total_Funding']
        city_ecosystem = city_ecosystem.nlargest(8, 'Total_Funding')
        
        fig9 = px.scatter(
            city_ecosystem,
            x='Startups',
            y='Investors',
            size='Total_Funding',
            color='City',
            title="City Ecosystem: Startups vs Investors",
            hover_data=['Total_Funding'],
            size_max=60
        )
        fig9.update_layout(height=500)
        st.plotly_chart(fig9, use_container_width=True)
    
    # Heatmap analysis
    st.subheader("🔥 **City vs Industry Heatmap**")
    
    # Create heatmap data
    top_cities = filtered_df['City'].value_counts().head(6).index
    top_industries_geo = filtered_df['Industry'].value_counts().head(6).index
    
    heatmap_data = filtered_df[
        (filtered_df['City'].isin(top_cities)) & 
        (filtered_df['Industry'].isin(top_industries_geo))
    ]
    
    heatmap_pivot = heatmap_data.groupby(['City', 'Industry'])['Amount'].sum().reset_index()
    heatmap_pivot = heatmap_pivot.pivot(index='City', columns='Industry', values='Amount').fillna(0)
    
    fig10 = px.imshow(
        heatmap_pivot,
        title="Funding Heatmap: Top Cities vs Industries (USD)",
        color_continuous_scale='RdYlBu_r',
        aspect='auto'
    )
    fig10.update_layout(height=400)
    st.plotly_chart(fig10, use_container_width=True)
    
    # Summary metrics by city
    st.subheader("🏆 **City Performance Ranking**")
    city_performance = filtered_df.groupby('City').agg({
        'Amount': ['sum', 'mean'],
        'Startup_Name': 'nunique',
        'Investor': 'nunique'
    }).round(0)
    
    city_performance.columns = ['Total Funding', 'Avg Deal Size', 'Startups', 'Investors']
    city_performance['Total Funding'] = city_performance['Total Funding'].apply(lambda x: f"${x/1e6:.1f}M")
    city_performance['Avg Deal Size'] = city_performance['Avg Deal Size'].apply(lambda x: f"${x/1e6:.1f}M")
    city_performance = city_performance.sort_values('Startups', ascending=False).head(10)
    
    st.dataframe(city_performance, use_container_width=True)

# ===================
# Data Export Section
# ===================
st.markdown("---")
st.subheader("📋 **Data Export**")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Show summary
    st.info(f"📊 **Current Dataset**: {len(filtered_df)} records | {filtered_df['Startup_Name'].nunique()} startups | {filtered_df['Investor'].nunique()} investors")
    
    # Download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="💾 **Download Filtered Data**",
        data=csv,
        file_name=f"startup_funding_export_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        use_container_width=True
    )

# ===================
# Footer
# ===================
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p>📊 <strong>Startup Funding Dashboard</strong></p>
        <p>Built with ❤️ using Streamlit & Plotly</p>
        <p><em>Professional Analytics for Indian Startup Ecosystem</em></p>
    </div>
    """, 
    unsafe_allow_html=True
)
