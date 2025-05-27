"""
대시보드 개요 페이지 (CSV 연동 + 업로드 + 상세 보기 확장)
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
import numpy as np

DEFAULT_CSV_PATH = "premium_remember_jobs_20250527_220128.csv"

def render_dashboard_overview(candidates_df: pd.DataFrame, interview_df: pd.DataFrame):
    st.header("📊 대시보드 개요")
    st.markdown("### 오늘의 채용 현황과 주요 활동을 한눈에 확인하세요")

    # 🔍 필터 추가
    with st.sidebar:
        st.subheader("🔧 필터 설정")
        position_options = candidates_df['position'].unique().tolist()
        position_filter = st.multiselect("직무 선택", position_options, default=position_options)

        status_options = candidates_df['status'].unique().tolist()
        status_filter = st.multiselect("진행 상태 선택", status_options, default=status_options)

    filtered_df = candidates_df[
        (candidates_df['position'].isin(position_filter)) &
        (candidates_df['status'].isin(status_filter))
    ]

    filtered_interviews = interview_df[interview_df['name'].isin(filtered_df['name'])]

    col1, col2 = st.columns([2, 1])

    with col1:
        render_today_metrics(filtered_df)
        render_upcoming_interviews(filtered_interviews)

    with col2:
        render_recent_activities(filtered_df)
        render_today_todos()
        render_notifications(filtered_df)

    st.markdown("---")
    render_candidate_detail_table(filtered_df)

def render_today_metrics(candidates_df: pd.DataFrame):
    st.subheader("📊 오늘의 주요 지표")
    today = datetime.now().date()
    candidates_df['applied_date'] = pd.to_datetime(candidates_df['applied_date'], errors='coerce')
    today_applicants = len(candidates_df[candidates_df['applied_date'].dt.date == today])

    week_start = today - timedelta(days=today.weekday())
    week_applicants = len(candidates_df[candidates_df['applied_date'].dt.date >= week_start])

    month_start = today.replace(day=1)
    month_applicants = len(candidates_df[candidates_df['applied_date'].dt.date >= month_start])

    avg_score_today = candidates_df[candidates_df['applied_date'].dt.date == today]['resume_score'].mean()
    avg_score_today = avg_score_today if not pd.isna(avg_score_today) else 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📅 오늘 지원자", today_applicants)
    with col2:
        st.metric("📈 이번 주", week_applicants)
    with col3:
        st.metric("📆 이번 달", month_applicants)
    with col4:
        st.metric("⭐ 현재 평균 점수", f"{avg_score_today:.1f}점")

def render_upcoming_interviews(interview_df: pd.DataFrame):
    st.subheader("📅 예정된 면접 일정")
    interview_df['interview_date'] = pd.to_datetime(interview_df['interview_date'], errors='coerce')
    upcoming = interview_df[interview_df['interview_date'] >= datetime.now()].sort_values('interview_date').head(5)

    if upcoming.empty:
        st.info("예정된 면접이 없습니다.")
    else:
        for _, row in upcoming.iterrows():
            st.markdown(f"- **{row['name']}** ({row['position']}) – {row['interview_date'].strftime('%Y-%m-%d')}")

def render_recent_activities(candidates_df: pd.DataFrame):
    st.subheader("🕒 최근 지원자 활동")
    recent = candidates_df.sort_values('applied_date', ascending=False).head(5)

    for _, row in recent.iterrows():
        st.markdown(f"- {row['applied_date'].strftime('%Y-%m-%d')} | **{row['name']}** ({row['position']}) – 점수: {row['resume_score']}")

def render_today_todos():
    st.subheader("📝 오늘의 할 일")
    st.checkbox("이력서 검토 5건")
    st.checkbox("면접 일정 조율")
    st.checkbox("채용 채널 성과 분석")
    st.checkbox("최종 합격자 통보")

def render_notifications(candidates_df: pd.DataFrame):
    st.subheader("🔔 주의할 지원자")
    high_score = candidates_df[candidates_df['resume_score'] >= 90].head(3)

    if high_score.empty:
        st.info("알림 대상 지원자가 없습니다.")
    else:
        for _, row in high_score.iterrows():
            st.warning(f"⚠️ {row['name']} – 이력서 점수 {row['resume_score']}점 / {row['position']}")

def render_candidate_detail_table(filtered_df):
    st.subheader("📋 지원자 상세 보기")
    for _, row in filtered_df.iterrows():
        with st.expander(f"👤 {row['name']} - {row['position']} (점수: {row['resume_score']})"):
            st.write(f"📧 이메일: {row['email']}")
            st.write(f"📆 지원일: {row['applied_date'].strftime('%Y-%m-%d') if pd.notnull(row['applied_date']) else 'N/A'}")
            st.write(f"⭐ 평점: {row['rating']}")
            st.write(f"📋 상태: {row['status']}")

def load_csv_data(uploaded_file):
    raw_df = pd.read_csv(uploaded_file)
    df_dashboard = pd.DataFrame({
        'name': raw_df['회사명'],
        'position': raw_df['직무'],
        'status': np.random.choice(['서류 심사', '1차 면접', '2차 면접', '최종 면접', '합격', '불합격'], len(raw_df)),
        'applied_date': pd.to_datetime(raw_df['공고시작일'], errors='coerce'),
        'resume_score': np.random.randint(70, 95, len(raw_df)),
        'rating': np.round(np.random.uniform(3.5, 5.0, len(raw_df)), 1),
        'email': raw_df['회사명'].str.replace(" ", "").str.lower() + "@email.com"
    })
    interview_df = df_dashboard[df_dashboard['status'].isin(['1차 면접', '2차 면접', '최종 면접'])].copy()
    interview_df['interview_date'] = [datetime.now() + timedelta(days=i) for i in range(1, len(interview_df)+1)]
    return df_dashboard, interview_df

if __name__ == "__main__":
    st.set_page_config(page_title="📊 대시보드 개요", layout="wide")
    st.markdown("<h1 style='text-align:center;'>📊 대시보드 개요 (CSV 업로드 + 상세 보기)</h1>", unsafe_allow_html=True)

    st.sidebar.title("📁 CSV 업로드")
    uploaded_file = st.sidebar.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

    try:
        if uploaded_file:
            df_dashboard, sample_interviews = load_csv_data(uploaded_file)
        else:
            raw_df = pd.read_csv(DEFAULT_CSV_PATH)
            df_dashboard, sample_interviews = load_csv_data(DEFAULT_CSV_PATH)

        render_dashboard_overview(df_dashboard, sample_interviews)
    except Exception as e:
        st.error(f"❌ 데이터 로딩 실패: {e}")
