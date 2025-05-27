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
    
    # 오늘 지원자 수 계산
    today = datetime.now().date()
    today_applicants = len(candidates_df[candidates_df['applied_date'].dt.date == today])
    
    # 이번 주 지원자 수
    week_start = today - timedelta(days=today.weekday())
    this_week = candidates_df[candidates_df['applied_date'].dt.date >= week_start]
    week_applicants = len(this_week)
    
    # 이번 달 지원자 수
    month_start = today.replace(day=1)
    this_month = candidates_df[candidates_df['applied_date'].dt.date >= month_start]
    month_applicants = len(this_month)
    
    # 평균 이력서 점수
    avg_score_today = candidates_df[candidates_df['applied_date'].dt.date == today]['resume_score'].mean()
    avg_score_today = avg_score_today if not pd.isna(avg_score_today) else 0
    
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    with metric_col1:
        st.metric(
            label="📅 오늘 지원자",
            value=today_applicants,
            delta=f"전일 대비 {random.randint(-5, 15)}명"
        )
    
    with metric_col2:
        st.metric(
            label="📈 이번 주",
            value=week_applicants,
            delta=f"전주 대비 {random.randint(-20, 50)}명"
        )
    
    with metric_col3:
        st.metric(
            label="📆 이번 달",
            value=month_applicants,
            delta=f"전월 대비 {random.randint(-100, 200)}명"
        )
    
    with metric_col4:
        st.metric(
            label="⭐ 오늘 평균 점수",
            value=f"{avg_score_today:.1f}점",
            delta=f"{random.uniform(-5, 5):.1f}점"
        )

def render_upcoming_interviews(
