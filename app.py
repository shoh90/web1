"""
종합 채용 대시보드 - 메인 애플리케이션
"""

import streamlit as st
import pandas as pd
import sys
import os

# 현재 디렉토리를 Python 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# 모듈 임포트
from config import PAGE_CONFIG, load_custom_css, DASHBOARD_MENU
from utils.data_generator import DataGenerator, calculate_hiring_metrics, filter_candidates
from utils.charts import ChartGenerator
from pages.dashboard_overview import render_dashboard_overview_extended

# 페이지 설정
st.set_page_config(**PAGE_CONFIG)

# CSS 스타일 로드
st.markdown(load_custom_css(), unsafe_allow_html=True)

class RecruitmentDashboard:
    """채용 대시보드 메인 클래스"""
    
    def __init__(self):
        self.data_generator = DataGenerator()
        self.chart_generator = ChartGenerator()
        self.initialize_session_state()
        self.load_data()
    
    def initialize_session_state(self):
        """세션 상태 초기화"""
        if 'data_loaded' not in st.session_state:
            st.session_state.data_loaded = False
        
        if 'refresh_data' not in st.session_state:
            st.session_state.refresh_data = False
    
    def load_data(self):
        """데이터 로드"""
        if not st.session_state.data_loaded or st.session_state.refresh_data:
            with st.spinner('데이터를 불러오는 중...'):
                (
                    st.session_state.candidates_df,
                    st.session_state.channel_df,
                    st.session_state.monthly_df,
                    st.session_state.region_df,
                    st.session_state.funnel_df,
                    st.session_state.interview_df
                ) = self.data_generator.generate_all_data()
                
                st.session_state.data_loaded = True
                st.session_state.refresh_data = False
    
    def render_header(self):
        """헤더 렌더링"""
        st.markdown('<h1 class="main-header">🎯 종합 채용 대시보드</h1>', unsafe_allow_html=True)
        
        # 서브 헤더와 새로고침 버튼
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("### 데이터 기반 채용 인사이트로 더 나은 인재 확보 전략을 수립하세요")
        
        with col2:
            if st.button("🔄 데이터 새로고침", use_container_width=True):
                st.session_state.refresh_data = True
                st.rerun()
        
        st.markdown("---")
    
    def render_sidebar(self):
        """사이드바 렌더링"""
        st.sidebar.markdown('<div class="sidebar-header">📊 대시보드 설정</div>', unsafe_allow_html=True)
        
        # 날짜 범위 선택
        st.sidebar.subheader("📅 분석 기간")
        from datetime import datetime, timedelta
        
        date_range = st.sidebar.date_input(
            "기간 선택",
            value=(datetime.now() - timedelta(days=30), datetime.now()),
            max_value=datetime.now(),
            key="date_range"
        )
        
        # 필터 옵션
        st.sidebar.subheader("🔍 필터 옵션")
        
        position_filter = st.sidebar.multiselect(
            "직무 선택",
            options=st.session_state.candidates_df['position'].unique(),
            default=st.session_state.candidates_df['position'].unique(),
            key="position_filter"
        )
        
        status_filter = st.sidebar.multiselect(
            "상태 선택", 
            options=st.session_state.candidates_df['status'].unique(),
            default=st.session_state.candidates_df['status'].unique(),
            key="status_filter"
        )
        
        location_filter = st.sidebar.multiselect(
            "지역 선택",
            options=st.session_state.candidates_df['location'].unique(),
            default=st.session_state.candidates_df['location'].unique(),
            key="location_filter"
        )
        
        # 점수 범위 필터
        st.sidebar.subheader("📊 점수 범위")
        score_range = st.sidebar.slider(
            "이력서 점수",
            min_value=0,
            max_value=100,
            value=(60, 100),
            key="score_range"
        )
        
        # 필터링된 데이터 반환
        filters = {
            'positions': position_filter,
            'statuses': status_filter,
            'locations': location_filter,
            'date_range': date_range,
            'min_score': score_range[0],
            'max_score': score_range[1]
        }
        
        return filters
    
    def apply_filters(self, filters):
        """필터 적용"""
        filtered_df = st.session_state.candidates_df.copy()
        
        # 필터 적용
        if filters['positions']:
            filtered_df = filtered_df[filtered_df['position'].isin(filters['positions'])]
        
        if filters['statuses']:
            filtered_df = filtered_df[filtered_df['status'].isin(filters['statuses'])]
        
        if filters['locations']:
            filtered_df = filtered_df[filtered_df['location'].isin(filters['locations'])]
        
        # 날짜 범위 필터
        if len(filters['date_range']) == 2:
            start_date, end_date = filters['date_range']
            filtered_df = filtered_df[
                (filtered_df['applied_date'].dt.date >= start_date) &
                (filtered_df['applied_date'].dt.date <= end_date)
            ]
        
        # 점수 범위 필터
        filtered_df = filtered_df[
            (filtered_df['resume_score'] >= filters['min_score']) &
            (filtered_df['resume_score'] <= filters['max_score'])
        ]
        
        return filtered_df
    
    def render_key_metrics(self, filtered_df):
        """핵심 지표 카드"""
        metrics = calculate_hiring_metrics(filtered_df)
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            st.metric(
                label="📊 총 지원자",
                value=f"{metrics['total_applicants']:,}",
                delta=f"전체 {len(st.session_state.candidates_df):,}명 중"
            )
        
        with col2:
            st.metric(
                label="🎯 최종 합격",
                value=f"{metrics['total_hired']}명",
                delta=f"{metrics['overall_conversion_rate']}% 전환율"
            )
        
        with col3:
            avg_leadtime = 24  # 예시값
            st.metric(
                label="⏱️ 평균 리드타임", 
                value=f"{avg_leadtime}일",
                delta="3일 단축"
            )
        
        with col4:
            total_cost = st.session_state.channel_df['cost'].sum()
            st.metric(
                label="💰 총 광고비",
                value=f"{total_cost//10000:,}만원", 
                delta="예산 대비 85%"
            )
        
        with col5:
            active_positions = len(filtered_df['position'].unique())
            st.metric(
                label="📝 활성 공고",
                value=f"{active_positions * 3}개",
                delta=f"{active_positions}개 직무"
            )
        
        with col6:
            avg_score = filtered_df['resume_score'].mean()
            st.metric(
                label="⭐ 평균 점수",
                value=f"{avg_score:.0f}점",
                delta="이력서 품질"
            )
    
    def render_dashboard_overview_tab(self, filtered_df):
        """대시보드 개요 탭"""
        render_dashboard_overview_extended(filtered_df, st.session_state.interview_df)
    
    def render_candidate_management_tab(self, filtered_df):
        """지원자 관리 탭"""
        st.header("👥 지원자 관리")
        
        # 검색 및 정렬
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            search_term = st.text_input("🔍 지원자 검색", placeholder="이름, 포지션, 스킬로 검색...")
        
        with col2:
            sort_by = st.selectbox("정렬 기준", ['이름', '지원일', '점수', '평점'])
        
        with col3:
            sort_order = st.selectbox("정렬 순서", ['오름차순', '내림차순'])
        
        # 검색 적용
        search_df = filtered_df
        if search_term:
            search_df = filtered_df[
                filtered_df['name'].str.contains(search_term, case=False, na=False) |
                filtered_df['position'].str.contains(search_term, case=False, na=False) |
                filtered_df['skills'].str.contains(search_term, case=False, na=False)
            ]
        
        # 정렬 적용
        sort_mapping = {'이름': 'name', '지원일': 'applied_date', '점수': 'resume_score', '평점': 'rating'}
        ascending = sort_order == '오름차순'
        search_df = search_df.sort_values(sort_mapping[sort_by], ascending=ascending)
        
        # 상태별 요약
        st.subheader("📊 현재 상태 분포")
        status_counts = search_df['status'].value_counts()
        
        status_cols = st.columns(len(status_counts))
        for i, (status, count) in enumerate(status_counts.items()):
            with status_cols[i]:
                st.metric(status, count)
        
        # 지원자 목록
        st.subheader(f"📋 지원자 목록 (총 {len(search_df)}명)")
        
        # 페이지네이션
        items_per_page = 10
        total_pages = (len(search_df) - 1) // items_per_page + 1
        
        if total_pages > 1:
            page = st.selectbox("페이지", range(1, total_pages + 1), key="candidate_page") - 1
            start_idx = page * items_per_page
            end_idx = min(start_idx + items_per_page, len(search_df))
            page_df = search_df.iloc[start_idx:end_idx]
        else:
            page_df = search_df
        
        # 지원자 카드 표시
        for _, candidate in page_df.iterrows():
            self.render_candidate_card(candidate)
    
    def render_candidate_card(self, candidate):
        """개별 지원자 카드"""
        with st.expander(f"👤 {candidate['name']} - {candidate['position']} (점수: {candidate['resume_score']}점)"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**🆔 ID:** {candidate['id']}")
                st.write(f"**📧 이메일:** {candidate['email']}")
                st.write(f"**🏢 경력:** {candidate['experience']}")
                st.write(f"**📍 지역:** {candidate['location']}")
                
            with col2:
                st.write(f"**⭐ 평점:** {candidate['rating']}")
                st.write(f"**📊 점수:** {candidate['resume_score']}점")
                st.write(f"**💰 희망연봉:** {candidate['salary_expectation']}")
                st.write(f"**🛠️ 스킬:** {candidate['skills']}")
                
            with col3:
                # 상태 배지
                from config import STATUS_COLORS
                status_color = STATUS_COLORS.get(candidate['status'], '#6b7280')
                
                st.markdown(f"""
                <div class="status-badge" style="background-color: {status_color}; color: white;">
                    {candidate['status']}
                </div>
                """, unsafe_allow_html=True)
                
                st.write(f"**📅 지원일:** {candidate['applied_date'].strftime('%Y-%m-%d')}")
                st.write(f"**📊 유입경로:** {candidate['source']}")
                
                # 진행 바
                progress = candidate['resume_score'] / 100
                st.progress(progress, text=f"점수: {candidate['resume_score']}점")
                
                # 액션 버튼
                btn_col1, btn_col2, btn_col3 = st.columns(3)
                with btn_col1:
                    if st.button("📧", key=f"email_{candidate['id']}", help="이메일"):
                        st.success(f"{candidate['name']}님에게 이메일을 보냈습니다.")
                with btn_col2:
                    if st.button("📅", key=f"schedule_{candidate['id']}", help="일정"):
                        st.info("면접 일정을 잡았습니다.")
                with btn_col3:
                    if st.button("📝", key=f"note_{candidate['id']}", help="메모"):
                        st.info("메모를 추가했습니다.")
    
    def render_funnel_tab(self):
        """채용 퍼널 탭"""
        st.header("🔄 채용 퍼널 분석")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 퍼널 차트
            funnel_chart = self.chart_generator.create_funnel_chart(st.session_state.funnel_df)
            st.plotly_chart(funnel_chart, use_container_width=True)
        
        with col2:
            # 전환율 차트
            conversion_chart = self.chart_generator.create_conversion_rate_chart(st.session_state.funnel_df)
            st.plotly_chart(conversion_chart, use_container_width=True)
        
        # 퍼널 상세 분석
        st.subheader("📈 퍼널 상세 분석")
        
        funnel_col1, funnel_col2, funnel_col3 = st.columns(3)
        
        with funnel_col1:
            st.info("""
            **💡 서류 심사 분석**
            - 통과율: 45.0%
            - 업계 평균 대비 우수
            - 추천: 스크리닝 기준 최적화
            """)
        
        with funnel_col2:
            st.warning("""
            **⚠️ 면접 단계 분석**
            - 1차→2차 전환율 48%
            - 면접 품질 향상 필요
            - 추천: 면접관 교육 강화
            """)
        
        with funnel_col3:
            st.success("""
            **✅ 최종 전환율**
            - 전체 전환율: 5.0%
            - 목표 대비 달성
            - 지속적 모니터링 필요
            """)
        
        # 단계별 상세 테이블
        st.subheader("📋 단계별 상세 현황")
        
        funnel_detail = st.session_state.funnel_df.copy()
        funnel_detail['이탈자 수'] = funnel_detail['count'].shift(1) - funnel_detail['count']
        funnel_detail['이탈자 수'] = funnel_detail['이탈자 수'].fillna(0).astype(int)
        funnel_detail['누적 이탈율'] = ((funnel_detail['count'].iloc[0] - funnel_detail['count']) / funnel_detail['count'].iloc[0] * 100).round(1)
        
        display_funnel = funnel_detail[['stage', 'count', '이탈자 수', 'percentage', '누적 이탈율']].copy()
        display_funnel.columns = ['단계', '인원 수', '이탈자 수', '비율(%)', '누적 이탈율(%)']
        
        st.dataframe(display_funnel, use_container_width=True, hide_index=True)
    
    def render_channel_performance_tab(self):
        """채널 성과 탭"""
        st.header("📊 채널별 성과 분석")
        
        # 채널 성과 차트들
        channel_charts = self.chart_generator.create_channel_performance_chart(st.session_state.channel_df)
        
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.plotly_chart(channel_charts['applicants'], use_container_width=True)
            st.plotly_chart(channel_charts['roi'], use_container_width=True)
        
        with chart_col2:
            st.plotly_chart(channel_charts['conversion'], use_container_width=True)
            st.plotly_chart(channel_charts['efficiency'], use_container_width=True)
        
        # 채널 성과 테이블
        st.subheader("📋 채널별 상세 성과")
        
        channel_detail = st.session_state.channel_df.copy()
        channel_detail['ROI'] = np.where(
            channel_detail['cost'] > 0,
            ((channel_detail['hired'] * 50000000) - channel_detail['cost']) / channel_detail['cost'] * 100,
            0
        ).round(1)
        
        # CPA 계산
        channel_detail['CPA'] = np.where(
            channel_detail['hired'] > 0,
            channel_detail['cost'] / channel_detail['hired'],
            0
        ).astype(int)
        
        display_channels = channel_detail[['channel', 'applicants', 'hired', 'conversion_rate', 'cost', 'CPA', 'ROI']].copy()
        display_channels.columns = ['채널', '지원자 수', '합격자 수', '전환율(%)', '광고비(원)', 'CPA(원)', 'ROI(%)']
        
        # 숫자 포맷팅
        display_channels['광고비(원)'] = display_channels['광고비(원)'].apply(lambda x: f"{x:,}")
        display_channels['CPA(원)'] = display_channels['CPA(원)'].apply(lambda x: f"{x:,}" if x > 0 else "0")
        
        st.dataframe(display_channels, use_container_width=True, hide_index=True)
        
        # 채널 추천 인사이트
        st.subheader("💡 채널 최적화 제안")
        
        # 최고 성과 채널 찾기
        best_channel = st.session_state.channel_df.loc[st.session_state.channel_df['conversion_rate'].idxmax()]
        worst_channel = st.session_state.channel_df.loc[st.session_state.channel_df['conversion_rate'].idxmin()]
        
        insight_col1, insight_col2, insight_col3 = st.columns(3)
        
        with insight_col1:
            st.success(f"""
            **🏆 최고 성과 채널**
            
            **{best_channel['channel']}**
            - 전환율: {best_channel['conversion_rate']:.1f}%
            - 지원자: {best_channel['applicants']:,}명
            - 합격자: {best_channel['hired']}명
            
            **추천:** 예산 확대 검토
            """)
        
        with insight_col2:
            st.warning(f"""
            **⚠️ 개선 필요 채널**
            
            **{worst_channel['channel']}**
            - 전환율: {worst_channel['conversion_rate']:.1f}%
            - 높은 비용 대비 낮은 성과
            
            **추천:** 타겟팅 재검토 필요
            """)
        
        with insight_col3:
            # 무료 채널 성과
            free_channels = st.session_state.channel_df[st.session_state.channel_df['cost'] == 0]
            if not free_channels.empty:
                best_free = free_channels.loc[free_channels['conversion_rate'].idxmax()]
                st.info(f"""
                **💰 최고 효율 무료 채널**
                
                **{best_free['channel']}**
                - 전환율: {best_free['conversion_rate']:.1f}%
                - 비용: 무료
                
                **추천:** 적극 활용 권장
                """)
    
    def render_analytics_tab(self):
        """분석 리포트 탭"""
        st.header("📍 분석 리포트")
        
        analytics_col1, analytics_col2 = st.columns(2)
        
        with analytics_col1:
            # 지역별 분포 차트
            regional_charts = self.chart_generator.create_regional_distribution_chart(st.session_state.region_df)
            st.plotly_chart(regional_charts['pie'], use_container_width=True)
            
            # 이력서 점수 분포
            score_chart = self.chart_generator.create_score_distribution_chart(st.session_state.candidates_df)
            st.plotly_chart(score_chart, use_container_width=True)
        
        with analytics_col2:
            # 월별 트렌드
            trend_chart = self.chart_generator.create_monthly_trend_chart(st.session_state.monthly_df)
            st.plotly_chart(trend_chart, use_container_width=True)
            
            # 경력별 분포
            experience_chart = self.chart_generator.create_experience_distribution_chart(st.session_state.candidates_df)
            st.plotly_chart(experience_chart, use_container_width=True)
        
        # 상세 분석 섹션
        st.subheader("📊 상세 분석")
        
        detail_tab1, detail_tab2, detail_tab3 = st.tabs(["지역 분석", "트렌드 분석", "성과 분석"])
        
        with detail_tab1:
            st.markdown("#### 지역별 채용 현황")
            
            # 지역별 상세 테이블
            region_detail = st.session_state.region_df.copy()
            region_detail['평균 연봉'] = region_detail['avg_salary_expectation']
            region_detail['품질 점수'] = region_detail['avg_quality_score']
            
            display_regions = region_detail[['region', 'count', 'percentage', '평균 연봉', '품질 점수']].copy()
            display_regions.columns = ['지역', '지원자 수', '비율(%)', '평균 희망연봉', '평균 품질점수']
            
            st.dataframe(display_regions, use_container_width=True, hide_index=True)
            
            # 지역별 인사이트
            st.markdown("**💡 지역별 인사이트**")
            col1, col2 = st.columns(2)
            
            with col1:
                st.info("""
                **서울/경기 집중도**
                - 전체 지원자의 68.6% 집중
                - 높은 품질 점수 유지
                - 경쟁 심화로 인한 높은 연봉 기대
                """)
            
            with col2:
                st.success("""
                **지방 인재 활용**
                - 상대적으로 낮은 경쟁률
                - 합리적인 연봉 기대치
                - 원격근무 확대로 기회 증가
                """)
        
        with detail_tab2:
            st.markdown("#### 월별 트렌드 분석")
            
            # 트렌드 요약
            trend_summary = st.session_state.monthly_df.copy()
            trend_summary['성장률'] = trend_summary['total_applicants'].pct_change() * 100
            trend_summary['성장률'] = trend_summary['성장률'].fillna(0).round(1)
            
            display_trend = trend_summary[['month', 'total_applicants', 'developers', 'designers', '성장률']].copy()
            display_trend.columns = ['월', '전체 지원자', '개발자', '디자이너', '전월 대비 성장률(%)']
            
            st.dataframe(display_trend, use_container_width=True, hide_index=True)
            
            # 계절성 분석
            st.markdown("**📈 계절성 분석**")
            seasonal_col1, seasonal_col2 = st.columns(2)
            
            with seasonal_col1:
                st.info("""
                **채용 성수기 (3-4월, 9-10월)**
                - 봄/가을 채용 활성화
                - 평균 30% 지원자 증가
                - 경력직 이동 활발
                """)
            
            with seasonal_col2:
                st.warning("""
                **채용 비수기 (1-2월, 7-8월)**
                - 연말연시/휴가철 영향
                - 지원자 수 감소
                - 우수 인재 확보 기회
                """)
        
        with detail_tab3:
            st.markdown("#### 채용 성과 분석")
            
            # 성과 지표 계산
            total_candidates = len(st.session_state.candidates_df)
            total_hired = len(st.session_state.candidates_df[st.session_state.candidates_df['status'] == '합격'])
            avg_score = st.session_state.candidates_df['resume_score'].mean()
            
            perf_col1, perf_col2, perf_col3 = st.columns(3)
            
            with perf_col1:
                st.metric("전체 전환율", f"{(total_hired/total_candidates*100):.1f}%", "목표 5.0%")
            
            with perf_col2:
                st.metric("평균 이력서 점수", f"{avg_score:.1f}점", "목표 75점")
            
            with perf_col3:
                high_score_ratio = len(st.session_state.candidates_df[st.session_state.candidates_df['resume_score'] >= 80]) / total_candidates * 100
                st.metric("우수 지원자 비율", f"{high_score_ratio:.1f}%", "80점 이상")
            
            # 성과 개선 제안
            st.markdown("**🎯 성과 개선 제안**")
            
            improvement_col1, improvement_col2 = st.columns(2)
            
            with improvement_col1:
                st.success("""
                **✅ 잘하고 있는 것**
                - 링크드인 채널 높은 전환율
                - 직접지원/추천 채널 우수 성과
                - 서류 심사 효율성 양호
                """)
            
            with improvement_col2:
                st.warning("""
                **⚠️ 개선이 필요한 것**
                - 면접 단계 전환율 향상
                - 지방 인재 유치 전략 필요
                - 채용 리드타임 단축
                """)
    
    def render_ai_insights_tab(self):
        """AI 인사이트 탭"""
        st.header("🤖 AI 채용 인사이트")
        
        insights_col1, insights_col2 = st.columns(2)
        
        with insights_col1:
            st.subheader("🔍 주요 발견사항")
            
            # 데이터 기반 인사이트 생성
            high_score_candidates = len(st.session_state.candidates_df[st.session_state.candidates_df['resume_score'] >= 80])
            best_channel = st.session_state.channel_df.loc[st.session_state.channel_df['conversion_rate'].idxmax()]
            
            insights = [
                f"80점 이상 이력서의 합격률이 평균 대비 2.3배 높음 ({high_score_candidates}명)",
                f"{best_channel['channel']} 채널의 전환율이 {best_channel['conversion_rate']:.1f}%로 가장 높음", 
                "경력 4-6년 구간의 지원자 품질 점수 최고 (평균 82.4점)",
                "자기소개서 800자 이상 작성 시 합격률 68% 향상",
                "면접 후 24시간 내 피드백 제공 시 지원자 만족도 87% 증가"
            ]
            
            for insight in insights:
                st.markdown(f"""
                <div class="insights-card">
                    💡 {insight}
                </div>
                """, unsafe_allow_html=True)
        
        with insights_col2:
            st.subheader("📈 개선 권장사항")
            
            recommendations = [
                f"{best_channel['channel']} 채널 투자 확대 및 타겟팅 강화",
                "이력서 첨삭 서비스 활용률 증대 방안 마련",
                "80점 미만 지원자 대상 사전 가이드 제공", 
                "경력직 중심의 채용 전략 수립 검토",
                "면접 프로세스 표준화 및 피드백 시스템 구축"
            ]
            
            for rec in recommendations:
                st.markdown(f"""
                <div class="recommendation-card">
                    🎯 {rec}
                </div>
                """, unsafe_allow_html=True)
        
        # AI 분석 차트들
        st.subheader("📊 AI 기반 분석")
        
        ai_tab1, ai_tab2, ai_tab3 = st.tabs(["성과 예측", "이상 탐지", "최적화 제안"])
        
        with ai_tab1:
            # 성과 예측 차트
            st.markdown("#### 📈 향후 3개월 채용 성과 예측")
            
            # 가상의 예측 데이터
            import numpy as np
            future_months = ['2024-07', '2024-08', '2024-09']
            predicted_applicants = [580, 520, 650]
            confidence_interval = [50, 45, 60]
            
            prediction_data = pd.DataFrame({
                'month': future_months,
                'predicted': predicted_applicants,
                'lower': [p - c for p, c in zip(predicted_applicants, confidence_interval)],
                'upper': [p + c for p, c in zip(predicted_applicants, confidence_interval)]
            })
            
            import plotly.graph_objects as go
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=prediction_data['month'],
                y=prediction_data['predicted'],
                mode='lines+markers',
                name='예측값',
                line=dict(color='blue', width=3)
            ))
            
            fig.add_trace(go.Scatter(
                x=prediction_data['month'],
                y=prediction_data['upper'],
                fill=None,
                mode='lines',
                line_color='rgba(0,0,0,0)',
                showlegend=False
            ))
            
            fig.add_trace(go.Scatter(
                x=prediction_data['month'],
                y=prediction_data['lower'],
                fill='tonexty',
                mode='lines',
                line_color='rgba(0,0,0,0)',
                name='신뢰구간',
                fillcolor='rgba(0,100,80,0.2)'
            ))
            
            fig.update_layout(
                title="향후 3개월 지원자 수 예측",
                xaxis_title="월",
                yaxis_title="예상 지원자 수",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # 예측 요약
            pred_col1, pred_col2, pred_col3 = st.columns(3)
            
            with pred_col1:
                st.metric("7월 예측", "580명", "△60명")
            with pred_col2:
                st.metric("8월 예측", "520명", "▽60명") 
            with pred_col3:
                st.metric("9월 예측", "650명", "△130명")
        
        with ai_tab2:
            st.markdown("#### 🔍 이상 패턴 탐지")
            
            # 이상 패턴 감지 결과
            anomaly_col1, anomaly_col2 = st.columns(2)
            
            with anomaly_col1:
                st.error("""
                **🚨 감지된 이상 패턴**
                
                - 특정 채널에서 급격한 지원자 증가 감지
                - 평균 대비 200% 증가 (조사 필요)
                - 스팸 지원 가능성 검토 요망
                """)
                
                st.warning("""
                **⚠️ 주의 패턴**
                
                - 고득점 지원자의 면접 불참률 증가
                - 경쟁사 대량 채용 시기와 겹침
                - 대응 전략 수립 필요
                """)
            
            with anomaly_col2:
                st.info("""
                **📊 정상 범위 지표**
                
                - 전체 지원자 수: 정상 범위
                - 평균 이력서 점수: 안정적
                - 면접 진행률: 양호
                """)
                
                st.success("""
                **✅ 긍정적 변화**
                
                - 우수 지원자 비율 상승
                - 면접 만족도 개선
                - 채용 효율성 향상
                """)
        
        with ai_tab3:
            st.markdown("#### 🎯 최적화 제안")
            
            # 최적화 제안들
            opt_col1, opt_col2 = st.columns(2)
            
            with opt_col1:
                st.markdown("**💰 예산 최적화**")
                
                budget_suggestions = [
                    "링크드인 예산 30% 증액 권장",
                    "사람인 예산 15% 감액 고려", 
                    "직접지원 채널 강화 투자",
                    "추천 프로그램 인센티브 확대"
                ]
                
                for suggestion in budget_suggestions:
                    st.write(f"• {suggestion}")
                
                st.markdown("**⏰ 프로세스 최적화**")
                
                process_suggestions = [
                    "서류 심사 기간 3일 → 2일 단축",
                    "면접 일정 자동화 시스템 도입",
                    "합격 통보 시점 최적화",
                    "불합격자 피드백 자동화"
                ]
                
                for suggestion in process_suggestions:
                    st.write(f"• {suggestion}")
            
            with opt_col2:
                st.markdown("**📊 타겟팅 최적화**")
                
                targeting_suggestions = [
                    "경력 3-5년 개발자 타겟 확대",
                    "부산/대구 지역 인재 발굴 강화", 
                    "특정 대학 출신 타겟팅",
                    "전직자 재입사 프로그램 검토"
                ]
                
                for suggestion in targeting_suggestions:
                    st.write(f"• {suggestion}")
                
                st.markdown("**🔄 개선 액션 플랜**")
                
                action_plan = [
                    "1주차: 고성과 채널 예산 재배분",
                    "2주차: 면접 프로세스 표준화",
                    "3주차: 신규 채널 테스트 시작", 
                    "4주차: 성과 측정 및 조정"
                ]
                
                for action in action_plan:
                    st.write(f"• {action}")
    
    def render_footer(self):
        """푸터 렌더링"""
        st.markdown("""
        <div class="footer">
            🚀 <strong>Advanced Recruitment Dashboard v2.0</strong><br>
            데이터 기반 채용 의사결정을 위한 통합 플랫폼<br>
            Built with ❤️ using Streamlit, Plotly, and Pandas<br>
            <small>마지막 업데이트: 2024년 5월 27일</small>
        </div>
        """, unsafe_allow_html=True)
    
    def run(self):
        """메인 애플리케이션 실행"""
        # 헤더 렌더링
        self.render_header()
        
        # 사이드바에서 필터 가져오기
        filters = self.render_sidebar()
        
        # 필터 적용
        filtered_df = self.apply_filters(filters)
        
        # 핵심 지표 표시
        self.render_key_metrics(filtered_df)
        
        st.markdown("---")
        
        # 탭 생성
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📈 대시보드 개요", "👥 지원자 관리", "🔄 채용 퍼널", 
            "📊 채널 성과", "📍 분석 리포트", "🤖 AI 인사이트"
        ])
        
        with tab1:
            self.render_dashboard_overview_tab(filtered_df)
        
        with tab2:
            self.render_candidate_management_tab(filtered_df)
        
        with tab3:
            self.render_funnel_tab()
        
        with tab4:
            self.render_channel_performance_tab()
        
        with tab5:
            self.render_analytics_tab()
        
        with tab6:
            self.render_ai_insights_tab()
        
        # 푸터 렌더링
        self.render_footer()

# 메인 실행부
if __name__ == "__main__":
    dashboard = RecruitmentDashboard()
    dashboard.run()
