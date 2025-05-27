"""
📌 종합 채용 대시보드 (에러 방지 개선 버전)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import random

# 페이지 설정
st.set_page_config(
    page_title="종합 채용 대시보드",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def generate_sample_data():
    names = ['김민수', '이지은', '박준호', '최서영', '정하늘', '강민아', '윤성진', '조유리']
    positions = ['프론트엔드 개발자', '백엔드 개발자', '디자이너', '데이터 분석가']
    statuses = ['서류 심사', '1차 면접', '2차 면접', '최종 면접', '합격', '불합격']
    experiences = ['신입', '1년', '2년', '3년']
    locations = ['서울', '경기', '부산']
    sources = ['사람인', '잡코리아', '링크드인']

    candidates_data = []
    for i, name in enumerate(names):
        applied_date = datetime.now() - timedelta(days=random.randint(1, 90))
        candidates_data.append({
            'id': f'REC{i+1:04d}',
            'name': name,
            'position': random.choice(positions),
            'status': random.choice(statuses),
            'experience': random.choice(experiences),
            'location': random.choice(locations),
            'resume_score': random.randint(60, 98),
            'rating': round(random.uniform(3.0, 5.0), 1),
            'applied_date': applied_date,
            'email': f'{name.replace(" ", "").lower()}@email.com',
            'salary_expectation': f'{random.randint(3000, 8000)}만원',
            'skills': random.choice(['Python', 'React', 'SQL']),
            'source': random.choice(sources)
        })

    candidates_df = pd.DataFrame(candidates_data)
    candidates_df['applied_date'] = pd.to_datetime(candidates_df['applied_date'], errors='coerce')
    candidates_df.dropna(subset=['applied_date'], inplace=True)

    channel_df = pd.DataFrame({
        'channel': sources,
        'applicants': [1024, 756, 234],
        'hired': [51, 38, 18],
        'cost': [4800000, 3200000, 1800000],
        'conversion_rate': [4.98, 5.03, 7.69]
    })

    funnel_df = pd.DataFrame({
        'stage': ['총 지원자', '서류 통과', '1차 면접', '2차 면접', '최종 면접', '최종 합격'],
        'count': [3014, 1507, 754, 377, 226, 151],
        'percentage': [100, 50.0, 25.0, 12.5, 7.5, 5.0]
    })

    monthly_df = pd.DataFrame({
        'month': ['2024-01', '2024-02', '2024-03'],
        'total_applicants': [456, 523, 612],
        'developers': [189, 217, 245],
        'designers': [67, 78, 89]
    })

    return candidates_df, channel_df, funnel_df, monthly_df

def main():
    st.markdown('<h1 class="main-header">📌 종합 채용 대시보드</h1>', unsafe_allow_html=True)
    st.markdown("### 데이터 기반 채용 인사이트로 전략 수립")

    try:
        candidates_df, channel_df, funnel_df, monthly_df = generate_sample_data()
        candidates_df['applied_date'] = pd.to_datetime(candidates_df['applied_date'], errors='coerce')
    except Exception as e:
        st.error(f"❌ 데이터 로딩 실패: {e}")
        return

    position_filter = st.sidebar.multiselect("직무 선택", candidates_df['position'].unique(), default=candidates_df['position'].unique())
    status_filter = st.sidebar.multiselect("상태 선택", candidates_df['status'].unique(), default=candidates_df['status'].unique())

    filtered_df = candidates_df[
        (candidates_df['position'].isin(position_filter)) &
        (candidates_df['status'].isin(status_filter))
    ]

    st.write("🔎 필터링된 데이터:", filtered_df.shape)

    st.metric("총 지원자 수", len(filtered_df))

    st.subheader("지원자 샘플")
    st.dataframe(filtered_df.head(), use_container_width=True)

if __name__ == "__main__":
    main()
