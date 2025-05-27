"""
채용 대시보드 설정 파일
"""

import streamlit as st
from datetime import datetime, timedelta

# 페이지 설정
PAGE_CONFIG = {
    "page_title": "종합 채용 대시보드",
    "page_icon": "👥",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# 색상 팔레트
COLORS = {
    "primary": "#3b82f6",
    "secondary": "#8b5cf6", 
    "success": "#10b981",
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "info": "#06b6d4",
    "light": "#f8fafc",
    "dark": "#1e293b"
}

# 상태별 색상 매핑
STATUS_COLORS = {
    '서류 심사': '#3b82f6',
    '1차 면접': '#f59e0b', 
    '2차 면접': '#f59e0b',
    '최종 면접': '#ef4444', 
    '합격': '#10b981',
    '불합격': '#6b7280'
}

# 직무 카테고리
JOB_CATEGORIES = {
    '개발': ['프론트엔드 개발자', '백엔드 개발자', 'DevOps 엔지니어', '머신러닝 엔지니어'],
    '디자인': ['UI/UX 디자이너', '프로덕트 디자이너', '그래픽 디자이너'],
    '데이터': ['데이터 분석가', '데이터 사이언티스트', '데이터 엔지니어'],
    '기획': ['프로덕트 매니저', '서비스 기획자', '비즈니스 분석가'],
    '품질': ['QA 엔지니어', 'QC 담당자', '테스트 엔지니어']
}

# 채용 채널
RECRUITMENT_CHANNELS = [
    '사람인', '잡코리아', '링크드인', '원티드', 
    '직접지원', '추천', 'GitHub Jobs', '프로그래머스'
]

# 지역 목록
REGIONS = [
    '서울', '경기', '부산', '대구', '인천', 
    '광주', '대전', '울산', '세종', '기타'
]

# 경력 구분
EXPERIENCE_LEVELS = [
    '신입', '1년', '2년', '3년', '4년', 
    '5년', '6년', '7년', '8년', '9년', '10년 이상'
]

# 채용 프로세스 단계
RECRUITMENT_STAGES = [
    '지원접수', '서류 심사', '1차 면접', 
    '2차 면접', '최종 면접', '합격', '불합격'
]

# 기본 필터 설정
DEFAULT_FILTERS = {
    'date_range': (datetime.now() - timedelta(days=30), datetime.now()),
    'items_per_page': 10,
    'chart_height': 400
}

# API 설정 (실제 환경에서는 환경변수 사용)
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'recruitment_db',
    'user': 'admin',
    'password': 'password'  # 실제로는 환경변수에서 가져오기
}

# 이메일 설정
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'email': 'hr@company.com',
    'password': 'app_password'  # 실제로는 환경변수에서 가져오기
}

# 대시보드 메뉴 구성
DASHBOARD_MENU = {
    "📈 대시보드 개요": "dashboard_overview",
    "👥 지원자 관리": "candidate_management", 
    "🔄 채용 퍼널": "recruitment_funnel",
    "📊 채널 성과": "channel_performance",
    "📍 분석 리포트": "analytics_report",
    "🤖 AI 인사이트": "ai_insights"
}

# 알림 설정
NOTIFICATION_SETTINGS = {
    'new_application_threshold': 10,  # 하루 지원자 수 임계값
    'interview_reminder_days': 1,     # 면접 리마인더 (일)
    'resume_score_threshold': 80      # 우수 이력서 점수 기준
}

def load_custom_css():
    """커스텀 CSS 스타일 로드"""
    return """
    <style>
        /* 메인 헤더 스타일 */
        .main-header {
            font-size: 3rem;
            font-weight: bold;
            background: linear-gradient(90deg, #3b82f6, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 2rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        
        /* 메트릭 카드 스타일 */
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin: 0.5rem 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
        }
        
        /* 사이드바 헤더 */
        .sidebar-header {
            font-size: 1.5rem;
            font-weight: bold;
            color: #3b82f6;
            margin-bottom: 1rem;
            text-align: center;
            padding: 1rem 0;
            border-bottom: 2px solid #e5e7eb;
        }
        
        /* 상태 배지 */
        .status-badge {
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: bold;
            margin: 0.2rem;
            display: inline-block;
        }
        
        .status-review { background-color: #dbeafe; color: #1e40af; }
        .status-interview { background-color: #fef3c7; color: #92400e; }
        .status-final { background-color: #fed7aa; color: #ea580c; }
        .status-pass { background-color: #dcfce7; color: #166534; }
        .status-fail { background-color: #fee2e2; color: #991b1b; }
        
        /* 지원자 카드 */
        .candidate-card {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
        }
        
        .candidate-card:hover {
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }
        
        /* 인사이트 카드 */
        .insights-card {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1rem 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .recommendation-card {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1rem 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        /* 푸터 */
        .footer {
            text-align: center;
            color: #6b7280;
            font-size: 0.9rem;
            margin-top: 3rem;
            padding: 2rem 0;
            border-top: 1px solid #e5e7eb;
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        }
        
        /* 알림 스타일 */
        .notification-card {
            background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
            color: white;
            padding: 1rem;
            border-radius: 8px;
            margin: 0.5rem 0;
            font-weight: 500;
        }
        
        /* 통계 카드 */
        .stats-card {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 1rem;
            text-align: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        /* 프로그레스 바 커스터마이징 */
        .stProgress .st-bo {
            background-color: #e5e7eb;
        }
        
        /* 버튼 스타일 */
        .action-button {
            background: linear-gradient(135deg, #3b82f6, #1d4ed8);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .action-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        }
        
        /* 테이블 스타일 */
        .dataframe {
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        /* 탭 스타일 */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            background-color: #f8fafc;
            border-radius: 8px;
            border: 1px solid #e5e7eb;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #3b82f6, #1d4ed8);
            color: white;
        }
    </style>
    """

# 차트 설정
CHART_CONFIG = {
    'funnel': {
        'colors': ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4'],
        'height': 500
    },
    'bar': {
        'color_scale': 'viridis',
        'height': 400
    },
    'pie': {
        'colors': ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'],
        'height': 400
    },
    'line': {
        'colors': ['#3b82f6', '#10b981', '#f59e0b', '#ef4444'],
        'height': 400
    }
}

# 데이터 새로고침 주기 (초)
REFRESH_INTERVALS = {
    'real_time': 30,
    'hourly': 3600,
    'daily': 86400
}
