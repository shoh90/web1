"""
채용 대시보드 차트 생성 모듈
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import streamlit as st

from config import COLORS, STATUS_COLORS, CHART_CONFIG

class ChartGenerator:
    """차트 생성을 담당하는 클래스"""
    
    def __init__(self):
        self.colors = COLORS
        self.status_colors = STATUS_COLORS
        self.chart_config = CHART_CONFIG
    
    def create_funnel_chart(self, funnel_df: pd.DataFrame, title: str = "채용 퍼널") -> go.Figure:
        """채용 퍼널 차트 생성"""
        fig = go.Figure(go.Funnel(
            y=funnel_df['stage'],
            x=funnel_df['count'],
            texttemplate="%{label}<br>%{value:,}<br>(%{percentInitial})",
            textfont={"size": 14, "color": "white"},
            connector={
                "line": {
                    "color": self.colors['primary'], 
                    "dash": "dot", 
                    "width": 3
                }
            },
            marker={
                "color": self.chart_config['funnel']['colors'],
                "line": {
                    "color": "white",
                    "width": 2
                }
            }
        ))
        
        fig.update_layout(
            title={
                'text': title,
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': self.colors['dark']}
            },
            height=self.chart_config['funnel']['height'],
            font=dict(size=12),
            showlegend=False,
            margin=dict(l=20, r=20, t=60, b=20)
        )
        
        return fig
    
    def create_conversion_rate_chart(self, funnel_df: pd.DataFrame) -> go.Figure:
        """단계별 전환율 차트"""
        conversion_data = []
        
        for i in range(1, len(funnel_df)):
            current_count = funnel_df.iloc[i]['count']
            previous_count = funnel_df.iloc[i-1]['count']
            rate = (current_count / previous_count * 100) if previous_count > 0 else 0
            
            conversion_data.append({
                'stage': f"{funnel_df.iloc[i-1]['stage']} → {funnel_df.iloc[i]['stage']}",
                'rate': rate
            })
        
        conv_df = pd.DataFrame(conversion_data)
        
        fig = px.bar(
            conv_df,
            y='stage',
            x='rate',
            orientation='h',
            title="단계별 전환율 (%)",
            color='rate',
            color_continuous_scale='Viridis',
            text='rate'
        )
        
        fig.update_traces(
            texttemplate='%{text:.1f}%',
            textposition='outside'
        )
        
        fig.update_layout(
            height=400,
            xaxis_title="전환율 (%)",
            yaxis_title="단계",
            showlegend=False
        )
        
        return fig
    
    def create_channel_performance_chart(self, channel_df: pd.DataFrame) -> Dict[str, go.Figure]:
        """채널 성과 관련 차트들"""
        charts = {}
        
        # 1. 채널별 지원자 수
        charts['applicants'] = px.bar(
            channel_df,
            x='channel',
            y='applicants',
            title="채널별 지원자 수",
            color='applicants',
            color_continuous_scale='Blues',
            text='applicants'
        )
        charts['applicants'].update_traces(
            texttemplate='%{text:,}',
            textposition='outside'
        )
        charts['applicants'].update_layout(height=400)
        
        # 2. 채널별 전환율
        charts['conversion'] = px.bar(
            channel_df,
            x='channel',
            y='conversion_rate',
            title="채널별 전환율 (%)",
            color='conversion_rate',
            color_continuous_scale='Reds',
            text='conversion_rate'
        )
        charts['conversion'].update_traces(
            texttemplate='%{text:.1f}%',
            textposition='outside'
        )
        charts['conversion'].update_layout(height=400)
        
        # 3. 채널 효율성 매트릭스 (버블 차트)
        charts['efficiency'] = px.scatter(
            channel_df,
            x='conversion_rate',
            y='applicants',
            size='hired',
            color='cpa',
            hover_name='channel',
            title="채널 효율성 매트릭스",
            labels={
                'conversion_rate': '전환율 (%)',
                'applicants': '지원자 수',
                'cpa': 'CPA (원)'
            },
            size_max=60
        )
        charts['efficiency'].update_layout(height=500)
        
        # 4. 채널별 ROI 분석
        channel_df_copy = channel_df.copy()
        channel_df_copy['roi'] = np.where(
            channel_df_copy['cost'] > 0,
            ((channel_df_copy['hired'] * 50000000) - channel_df_copy['cost']) / channel_df_copy['cost'] * 100,
            0
        )
        
        charts['roi'] = px.bar(
            channel_df_copy,
            x='channel',
            y='roi',
            title="채널별 ROI (%)",
            color='roi',
            color_continuous_scale='RdYlGn',
            text='roi'
        )
        charts['roi'].update_traces(
            texttemplate='%{text:.1f}%',
            textposition='outside'
        )
        charts['roi'].update_layout(height=400)
        
        return charts
    
    def create_monthly_trend_chart(self, monthly_df: pd.DataFrame) -> go.Figure:
        """월별 트렌드 차트"""
        fig = go.Figure()
        
        # 전체 지원자 수 라인
        fig.add_trace(go.Scatter(
            x=monthly_df['month'],
            y=monthly_df['total_applicants'],
            mode='lines+markers',
            name='전체 지원자',
            line=dict(color=self.colors['primary'], width=3),
            marker=dict(size=8)
        ))
        
        # 직무별 트렌드
        positions = ['developers', 'designers', 'data_analysts', 'product_managers']
        position_names = ['개발자', '디자이너', '데이터 분석가', '프로덕트 매니저']
        colors = [self.colors['success'], self.colors['warning'], self.colors['danger'], self.colors['info']]
        
        for pos, name, color in zip(positions, position_names, colors):
            if pos in monthly_df.columns:
                fig.add_trace(go.Scatter(
                    x=monthly_df['month'],
                    y=monthly_df[pos],
                    mode='lines+markers',
                    name=name,
                    line=dict(color=color, width=2),
                    marker=dict(size=6)
                ))
        
        fig.update_layout(
            title="월별 지원자 트렌드",
            xaxis_title="월",
            yaxis_title="지원자 수",
            height=400,
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig
    
    def create_regional_distribution_chart(self, region_df: pd.DataFrame) -> Dict[str, go.Figure]:
        """지역별 분포 차트들"""
        charts = {}
        
        # 1. 파이 차트
        charts['pie'] = px.pie(
            region_df,
            values='count',
            names='region',
            title="지역별 지원자 분포",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        charts['pie'].update_traces(textposition='inside', textinfo='percent+label')
        charts['pie'].update_layout(height=400)
        
        # 2. 막대 차트
        charts['bar'] = px.bar(
            region_df.sort_values('count', ascending=True),
            x='count',
            y='region',
            orientation='h',
            title="지역별 지원자 수",
            color='count',
            color_continuous_scale='Viridis',
            text='count'
        )
        charts['bar'].update_traces(
            texttemplate='%{text:,}명',
            textposition='outside'
        )
        charts['bar'].update_layout(height=400)
        
        return charts
    
    def create_score_distribution_chart(self, candidates_df: pd.DataFrame) -> go.Figure:
        """이력서 점수 분포 히스토그램"""
        fig = px.histogram(
            candidates_df,
            x='resume_score',
            nbins=20,
            title="이력서 점수 분포",
            color_discrete_sequence=[self.colors['primary']],
            labels={'resume_score': '이력서 점수', 'count': '지원자 수'}
        )
        
        # 평균선 추가
        mean_score = candidates_df['resume_score'].mean()
        fig.add_vline(
            x=mean_score,
            line_dash="dash",
            line_color="red",
            annotation_text=f"평균: {mean_score:.1f}점"
        )
        
        fig.update_layout(height=400)
        return fig
    
    def create_experience_distribution_chart(self, candidates_df: pd.DataFrame) -> go.Figure:
        """경력별 분포 차트"""
        experience_counts = candidates_df['experience'].value_counts()
        
        fig = px.bar(
            x=experience_counts.index,
            y=experience_counts.values,
            title="경력별 지원자 분포",
            labels={'x': '경력', 'y': '지원자 수'},
            color=experience_counts.values,
            color_continuous_scale='Blues'
        )
        
        fig.update_traces(text=experience_counts.values, textposition='outside')
        fig.update_layout(height=400)
        return fig
    
    def create_status_distribution_chart(self, candidates_df: pd.DataFrame) -> go.Figure:
        """상태별 분포 도넛 차트"""
        status_counts = candidates_df['status'].value_counts()
        
        # 상태별 색상 매핑
        colors = [self.status_colors.get(status, '#6b7280') for status in status_counts.index]
        
        fig = go.Figure(data=[go.Pie(
            labels=status_counts.index,
            values=status_counts.values,
            hole=0.3,
            marker_colors=colors
        )])
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            textfont_size=12
        )
        
        fig.update_layout(
            title="지원자 상태 분포",
            height=400,
            showlegend=True,
            legend=dict(orientation="v", yanchor="middle", y=0.5)
        )
        
        return fig
    
    def create_hiring_timeline_chart(self, candidates_df: pd.DataFrame) -> go.Figure:
        """채용 타임라인 차트"""
        # 합격자들의 채용 기간 계산
        hired_df = candidates_df[candidates_df['status'] == '합격'].copy()
        
        if hired_df.empty:
            # 빈 차트 반환
            fig = go.Figure()
            fig.add_annotation(
                text="합격자 데이터가 없습니다",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False, font=dict(size=16)
            )
            fig.update_layout(height=400, title="채용 타임라인")
            return fig
        
        # 가상의 채용 완료일 생성 (지원일 + 랜덤 기간)
        import random
        hired_df['hire_duration'] = [random.randint(14, 45) for _ in range(len(hired_df))]
        
        fig = px.scatter(
            hired_df,
            x='applied_date',
            y='hire_duration',
            color='position',
            size='resume_score',
            hover_data=['name', 'experience'],
            title="채용 타임라인 (지원일 vs 채용기간)",
            labels={
                'applied_date': '지원일',
                'hire_duration': '채용 기간 (일)',
                'position': '직무'
            }
        )
        
        fig.update_layout(height=400)
        return fig
    
    def create_performance_radar_chart(self, channel_df: pd.DataFrame, selected_channels: List[str] = None) -> go.Figure:
        """채널 성과 레이더 차트"""
        if selected_channels is None:
            selected_channels = channel_df['channel'].head(4).tolist()
        
        filtered_df = channel_df[channel_df['channel'].isin(selected_channels)]
        
        # 점수 정규화 (0-100 스케일)
        metrics = ['applicants', 'conversion_rate', 'quality_score']
        metric_names = ['지원자 수', '전환율', '품질 점수']
        
        fig = go.Figure()
        
        for _, row in filtered_df.iterrows():
            # 각 메트릭을 0-100으로 정규화
            normalized_values = []
            for metric in metrics:
                if metric == 'applicants':
                    # 지원자 수는 최대값 대비 비율
                    max_val = channel_df['applicants'].max()
                    normalized_values.append((row[metric] / max_val) * 100)
                elif metric == 'conversion_rate':
                    # 전환율은 그대로 사용 (이미 %)
                    normalized_values.append(row[metric] * 10)  # 스케일 조정
                elif metric == 'quality_score':
                    # 품질 점수 (1-5 → 0-100)
                    normalized_values.append((row[metric] / 5) * 100)
            
            fig.add_trace(go.Scatterpolar(
                r=normalized_values + [normalized_values[0]],  # 닫힌 도형을 위해 첫 값 반복
                theta=metric_names + [metric_names[0]],
                fill='toself',
                name=row['channel'],
                line=dict(width=2)
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            title="채널별 성과 비교 (레이더 차트)",
            height=400,
            showlegend=True
        )
        
        return fig
    
    def create_cohort_analysis_chart(self, candidates_df: pd.DataFrame) -> go.Figure:
        """코호트 분석 차트 (월별 지원자 현황)"""
        # 월별로 그룹화
        candidates_df['apply_month'] = candidates_df['applied_date'].dt.to_period('M')
        cohort_data = candidates_df.groupby(['apply_month', 'status']).size().unstack(fill_value=0)
        
        # 히트맵 생성
        fig = px.imshow(
            cohort_data.T,
            title="월별 지원자 상태 분포 (코호트 분석)",
            labels=dict(x="지원 월", y="상태", color="지원자 수"),
            aspect="auto",
            color_continuous_scale='Blues'
        )
        
        fig.update_layout(height=400)
        return fig
