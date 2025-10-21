import streamlit as st
import requests
import pandas as pd
import json

# Page configuration
st.set_page_config(
    page_title="Student Performance Predictor",
    page_icon="🎓",
    layout="wide"
)

# API endpoint
API_URL = "http://host.docker.internal:5000"

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        font-size: 1.1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("🎓 Student Performance Prediction System")
st.markdown("Predict student performance based on demographics, study habits, and activities")
st.markdown("---")

# Check API health
try:
    health_response = requests.get(f"{API_URL}/health", timeout=5)
    if health_response.status_code == 200:
        health_data = health_response.json()
        if health_data.get("model"):
            st.success("✅ API is connected and model is loaded")
        else:
            st.warning("⚠️ API connected but model not loaded")
    else:
        st.error("❌ API connection failed")
except requests.exceptions.RequestException:
    st.error("❌ Cannot connect to API. Make sure FastAPI is running on http://localhost:8000")

st.markdown("---")

# Create tabs for organized input
tab1, tab2, tab3 = st.tabs(["📋 Basic Info", "📚 Academic Details", "🎯 Activities"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        student_id = st.text_input(
            "Student ID *", 
            value="2231",
            help="Unique identifier for the student"
        )
        
        age = st.number_input(
            "Age *", 
            min_value=15, 
            max_value=18, 
            value=17,
            help="Student's age (15-18 years)"
        )
        
        gender = st.selectbox(
            "Gender *",
            options=[0, 1],
            format_func=lambda x: "Male" if x == 0 else "Female",
            help="0 = Male, 1 = Female"
        )
    
    with col2:
        ethnicity = st.selectbox(
            "Ethnicity *",
            options=[0, 1, 2, 3],
            format_func=lambda x: f"Category {x}",
            help="Ethnicity categories (0-3)"
        )
        
        parental_education = st.selectbox(
            "Parental Education Level *",
            options=[0, 1, 2, 3, 4],
            format_func=lambda x: ["None", "High School", "Some College", "Bachelor's", "Higher"][x],
            help="0=None, 1=High School, 2=Some College, 3=Bachelor's, 4=Higher"
        )
        
        parental_support = st.selectbox(
            "Parental Support Level *",
            options=[0, 1, 2, 3, 4],
            format_func=lambda x: ["None", "Low", "Moderate", "High", "Very High"][x],
            help="Level of parental support (0=None to 4=Very High)"
        )

with tab2:
    col3, col4 = st.columns(2)
    
    with col3:
        study_time = st.slider(
            "Study Time Weekly (hours) *",
            min_value=0,
            max_value=20,
            value=10,
            help="Hours spent studying per week"
        )
        
        absences = st.slider(
            "Number of Absences *",
            min_value=0,
            max_value=30,
            value=5,
            help="Total number of absences"
        )
    
    with col4:
        tutoring = st.selectbox(
            "Tutoring *",
            options=[0, 1],
            format_func=lambda x: "No" if x == 0 else "Yes",
            help="Does the student receive tutoring?"
        )
        
        st.markdown("###")  # Spacing

with tab3:
    st.markdown("### Extracurricular Activities")
    
    col5, col6 = st.columns(2)
    
    with col5:
        extracurricular = st.selectbox(
            "Extracurricular Activities *",
            options=[0, 1],
            format_func=lambda x: "No" if x == 0 else "Yes",
            help="General extracurricular participation"
        )
        
        sports = st.selectbox(
            "Sports Participation *",
            options=[0, 1],
            format_func=lambda x: "No" if x == 0 else "Yes",
            help="Does the student participate in sports?"
        )
    
    with col6:
        music = st.selectbox(
            "Music Activities *",
            options=[0, 1],
            format_func=lambda x: "No" if x == 0 else "Yes",
            help="Does the student participate in music?"
        )
        
        volunteering = st.selectbox(
            "Volunteering *",
            options=[0, 1],
            format_func=lambda x: "No" if x == 0 else "Yes",
            help="Does the student volunteer?"
        )

# Predict button
st.markdown("---")

col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    predict_button = st.button("🔮 Predict Student Performance", type="primary", use_container_width=True)

if predict_button:
    # Prepare data payload matching the Student schema exactly
    student_data = {
        "StudentID": student_id,
        "Age": age,
        "Gender": gender,
        "Ethnicity": ethnicity,
        "ParentalEducation": parental_education,
        "StudyTimeWeekly": study_time,
        "Absences": absences,
        "Tutoring": tutoring,
        "ParentalSupport": parental_support,
        "Extracurricular": extracurricular,
        "Sports": sports,
        "Music": music,
        "Volunteering": volunteering
    }
    
    try:
        with st.spinner("🔄 Making prediction..."):
            response = requests.post(
                f"{API_URL}/predict",
                json=student_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
        
        if response.status_code == 201:
            result = response.json()
            prediction = result.get("prediction", [])
            
            st.success("✅ Prediction completed successfully!")
            
            # Display results
            st.markdown("---")
            st.markdown("## 📈 Prediction Results")
            
            # Create columns for results display
            result_col1, result_col2, result_col3 = st.columns(3)
            
            with result_col1:
                if prediction:
                    st.metric(
                        label="Predicted Performance Score",
                        value=f"{prediction[0]:.2f}",
                        delta=None
                    )
            
            with result_col2:
                # Categorize performance
                if prediction:
                    score = prediction[0]
                    if score >= 80:
                        category = "Excellent"
                        emoji = "🟢"
                    elif score >= 60:
                        category = "Good"
                        emoji = "🟡"
                    elif score >= 40:
                        category = "Average"
                        emoji = "🟠"
                    else:
                        category = "Needs Improvement"
                        emoji = "🔴"
                    
                    st.metric(
                        label="Performance Category",
                        value=f"{emoji} {category}"
                    )
            
            with result_col3:
                if prediction:
                    percentile = min(99, int((prediction[0] / 100) * 100))
                    st.metric(
                        label="Estimated Percentile",
                        value=f"{percentile}th"
                    )
            
            # Recommendations
            st.markdown("---")
            st.markdown("### 💡 Recommendations")
            
            recommendations = []
            
            if study_time < 10:
                recommendations.append("📚 Consider increasing weekly study time for better performance")
            
            if absences > 10:
                recommendations.append("⚠️ High number of absences may impact performance - focus on attendance")
            
            if tutoring == 0 and prediction and prediction[0] < 60:
                recommendations.append("👨‍🏫 Tutoring could help improve academic performance")
            
            if extracurricular == 0:
                recommendations.append("🎯 Extracurricular activities can enhance overall development")
            
            if parental_support < 2:
                recommendations.append("👨‍👩‍👧 Increased parental support may positively impact performance")
            
            if recommendations:
                for rec in recommendations:
                    st.info(rec)
            else:
                st.success("✨ Great profile! Keep up the good work!")
            
            # Show input data
            with st.expander("📋 View Submitted Data"):
                df = pd.DataFrame([student_data])
                st.dataframe(df, use_container_width=True)
            
        else:
            st.error(f"❌ Prediction failed with status code: {response.status_code}")
            try:
                error_detail = response.json()
                st.error(f"Error details: {error_detail}")
            except:
                st.error(f"Response text: {response.text}")
            
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timed out. Please try again.")
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error connecting to API: {str(e)}")
    except Exception as e:
        st.error(f"❌ An unexpected error occurred: {str(e)}")

# Sidebar with information
st.sidebar.title("ℹ️ About")
st.sidebar.info(
    """
    **Student Performance Predictor**
    
    This ML-powered application predicts student academic performance based on:
    
    **Demographics:**
    - Age, Gender, Ethnicity
    - Parental Education
    
    **Academic Factors:**
    - Weekly Study Time
    - Attendance (Absences)
    - Tutoring Support
    
    **Activities:**
    - Sports, Music, Volunteering
    - General Extracurriculars
    
    **Support Systems:**
    - Parental Support Level
    """
)

st.sidebar.markdown("---")
st.sidebar.title("🔧 Configuration")
api_url_input = st.sidebar.text_input("API URL", value=API_URL)
if api_url_input != API_URL:
    API_URL = api_url_input

st.sidebar.markdown("---")
st.sidebar.markdown("### 📝 Field Guide")
st.sidebar.markdown("""
**Gender:** 0=Male, 1=Female

**Ethnicity:** Categories 0-3

**Parental Education:**
- 0: None
- 1: High School
- 2: Some College
- 3: Bachelor's
- 4: Higher

**Binary Fields (0=No, 1=Yes):**
- Tutoring
- Extracurricular
- Sports
- Music
- Volunteering
""")