"""
채용 대시보드 데이터 생성 및 관리 모듈
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from typing import Tuple, Dict, List
import streamlit as st

# 설정 파일에서 상수 가져오기
from config import (
    JOB_CATEGORIES, RECRUITMENT_CHANNELS, REGIONS, 
    EXPERIENCE_LEVELS, RECRUITMENT_STAGES
)

class DataGenerator:
    """채용 데이터를 생성하고 관리하는 클래스"""
    
    def __init__(self):
        self.names = self._generate_korean_names()
        self.companies = self._get_company_list()
        self.skills = self._get_skills_by_position()
        
    def _generate_korean_names(self) -> List[str]:
        """한국 이름 생성"""
        surnames = ['김', '이', '박', '최', '정', '강', '조', '윤', '장', '임', '한', '오', '서', '신', '권', '황', '안', '송', '류', '전']
        given_names = ['민수', '지은', '준호', '서영', '하늘', '민아', '성진', '유리', '지수', '도현', 
                      '민철', '수진', '현우', '예린', '태현', '소영', '도윤', '채영', '민성', '지훈',
                      '윤서', '준표', '소희', '태영', '은지', '승현', '다은', '민호', '수빈', '재현']
        
        names = []
        for _ in range(100):
            surname = random.choice(surnames)
            given_name = random.choice(given_names)
            names.append(f"{surname}{given_name}")
        return names
    
    def _get_company_list(self) -> List[str]:
        """이전 직장 리스트"""
        return [
            '삼성전자', 'LG전자', 'SK하이닉스', '현대자동차', 'KT',
            '네이버', '카카오', '쿠팡', '배달의민족', '토스',
            '라인', '넥슨', 'NHN', '우아한형제들', '마켓컬리',
            '당근마켓', '직방', '야놀자', '무신사', '29CM'
        ]
    
    def _get_skills_by_position(self) -> Dict[str, List[str]]:
        """직무별 스킬 매핑"""
        return {
            '프론트엔드 개발자': ['React', 'Vue.js', 'Angular', 'JavaScript', 'TypeScript', 'HTML/CSS', 'Webpack'],
            '백엔드 개발자': ['Python', 'Java', 'Node.js', 'Spring', 'Django', 'MySQL', 'PostgreSQL', 'Redis'],
            'DevOps 엔지니어': ['AWS', 'Docker', 'Kubernetes', 'Jenkins', 'Terraform', 'Ansible', 'Git'],
            '머신러닝 엔지니어': ['Python', 'TensorFlow', 'PyTorch', 'Scikit-learn', 'Pandas', 'NumPy', 'SQL'],
            'UI/UX 디자이너': ['Figma', 'Sketch', 'Adobe XD', 'Photoshop', 'Illustrator', 'Principle', 'Zeplin'],
            '프로덕트 디자이너': ['Figma', 'Sketch', 'Framer', 'Principle', 'InVision', 'Miro', 'Adobe Creative'],
            '데이터 분석가': ['SQL', 'Python', 'R', 'Tableau', 'Power BI', 'Excel', 'Google Analytics'],
            '데이터 사이언티스트': ['Python', 'R', 'SQL', 'Jupyter', 'Pandas', 'Scikit-learn', 'TensorFlow'],
            '프로덕트 매니저': ['JIRA', 'Confluence', 'Figma', 'Analytics', 'A/B Testing', 'SQL', 'Excel'],
            'QA 엔지니어': ['Selenium', 'Postman', 'JIRA', 'TestRail', 'Python', 'Java', 'Git']
        }
    
    @st.cache_data(ttl=3600)  # 1시간 캐시
    def generate_candidates_data(_self, num_candidates: int = 100) -> pd.DataFrame:
        """지원자 데이터 생성"""
        
        # 모든 직무 리스트 생성
        all_positions = []
        for positions in JOB_CATEGORIES.values():
            all_positions.extend(positions)
        
        candidates_data = []
        
        for i in range(num_candidates):
            name = random.choice(_self.names)
            position = random.choice(all_positions)
            
            # 직무에 따른 스킬 할당
            position_skills = _self.skills.get(position, ['기본 스킬'])
            selected_skills = random.sample(position_skills, min(3, len(position_skills)))
            
            # 지원일 생성 (최근 6개월)
            applied_date = datetime.now() - timedelta(days=random.randint(1, 180))
            
            # 경력에 따른 가중치가 있는 점수 생성
            experience = random.choice(EXPERIENCE_LEVELS)
            exp_weight = {'신입': 0.8, '1년': 0.85, '2년': 0.9, '3년': 0.95}.get(experience, 1.0)
            base_score = random.normalvariate(75, 15)
            resume_score = max(50, min(98, int(base_score * exp_weight)))
            
            # 상태 가중치 (최근 지원자일수록 초기 단계)
            days_ago = (datetime.now() - applied_date).days
            if days_ago < 7:
                status_weights = [0.5, 0.3, 0.1, 0.05, 0.03, 0.02]
            elif days_ago < 30:
                status_weights = [0.2, 0.3, 0.25, 0.15, 0.07, 0.03]
            else:
                status_weights = [0.1, 0.15, 0.2, 0.25, 0.2, 0.1]
            
            status = random.choices(RECRUITMENT_STAGES[1:], weights=status_weights)[0]
            
            candidate = {
                'id': f'REC{i+1:04d}',
                'name': name,
                'position': position,
                'status': status,
                'experience': experience,
                'location': random.choice(REGIONS),
                'resume_score': resume_score,
                'rating': round(random.uniform(3.0, 5.0), 1),
                'applied_date': applied_date,
                'email': f'{name.lower().replace(" ", "")}@email.com',
                'phone': f'010-{random.randint(1000,9999)}-{random.randint(1000,9999)}',
                'salary_expectation': f'{random.randint(3000, 8000)}만원',
                'skills': ', '.join(selected_skills),
                'source': random.choice(RECRUITMENT_CHANNELS),
                'previous_company': random.choice(_self.companies) if experience != '신입' else '신입',
                'education': random.choice(['고졸', '전문대졸', '대졸', '석사', '박사']),
                'portfolio_url': f'https://portfolio.{name.lower()}.com' if position in ['프론트엔드 개발자', 'UI/UX 디자이너'] else None,
                'github_url': f'https://github.com/{name.lower()}' if '개발자' in position or '엔지니어' in position else None,
                'linkedin_url': f'https://linkedin.com/in/{name.lower()}',
                'interview_date': applied_date + timedelta(days=random.randint(7, 21)) if status in ['1차 면접', '2차 면접', '최종 면접'] else None,
                'notes': f'{name}님은 {position} 경력 {experience}으로 {", ".join(selected_skills)} 스킬을 보유하고 있습니다.'
            }
            
            candidates_data.append(candidate)
        
        return pd.DataFrame(candidates_data)
    
    @st.cache_data(ttl=3600)
    def generate_channel_performance_data(_self) -> pd.DataFrame:
        """채널 성과 데이터 생성"""
        channel_data = []
        
        # 채널별 특성을 반영한 데이터 생성
        channel_configs = {
            '사람인': {'base_applicants': 1200, 'conversion_rate': 4.5, 'cost_per_click': 800},
            '잡코리아': {'base_applicants': 900, 'conversion_rate': 5.2, 'cost_per_click': 750},
            '링크드인': {'base_applicants': 300, 'conversion_rate': 8.5, 'cost_per_click': 1200},
            '원티드': {'base_applicants': 600, 'conversion_rate': 6.8, 'cost_per_click': 950},
            '직접지원': {'base_applicants': 200, 'conversion_rate': 12.0, 'cost_per_click': 0},
            '추천': {'base_applicants': 80, 'conversion_rate': 15.5, 'cost_per_click': 0},
            'GitHub Jobs': {'base_applicants': 150, 'conversion_rate': 9.2, 'cost_per_click': 600},
            '프로그래머스': {'base_applicants': 180, 'conversion_rate': 7.8, 'cost_per_click': 700}
        }
        
        for channel, config in channel_configs.items():
            # 계절성과 랜덤 요소를 반영한 지원자 수
            seasonal_factor = random.uniform(0.8, 1.2)
            applicants = int(config['base_applicants'] * seasonal_factor)
            
            # 전환율에 약간의 변동성 추가
            conversion_rate = config['conversion_rate'] * random.uniform(0.9, 1.1)
            hired = int(applicants * conversion_rate / 100)
            
            # 비용 계산
            if config['cost_per_click'] > 0:
                total_cost = applicants * config['cost_per_click']
                cpa = total_cost / hired if hired > 0 else 0
            else:
                total_cost = 0
                cpa = 0
            
            channel_data.append({
                'channel': channel,
                'applicants': applicants,
                'hired': hired,
                'cost': total_cost,
                'conversion_rate': round(conversion_rate, 2),
                'cpa': round(cpa, 0),
                'clicks': applicants * random.randint(3, 8),  # 지원자 당 평균 클릭 수
                'ctr': round(random.uniform(2.0, 8.0), 2),  # 클릭율
                'quality_score': round(random.uniform(3.5, 5.0), 1)  # 채널 품질 점수
            })
        
        return pd.DataFrame(channel_data)
    
    @st.cache_data(ttl=3600)
    def generate_monthly_trend_data(_self) -> pd.DataFrame:
        """월별 트렌드 데이터 생성"""
        months = pd.date_range(start='2024-01-01', end='2024-06-30', freq='M')
        
        trend_data = []
        base_applicants = 400
        
        for i, month in enumerate(months):
            # 계절성 반영 (봄, 가을에 채용 활발)
            seasonal_factor = 1.0
            month_num = month.month
            if month_num in [3, 4, 9, 10]:  # 봄, 가을
                seasonal_factor = 1.3
            elif month_num in [1, 2, 12]:  # 겨울
                seasonal_factor = 0.8
            elif month_num in [7, 8]:  # 여름
                seasonal_factor = 0.9
            
            # 성장 트렌드 반영
            growth_factor = 1 + (i * 0.05)  # 월별 5% 성장
            
            total = int(base_applicants * seasonal_factor * growth_factor)
            
            # 직무별 분배 (비율을 약간씩 변동)
            dev_ratio = random.uniform(0.45, 0.55)
            design_ratio = random.uniform(0.12, 0.18)
            data_ratio = random.uniform(0.08, 0.15)
            pm_ratio = random.uniform(0.05, 0.10)
            qa_ratio = random.uniform(0.03, 0.08)
            others_ratio = 1 - (dev_ratio + design_ratio + data_ratio + pm_ratio + qa_ratio)
            
            trend_data.append({
                'month': month.strftime('%Y-%m'),
                'total_applicants': total,
                'developers': int(total * dev_ratio),
                'designers': int(total * design_ratio),
                'data_analysts': int(total * data_ratio),
                'product_managers': int(total * pm_ratio),
                'qa_engineers': int(total * qa_ratio),
                'others': int(total * others_ratio),
                'avg_quality_score': round(random.uniform(70, 85), 1),
                'avg_response_time': round(random.uniform(2.5, 7.0), 1)  # 평균 응답 시간(일)
            })
        
        return pd.DataFrame(trend_data)
    
    @st.cache_data(ttl=3600)
    def generate_regional_data(_self) -> pd.DataFrame:
        """지역별 분포 데이터 생성"""
        # 실제 인구 분포를 반영한 가중치
        region_weights = {
            '서울': 0.35, '경기': 0.25, '부산': 0.08, '대구': 0.06,
            '인천': 0.07, '광주': 0.04, '대전': 0.04, '울산': 0.03,
            '세종': 0.02, '기타': 0.06
        }
        
        total_candidates = 3500  # 전체 지원자 수
        regional_data = []
        
        for region, weight in region_weights.items():
            count = int(total_candidates * weight * random.uniform(0.9, 1.1))
            percentage = (count / total_candidates) * 100
            
            # 지역별 특성 반영
            if region == '서울':
                avg_salary = random.randint(5500, 7500)
                quality_score = random.uniform(78, 88)
            elif region == '경기':
                avg_salary = random.randint(4800, 6800)
                quality_score = random.uniform(75, 85)
            else:
                avg_salary = random.randint(3800, 5800)
                quality_score = random.uniform(70, 82)
            
            regional_data.append({
                'region': region,
                'count': count,
                'percentage': round(percentage, 1),
                'avg_salary_expectation': f'{avg_salary}만원',
                'avg_quality_score': round(quality_score, 1),
                'top_position': random.choice(['프론트엔드 개발자', '백엔드 개발자', 'UI/UX 디자이너'])
            })
        
        return pd.DataFrame(regional_data)
    
    @st.cache_data(ttl=3600)
    def generate_funnel_data(_self) -> pd.DataFrame:
        """채용 퍼널 데이터 생성"""
        # 실제적인 전환율을 반영한 퍼널
        total_applicants = 3500
        
        funnel_stages = [
            ('총 지원자', total_applicants, 100.0),
            ('서류 통과', int(total_applicants * 0.45), 45.0),
            ('1차 면접', int(total_applicants * 0.25), 25.
