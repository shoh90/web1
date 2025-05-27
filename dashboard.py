import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .sidebar-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #3b82f6;
        margin-bottom: 1rem;
    }
    
    .status-badge {
        padding: 0.2rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .status-interview { background-color: #fbbf24; color: #92400e; }
    .status-pass { background-color: #10b981; color: white; }
    .status-review { background-color: #3b82f6; color: white; }
    .status-final { background-color: #f59e0b; color: white; }
</style>
""", unsafe_allow_html=True)

# 샘플 데이터 생성 함수
@st.cache_data
def generate_sample_data():
    """채용 관련 샘플 데이터 생성"""
    
    # 지원자 데이터
    candidates_data = {
        'name': ['김민수', '이지은', '박준호', '최서영', '정하늘', '강민아', '윤성진', '조유리', '한지수', '임도현'],
        'position': ['프론트엔드 개발자', '백엔드 개발자', 'UI/UX 디자이너', '데이터 분석가', '프론트엔드 개발자', 
                    'QA 엔지니어', '백엔드 개발자', 'UI/UX 디자이너', '프로덕트 매니저', '데이터 분석가'],
        'status': ['서류 심사', '1차 면접', '최종 면접', '합격', '서류 심사', '1차 면접', '2차 면접', '합격', '서류 심사', '1차 면접'],
        'experience': ['3년', '5년', '4년', '2년', '2년', '3년', '6년', '3년', '4년', '1년'],
        'location': ['서울', '경기', '부산', '서울', '인천', '서울', '경기', '대구', '서울', '부산'],
        'resume_score': [85, 92, 78, 88, 76, 82, 89, 80, 87, 79],
        'rating': [4.5, 4.8, 4.3, 4.7, 4.2, 4.6, 4.9, 4.4, 4.8, 4.1],
        'applied_date': pd.date_range(start='2024-01-01', periods=10, freq='D'),
        'email': [f'{name.lower()}@email.com' for name in ['kimminsu', 'leejieun', 'parkjunho', 'choiseoyoung', 'jeonghaneul', 
                                                          'kangmina', 'yoonseongjin', 'joyuri', 'hanjisu', 'imdohyeon']],
        'salary_expectation': ['4000만원', '5500만원', '4200만원', '3800만원', '3500만원', '4100만원', '5800만원', '4300만원', '4800만원', '3600만원']
    }
    
    # 채널 성과 데이터
    channel_data = {
        'channel': ['사람인', '잡코리아', '링크드인', '원티드', '직접지원', '추천'],
        'applicants': [1024, 756, 234, 445, 298, 90],
        'hired': [51, 38, 18, 22, 14, 8],
        'cost': [4800000, 3200000, 1800000, 1950000, 500000, 0],
        'conversion_rate': [4.98, 5.03, 7.69, 4.94, 4.70, 8.89]
    }
    
    # 월별 트렌드 데이터
    monthly_trend = {
        'month': ['2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06'],
        'total_applicants': [456, 523, 612, 489, 567, 634],
        'developers': [189, 217, 245, 198, 234, 267],
        'designers': [67, 78, 89, 72, 85, 93],
        'marketers': [89, 98, 123, 95, 112, 128],
        'others': [111, 130, 155, 124, 136, 146]
    }
    
    # 지역별 분포 데이터
    region_data = {
        'region': ['서울', '경기', '부산', '대구', '인천', '기타'],
        'count': [1456, 723, 234, 156, 189, 278],
        'percentage': [51.2, 25.4, 8.2, 5.5, 6.6, 3.1]
    }
    
    return (
        pd.DataFrame(candidates_data),
        pd.DataFrame(channel_data),
        pd.DataFrame(monthly_trend),
        pd.DataFrame(region_data)
    )

# 데이터 로드
candidates_df, channel_df, monthly_df, region_df = generate_sample_data()

# 사이드바
st.sidebar.markdown('<div class="sidebar-header">📊 대시보드 설정</div>', unsafe_allow_html=True)

# 날짜 범위 선택
date_range = st.sidebar.date_input(
    "분석 기간 선택",
    value=(datetime.now() - timedelta(days=30), datetime.now()),
    max_value=datetime.now()
)

# 직무 필터
position_filter = st.sidebar.multiselect(
    "직무 선택",
    options=candidates_df['position'].unique(),
    default=candidates_df['position'].unique()
)

# 상태 필터
status_filter = st.sidebar.multiselect(
    "상태 선택", 
    options=candidates_df['status'].unique(),
    default=candidates_df['status'].unique()
)

# 지역 필터
location_filter = st.sidebar.multiselect(
    "지역 선택",
    options=candidates_df['location'].unique(),
    default=candidates_df['location'].unique()
)

# 데이터 필터링
filtered_df = candidates_df[
    (candidates_df['position'].isin(position_filter)) &
    (candidates_df['status'].isin(status_filter)) &
    (candidates_df['location'].isin(location_filter))
]

# 메인 헤더
st.markdown('<h1 class="main-header">🎯 종합 채용 대시보드</h1>', unsafe_allow_html=True)
st.markdown("---")

# 핵심 지표 카드
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric(
        label="📊 총 지원자",
        value="2,847",
        delta="12% ↑"
    )

with col2:
    st.metric(
        label="🎯 최종 합격",
        value="143",
        delta="5.0% 전환율"
    )

with col3:
    st.metric(
        label="⏱️ 평균 리드타임", 
        value="24일",
        delta="-3일"
    )

with col4:
    st.metric(
        label="💰 총 광고비",
        value="1,250만원", 
        delta="CPA 4,389원"
    )

with col5:
    st.metric(
        label="📝 활성 공고",
        value="28",
        delta="12개 직무"
    )

with col6:
    st.metric(
        label="⭐ 평균 점수",
        value="74점",
        delta="이력서 품질"
    )

st.markdown("---")

# 탭 생성
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 대시보드 개요", "👥 지원자 관리", "🔄 채용 퍼널", 
    "📊 채널 성과", "📍 분석 리포트", "🤖 AI 인사이트"
])

with tab1:
    st.header("📈 대시보드 개요")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📅 예정된 면접")
        upcoming_interviews = [
            {"candidate": "김민수", "position": "프론트엔드 개발자", "date": "2024-05-28", "time": "14:00", "type": "기술면접"},
            {"candidate": "이지은", "position": "백엔드 개발자", "date": "2024-05-29", "time": "10:00", "type": "최종면접"},
            {"candidate": "박준호", "position": "UI/UX 디자이너", "date": "2024-05-30", "time": "15:00", "type": "1차면접"}
        ]
        
        for interview in upcoming_interviews:
            st.info(f"**{interview['candidate']}** - {interview['position']}\n\n📅 {interview['date']} {interview['time']} | {interview['type']}")
    
    with col2:
        st.subheader("🔔 최근 활동")
        activities = [
            "김민수님이 프론트엔드 개발자에 지원 (2시간 전)",
            "이지은님 1차 면접 완료 (4시간 전)", 
            "최서영님 최종 합격 통보 (1일 전)",
            "박준호님 서류 심사 통과 (2일 전)"
        ]
        
        for activity in activities:
            st.success(activity)

with tab2:
    st.header("👥 지원자 관리")
    
    # 검색 기능
    search_term = st.text_input("🔍 지원자 검색", placeholder="이름 또는 포지션으로 검색...")
    
    if search_term:
        search_df = filtered_df[
            filtered_df['name'].str.contains(search_term, case=False) |
            filtered_df['position'].str.contains(search_term, case=False)
        ]
    else:
        search_df = filtered_df
    
    # 지원자 목록 표시
    for idx, row in search_df.iterrows():
        with st.expander(f"👤 {row['name']} - {row['position']}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**📧 이메일:** {row['email']}")
                st.write(f"**🏢 경력:** {row['experience']}")
                st.write(f"**📍 지역:** {row['location']}")
                
            with col2:
                st.write(f"**⭐ 평점:** {row['rating']}")
                st.write(f"**📊 이력서 점수:** {row['resume_score']}점")
                st.write(f"**💰 희망연봉:** {row['salary_expectation']}")
                
            with col3:
                # 상태 배지
                status_color = {
                    '서류 심사': 'blue', '1차 면접': 'orange', 
                    '2차 면접': 'orange', '최종 면접': 'red', '합격': 'green'
                }
                st.markdown(f"**📋 상태:** :{status_color.get(row['status'], 'gray')}[{row['status']}]")
                
                # 진행 바
                st.progress(row['resume_score'] / 100)
                
                # 액션 버튼
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    st.button("📧 이메일", key=f"email_{idx}")
                with col_btn2:
                    st.button("📅 면접일정", key=f"schedule_{idx}")

with tab3:
    st.header("🔄 채용 퍼널 분석")
    
    # 퍼널 데이터
    funnel_data = {
        'stage': ['지원자', '서류 합격', '면접자', '최종 합격'],
        'count': [2847, 1423, 428, 143],
        'percentage': [100, 50.0, 15.0, 5.0]
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 퍼널 차트
        fig_funnel = go.Figure(go.Funnel(
            y=funnel_data['stage'],
            x=funnel_data['count'],
            textinfo="value+percent initial",
            marker=dict(color=['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6'])
        ))
        fig_funnel.update_layout(title="채용 퍼널", height=400)
        st.plotly_chart(fig_funnel, use_container_width=True)
    
    with col2:
        # 전환율 분석
        st.subheader("📊 단계별 전환율")
        conversion_rates = [
            ("지원 → 서류", 50.0),
            ("서류 → 면접", 30.1), 
            ("면접 → 합격", 33.4),
            ("전체 전환율", 5.0)
        ]
        
        for stage, rate in conversion_rates:
            st.metric(stage, f"{rate}%")
            st.progress(rate / 100)

with tab4:
    st.header("📊 채널별 성과 분석")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 채널별 지원자 수
        fig_channel = px.bar(
            channel_df, 
            x='channel', 
            y='applicants',
            title="채널별 지원자 수",
            color='applicants',
            color_continuous_scale='viridis'
        )
        st.plotly_chart(fig_channel, use_container_width=True)
    
    with col2:
        # 채널별 전환율
        fig_conversion = px.bar(
            channel_df,
            x='channel',
            y='conversion_rate', 
            title="채널별 전환율",
            color='conversion_rate',
            color_continuous_scale='plasma'
        )
        st.plotly_chart(fig_conversion, use_container_width=True)
    
    # 채널 성과 테이블
    st.subheader("📋 채널별 상세 성과")
    
    # CPA 계산
    channel_df['cpa'] = channel_df['cost'] / channel_df['hired']
    channel_df['cpa'] = channel_df['cpa'].fillna(0).astype(int)
    
    display_df = channel_df[['channel', 'applicants', 'hired', 'conversion_rate', 'cost', 'cpa']].copy()
    display_df.columns = ['채널', '지원자 수', '합격자 수', '전환율(%)', '광고비(원)', 'CPA(원)']
    display_df['광고비(원)'] = display_df['광고비(원)'].apply(lambda x: f"{x:,}")
    display_df['CPA(원)'] = display_df['CPA(원)'].apply(lambda x: f"{x:,}" if x > 0 else "0")
    
    st.dataframe(display_df, use_container_width=True)

with tab5:
    st.header("📍 분석 리포트")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 지역별 분포
        fig_region = px.pie(
            region_df, 
            values='count', 
            names='region',
            title="지역별 지원자 분포"
        )
        st.plotly_chart(fig_region, use_container_width=True)
        
    with col2:
        # 월별 트렌드
        fig_trend = px.line(
            monthly_df,
            x='month',
            y=['total_applicants', 'developers', 'designers', 'marketers'],
            title="월별 지원자 트렌드"
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    
    # 경력별 분포
    experience_data = candidates_df['experience'].value_counts()
    fig_exp = px.bar(
        x=experience_data.index,
        y=experience_data.values,
        title="경력별 지원자 분포",
        labels={'x': '경력', 'y': '지원자 수'}
    )
    st.plotly_chart(fig_exp, use_container_width=True)

with tab6:
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
            st.info(f"💡 {insight}")
    
    with col2:
        st.subheader("📈 개선 권장사항")
        recommendations = [
            "링크드인 채널 투자 확대 및 타겟팅 강화",
            "이력서 첨삭 서비스 활용률 증대 방안 마련",
            "80점 미만 지원자 대상 사전 가이드 제공", 
            "경력직 중심의 채용 전략 수립 검토"
        ]
        
        for rec in recommendations:
            st.success(f"🎯 {rec}")
    
    # 이력서 점수 분포와 합격률 관계
    st.subheader("📊 이력서 점수별 합격률 분석")
    
    score_ranges = ['50-59', '60-69', '70-79', '80-89', '90-100']
    pass_rates = [1.2, 2.4, 4.2, 9.4, 18.7]
    
    fig_score = px.scatter(
        x=score_ranges,
        y=pass_rates,
        size=[234, 445, 567, 356, 123],
        title="점수 구간별 합격률",
        labels={'x': '점수 구간', 'y': '합격률(%)'}
    )
    st.plotly_chart(fig_score, use_container_width=True)

# 푸터
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6b7280; font-size: 0.9rem;'>
    🚀 Advanced Recruitment Dashboard | 데이터 기반 채용 의사결정을 위한 통합 플랫폼
</div>
""", unsafe_allow_html=True)
