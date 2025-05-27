"""
대시보드 개요 페이지
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random


def render_dashboard_overview(candidates_df: pd.DataFrame, interview_df: pd.DataFrame):
    """대시보드 개요 페이지 렌더링"""

    st.header("📈 대시보드 개요")
    st.markdown("### 오늘의 채용 현황과 주요 활동을 한눈에 확인하세요")

    # 오늘의 주요 지표
    col1, col2 = st.columns([2, 1])

    with col1:
        render_today_metrics(candidates_df)
        render_upcoming_interviews(interview_df)

    with col2:
        render_recent_activities(candidates_df)
        render_today_todos()
        render_notifications(candidates_df)


def render_today_metrics(candidates_df: pd.DataFrame):
    """오늘의 주요 지표"""
    st.subheader("📊 오늘의 주요 지표")

    today = datetime.now().date()
    today_applicants = len(candidates_df[candidates_df['applied_date'].dt.date == today])

    week_start = today - timedelta(days=today.weekday())
    this_week = candidates_df[candidates_df['applied_date'].dt.date >= week_start]
    week_applicants = len(this_week)

    month_start = today.replace(day=1)
    this_month = candidates_df[candidates_df['applied_date'].dt.date >= month_start]
    month_applicants = len(this_month)

    avg_score_today = candidates_df[candidates_df['applied_date'].dt.date == today]['resume_score'].mean()
    avg_score_today = avg_score_today if not pd.isna(avg_score_today) else 0

    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

    with metric_col1:
        st.metric("📅 오늘 지원자", today_applicants, f"{random.randint(-5, 15)}명 변화")

    with metric_col2:
        st.metric("📈 이번 주", week_applicants, f"{random.randint(-20, 50)}명 변화")

    with metric_col3:
        st.metric("📆 이번 달", month_applicants, f"{random.randint(-100, 200)}명 변화")

    with metric_col4:
        st.metric("⭐ 오늘 평균 점수", f"{avg_score_today:.1f}점", f"{random.uniform(-5, 5):.1f}점 변화")


def render_upcoming_interviews(interview_df: pd.DataFrame):
    """예정된 면접 일정"""
    st.subheader("📅 예정된 면접 일정")

    upcoming = interview_df[interview_df['interview_date'] >= datetime.now()]
    upcoming = upcoming.sort_values('interview_date').head(5)

    if upcoming.empty:
        st.info("예정된 면접이 없습니다.")
    else:
        for _, row in upcoming.iterrows():
            st.markdown(
                f"- **{row['name']}** ({row['position']}) – {row['interview_date'].strftime('%Y-%m-%d')}"
            )


def render_recent_activities(candidates_df: pd.DataFrame):
    """최근 지원자 활동"""
    st.subheader("🕒 최근 지원자 활동")

    recent = candidates_df.sort_values('applied_date', ascending=False).head(5)

    for _, row in recent.iterrows():
        st.markdown(
            f"- {row['applied_date'].strftime('%Y-%m-%d')} | **{row['name']}** ({row['position']}) – 점수: {row['resume_score']}"
        )


def render_today_todos():
    """오늘의 할 일 (예시)"""
    st.subheader("📝 오늘의 할 일")
    st.checkbox("이력서 검토 5건")
    st.checkbox("면접 일정 조율")
    st.checkbox("채용 채널 성과 분석")
    st.checkbox("최종 합격자 통보")


def render_notifications(candidates_df: pd.DataFrame):
    """지원자 알림"""
    st.subheader("🔔 주의할 지원자")

    high_score = candidates_df[candidates_df['resume_score'] >= 90].head(3)

    if high_score.empty:
        st.info("알림 대상 지원자가 없습니다.")
    else:
        for _, row in high_score.iterrows():
            st.warning(f"⚠️ {row['name']} – 이력서 점수 {row['resume_score']}점 / {row['position']}")
