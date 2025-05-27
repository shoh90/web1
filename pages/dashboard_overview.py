"""
대시보드 개요 페이지 (단독 실행 버전)
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

def render_dashboard_overview(candidates_df: pd.DataFrame, interview_df: pd.DataFrame):
    st.header("\ud83d\udcc8 \ub300신대수 \uac1c요")
    st.markdown("### \uc624\ub298\uc758 \ucc44용 \ud604\ud669과 \uc8fc요 \ud65c동을 \ud55c눈에 \ud655인하세요")

    col1, col2 = st.columns([2, 1])

    with col1:
        render_today_metrics(candidates_df)
        render_upcoming_interviews(interview_df)

    with col2:
        render_recent_activities(candidates_df)
        render_today_todos()
        render_notifications(candidates_df)

def render_today_metrics(candidates_df: pd.DataFrame):
    st.subheader("\ud83d\udcca \uc624\ub298\uc758 \uc8fc요 \uc9c0표")
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
        st.metric("\ud83d\udcc5 \uc624\ub298 \uc9c0원자", today_applicants)
    with col2:
        st.metric("\ud83d\udcc8 \uc774\ubcf8 \uc8fc", week_applicants)
    with col3:
        st.metric("\ud83d\udcc6 \uc774\ubcf8 \ub2ec", month_applicants)
    with col4:
        st.metric("\u2b50 \ud604재 \ud3c9균 \uc810수", f"{avg_score_today:.1f}점")

def render_upcoming_interviews(interview_df: pd.DataFrame):
    st.subheader("\ud83d\udcc5 \uc608정된 \uba74접 \uc77c정")
    interview_df['interview_date'] = pd.to_datetime(interview_df['interview_date'], errors='coerce')
    upcoming = interview_df[interview_df['interview_date'] >= datetime.now()].sort_values('interview_date').head(5)

    if upcoming.empty:
        st.info("예정된 면접이 없습니다.")
    else:
        for _, row in upcoming.iterrows():
            st.markdown(f"- **{row['name']}** ({row['position']}) – {row['interview_date'].strftime('%Y-%m-%d')}")

def render_recent_activities(candidates_df: pd.DataFrame):
    st.subheader("\ud83d\udd52 \uacbd쟁 \uc9c0원자 \ud65c동")
    recent = candidates_df.sort_values('applied_date', ascending=False).head(5)

    for _, row in recent.iterrows():
        st.markdown(f"- {row['applied_date'].strftime('%Y-%m-%d')} | **{row['name']}** ({row['position']}) – 점수: {row['resume_score']}")

def render_today_todos():
    st.subheader("\ud83d\udcdd \uc624\ub298의 \ud560 \uc77c")
    st.checkbox("이력서 검토 5건")
    st.checkbox("면접 일정 조율")
    st.checkbox("채용 채널 성과 분석")
    st.checkbox("최종 합격자 통보")

def render_notifications(candidates_df: pd.DataFrame):
    st.subheader("\ud83d\udd14 \uc8fc의할 \uc9c0원자")
    high_score = candidates_df[candidates_df['resume_score'] >= 90].head(3)

    if high_score.empty:
        st.info("알림 대상 지원자가 없습니다.")
    else:
        for _, row in high_score.iterrows():
            st.warning(f"⚠️ {row['name']} – 이력서 점수 {row['resume_score']}점 / {row['position']}")

if __name__ == "__main__":
    st.set_page_config(page_title="대시보드 개요", layout="wide")

    st.markdown("<h1 style='text-align:center;'>📈 대시보드 개요</h1>", unsafe_allow_html=True)

    # 샘플 데이터 생성
    sample_candidates = pd.DataFrame({
        'name': ['김민수', '이지은', '박준호'],
        'position': ['프론트엔드 개발자', '디자이너', '데이터 분석가'],
        'status': ['1차 면접', '최종 면접', '서류 심사'],
        'applied_date': [datetime.now(), datetime.now() - timedelta(days=1), datetime.now() - timedelta(days=2)],
        'resume_score': [85, 92, 78],
        'rating': [4.7, 4.9, 4.3],
        'email': ['minsu@email.com', 'jieun@email.com', 'junho@email.com']
    })

    sample_interviews = sample_candidates[sample_candidates['status'].isin(['1차 면접', '2차 면접', '최종 면접'])].copy()
    sample_interviews['interview_date'] = [datetime.now() + timedelta(days=i) for i in range(1, len(sample_interviews)+1)]

    render_dashboard_overview(sample_candidates, sample_interviews)
