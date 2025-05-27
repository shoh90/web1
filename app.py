"""
📌종합 채용 대시보드
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

# 커스텀 CSS
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
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .candidate-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .insights-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    .recommendation-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 데이터 생성 함수
@st.cache_data
def generate_sample_data():
    """샘플 데이터 생성"""
    
    # 지원자 데이터
    names = ['김민수', '이지은', '박준호', '최서영', '정하늘', '강민아', '윤성진', '조유리', 
             '한지수', '임도현', '송민철', '오수진', '배현우', '신예린', '장태현', '문소영']
    
    positions = ['프론트엔드 개발자', '백엔드 개발자', 'UI/UX 디자이너', '데이터 분석가', 
                'QA 엔지니어', '프로덕트 매니저', 'DevOps 엔지니어']
    
    statuses = ['서류 심사', '1차 면접', '2차 면접', '최종 면접', '합격', '불합격']
    experiences = ['신입', '1년', '2년', '3년', '4년', '5년', '6년', '7년 이상']
    locations = ['서울', '경기', '부산', '대구', '인천', '광주', '대전']
    sources = ['사람인', '잡코리아', '링크드인', '원티드', '직접지원', '추천']
    
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
            'email': f'{name.lower().replace(" ", "")}@email.com',
            'salary_expectation': f'{random.randint(3000, 8000)}만원',
            'skills': random.choice(['Python, Django', 'React, Node.js', 'Figma, Sketch', 'SQL, Tableau']),
            'source': random.choice(sources)
        })
    
    # 채널 성과 데이터
    channel_data = {
        'channel': ['사람인', '잡코리아', '링크드인', '원티드', '직접지원', '추천'],
        'applicants': [1024, 756, 234, 445, 298, 90],
        'hired': [51, 38, 18, 22, 14, 8],
        'cost': [4800000, 3200000, 1800000, 1950000, 500000, 0],
        'conversion_rate': [4.98, 5.03, 7.69, 4.94, 4.70, 8.89]
    }
    
    # 퍼널 데이터
    funnel_data = {
        'stage': ['총 지원자', '서류 통과', '1차 면접', '2차 면접', '최종 면접', '최종 합격'],
        'count': [3014, 1507, 754, 377, 226, 151],
        'percentage': [100, 50.0, 25.0, 12.5, 7.5, 5.0]
    }
    
    # 월별 트렌드 데이터
    monthly_data = {
        'month': ['2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06'],
        'total_applicants': [456, 523, 612, 489, 567, 634],
        'developers': [189, 217, 245, 198, 234, 267],
        'designers': [67, 78, 89, 72, 85, 93]
    }
    
    return (
        pd.DataFrame(candidates_data),
        pd.DataFrame(channel_data),
        pd.DataFrame(funnel_data),
        pd.DataFrame(monthly_data)
    )

# 메인 앱
def main():
    # 헤더
    st.markdown('<h1 class="main-header">📌 종합 채용 대시보드</h1>', unsafe_allow_html=True)
    st.markdown("### 데이터 기반 채용 인사이트로 더 나은 인재 확보 전략을 수립하세요")
    
    # 데이터 로드
    candidates_df, channel_df, funnel_df, monthly_df = generate_sample_data()
    
    # 사이드바
    st.sidebar.header("📊 대시보드 설정")
    
    # 필터 옵션
    position_filter = st.sidebar.multiselect(
        "직무 선택",
        options=candidates_df['position'].unique(),
        default=candidates_df['position'].unique()
    )
    
    status_filter = st.sidebar.multiselect(
        "상태 선택", 
        options=candidates_df['status'].unique(),
        default=candidates_df['status'].unique()
    )
    
    # 데이터 필터링
    filtered_df = candidates_df[
        (candidates_df['position'].isin(position_filter)) &
        (candidates_df['status'].isin(status_filter))
    ]
    
    st.markdown("---")
    
    # 핵심 지표
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric("📊 총 지원자", f"{len(candidates_df):,}", "12% ↑")
    
    with col2:
        hired_count = len(candidates_df[candidates_df['status'] == '합격'])
        conversion_rate = (hired_count / len(candidates_df) * 100) if len(candidates_df) > 0 else 0
        st.metric("🎯 최종 합격", f"{hired_count}", f"{conversion_rate:.1f}% 전환율")
    
    with col3:
        st.metric("⏱️ 평균 리드타임", "24일", "-3일")
    
    with col4:
        total_cost = channel_df['cost'].sum()
        st.metric("💰 총 광고비", f"{total_cost//10000:,}만원", "CPA 4,389원")
    
    with col5:
        st.metric("📝 활성 공고", "28", "12개 직무")
    
    with col6:
        avg_score = candidates_df['resume_score'].mean()
        st.metric("⭐ 평균 점수", f"{avg_score:.0f}점", "이력서 품질")
    
    st.markdown("---")
    
    # 탭 구성
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📈 대시보드 개요", "👥 지원자 관리", "🔄 채용 퍼널", 
        "📊 채널 성과", "📍 분석 리포트", "🤖 AI 인사이트"
    ])
    
    with tab1:
        render_dashboard_overview(filtered_df)
    
    with tab2:
        render_candidate_management(filtered_df)
    
    with tab3:
        render_funnel_analysis(funnel_df)
    
    with tab4:
        render_channel_performance(channel_df)
    
    with tab5:
        render_analytics_report(monthly_df, candidates_df)
    
    with tab6:
        render_ai_insights(candidates_df, channel_df)

def render_dashboard_overview(filtered_df):
    """대시보드 개요"""
    st.header("📈 대시보드 개요")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📅 예정된 면접")
        
        interview_candidates = filtered_df[filtered_df['status'].isin(['1차 면접', '2차 면접', '최종 면접'])].head(3)
        
        for _, candidate in interview_candidates.iterrows():
            interview_date = datetime.now() + timedelta(days=random.randint(1, 7))
            st.markdown(f"""
            <div class="candidate-card">
                <strong>👤 {candidate['name']}</strong> - {candidate['position']}<br>
                📅 {interview_date.strftime('%Y-%m-%d')} 14:00 | {candidate['status']}<br>
                📧 {candidate['email']} | ⭐ {candidate['rating']}
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("🔔 최근 활동")
        
        activities = [
            "새로운 지원자가 프론트엔드 개발자에 지원 (2시간 전)",
            "김민수님 1차 면접 완료 (4시간 전)", 
            "이지은님 최종 합격 통보 (1일 전)",
            "박준호님 서류 심사 통과 (2일 전)"
        ]
        
        for activity in activities:
            st.success(f"• {activity}")

def render_candidate_management(filtered_df):
    """지원자 관리"""
    st.header("👥 지원자 관리")
    
    # 검색
    search_term = st.text_input("🔍 지원자 검색", placeholder="이름 또는 포지션으로 검색...")
    
    if search_term:
        search_df = filtered_df[
            filtered_df['name'].str.contains(search_term, case=False, na=False) |
            filtered_df['position'].str.contains(search_term, case=False, na=False)
        ]
    else:
        search_df = filtered_df
    
    # 상태별 요약
    st.subheader("📊 현재 상태 분포")
    status_counts = search_df['status'].value_counts()
    
    status_cols = st.columns(len(status_counts))
    for i, (status, count) in enumerate(status_counts.items()):
        with status_cols[i]:
            st.metric(status, count)
    
    # 지원자 목록
    st.subheader(f"📋 지원자 목록 (총 {len(search_df)}명)")
    
    for _, candidate in search_df.head(10).iterrows():
        with st.expander(f"👤 {candidate['name']} - {candidate['position']} (점수: {candidate['resume_score']}점)"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**📧 이메일:** {candidate['email']}")
                st.write(f"**🏢 경력:** {candidate['experience']}")
                st.write(f"**📍 지역:** {candidate['location']}")
                
            with col2:
                st.write(f"**⭐ 평점:** {candidate['rating']}")
                st.write(f"**📊 점수:** {candidate['resume_score']}점")
                st.write(f"**💰 희망연봉:** {candidate['salary_expectation']}")
                
            with col3:
                st.write(f"**📋 상태:** {candidate['status']}")
                st.write(f"**📅 지원일:** {candidate['applied_date'].strftime('%Y-%m-%d')}")
                
                progress = candidate['resume_score'] / 100
                st.progress(progress, text=f"점수: {candidate['resume_score']}점")

def render_funnel_analysis(funnel_df):
    """채용 퍼널 분석"""
    st.header("🔄 채용 퍼널 분석")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 퍼널 차트
        fig_funnel = go.Figure(go.Funnel(
            y=funnel_df['stage'],
            x=funnel_df['count'],
            texttemplate="%{label}<br>%{value:,}<br>(%{percentInitial})",
            textfont={"size": 12},
            marker={"color": ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4']}
        ))
        
        fig_funnel.update_layout(title="채용 퍼널", height=500)
        st.plotly_chart(fig_funnel, use_container_width=True)
    
    with col2:
        # 전환율 분석
        st.subheader("📊 단계별 전환율")
        
        conversion_rates = [
            ("지원 → 서류", 50.0),
            ("서류 → 1차면접", 50.0), 
            ("1차 → 2차면접", 50.0),
            ("2차 → 최종면접", 60.0),
            ("최종 → 합격", 67.0)
        ]
        
        for stage, rate in conversion_rates:
            st.metric(stage, f"{rate}%")
            st.progress(rate / 100)

def render_channel_performance(channel_df):
    """채널 성과 분석"""
    st.header("📊 채널별 성과 분석")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 채널별 지원자 수
        fig_applicants = px.bar(
            channel_df, 
            x='channel', 
            y='applicants',
            title="채널별 지원자 수",
            color='applicants',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_applicants, use_container_width=True)
    
    with col2:
        # 채널별 전환율
        fig_conversion = px.bar(
            channel_df,
            x='channel',
            y='conversion_rate', 
            title="채널별 전환율 (%)",
            color='conversion_rate',
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig_conversion, use_container_width=True)
    
    # 채널 성과 테이블
    st.subheader("📋 채널별 상세 성과")
    
    channel_detail = channel_df.copy()
    channel_detail['CPA'] = np.where(
        channel_detail['hired'] > 0,
        channel_detail['cost'] / channel_detail['hired'],
        0
    ).astype(int)
    
    display_channels = channel_detail[['channel', 'applicants', 'hired', 'conversion_rate', 'cost', 'CPA']].copy()
    display_channels.columns = ['채널', '지원자 수', '합격자 수', '전환율(%)', '광고비(원)', 'CPA(원)']
    
    st.dataframe(display_channels, use_container_width=True)

def render_analytics_report(monthly_df, candidates_df):
    """분석 리포트"""
    st.header("📍 분석 리포트")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 월별 트렌드
        fig_trend = px.line(
            monthly_df,
            x='month',
            y=['total_applicants', 'developers', 'designers'],
            title="월별 지원자 트렌드"
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with col2:
        # 이력서 점수 분포
        fig_score = px.histogram(
            candidates_df,
            x='resume_score',
            nbins=15,
            title="이력서 점수 분포"
        )
        st.plotly_chart(fig_score, use_container_width=True)
    
    # 경력별 분포
    experience_counts = candidates_df['experience'].value_counts()
    fig_exp = px.bar(
        x=experience_counts.index,
        y=experience_counts.values,
        title="경력별 지원자 분포"
    )
    st.plotly_chart(fig_exp, use_container_width=True)

def render_ai_insights(candidates_df, channel_df):
    """AI 인사이트"""
    st.header("🤖 AI 채용 인사이트")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔍 주요 발견사항")
        
        insights = [
            "80점 이상 이력서의 합격률이 평균 대비 2.3배 높음",
            "링크드인 채널의 전환율이 7.69%로 가장 높음", 
            "경력 4-6년 구간의 지원자 품질 점수 최고",
            "자기소개서 800자 이상 작성 시 합격률 최대화"
        ]
        
        for insight in insights:
            st.markdown(f"""
            <div class="insights-card">
                💡 {insight}
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("📈 개선 권장사항")
        
        recommendations = [
            "링크드인 채널 투자 확대 및 타겟팅 강화",
            "이력서 첨삭 서비스 활용률 증대 방안 마련",
            "80점 미만 지원자 대상 사전 가이드 제공", 
            "경력직 중심의 채용 전략 수립 검토"
        ]
        
        for rec in recommendations:
            st.markdown(f"""
            <div class="recommendation-card">
                🎯 {rec}
            </div>
            """, unsafe_allow_html=True)
    
    # 이력서 점수별 합격률 분석
    st.subheader("📊 이력서 점수별 합격률 분석")
    
    score_ranges = ['50-59', '60-69', '70-79', '80-89', '90-100']
    pass_rates = [1.2, 2.4, 4.2, 9.4, 18.7]
    
    fig_score = px.scatter(
        x=score_ranges,
        y=pass_rates,
        size=[234, 445, 567, 356, 123],
        title="점수 구간별 합격률"
    )
    st.plotly_chart(fig_score, use_container_width=True)

if __name__ == "__main__":
    main()
