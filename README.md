# 🎯 종합 채용 대시보드

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.29.0-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

> 데이터 기반 채용 운영 분석으로 더 나은 인재 확보 전략을 수립하는 종합 대시보드

## 📊 주요 기능

### 🎯 핵심 지표 모니터링
- 총 지원자 수 및 증감률
- 단계별 전환율 분석
- 평균 채용 리드타임
- 채널별 CPA (Cost Per Acquisition)

### 👥 지원자 관리
- 실시간 검색 및 필터링
- 상세 지원자 프로필
- 상태별 진행 현황
- 이력서 점수 분석

### 📈 데이터 분석
- 채용 퍼널 시각화
- 채널별 성과 분석
- 지역/경력별 분포
- 월별 트렌드 분석

### 🤖 AI 인사이트
- 데이터 기반 발견사항
- 개선 권장사항
- 예측 분석
- 최적화 제안

## 🚀 빠른 시작

### 1. 저장소 클론
```bash
git clone https://github.com/your-username/recruitment-dashboard.git
cd recruitment-dashboard
```

### 2. 가상환경 설정 (권장)
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 애플리케이션 실행
```bash
streamlit run app.py
```

브라우저에서 `http://localhost:8501`로 접속하세요!

## 📦 설치 요구사항

- Python 3.8+
- Streamlit 1.29.0+
- Pandas 2.1.3+
- Plotly 5.17.0+
- Numpy 1.25.2+

## 🐳 Docker로 실행

### Docker 빌드 및 실행
```bash
docker build -t recruitment-dashboard .
docker run -p 8501:8501 recruitment-dashboard
```

### Docker Compose 사용
```bash
docker-compose up
```

## 📱 온라인 데모

🌐 **라이브 데모**: [Streamlit Cloud에서 보기](https://your-app.streamlit.app)

## 📸 스크린샷

### 메인 대시보드
![Dashboard](https://github.com/your-username/recruitment-dashboard/raw/main/assets/dashboard-screenshot.png)

### 지원자 관리
![Candidates](https://github.com/your-username/recruitment-dashboard/raw/main/assets/candidates-screenshot.png)

### 분석 리포트
![Analytics](https://github.com/your-username/recruitment-dashboard/raw/main/assets/analytics-screenshot.png)

## 🏗️ 프로젝트 구조

```
recruitment-dashboard/
├── app.py                 # 메인 애플리케이션
├── config.py             # 설정 파일
├── utils/                # 유틸리티 함수들
├── data/                 # 샘플 데이터
├── pages/                # 멀티페이지 구성
├── assets/               # 스타일 및 이미지
└── .streamlit/           # Streamlit 설정
```

## 🔧 커스터마이징

### 데이터 소스 변경
`utils/data_generator.py`에서 데이터 소스를 변경할 수 있습니다:

```python
# 실제 데이터베이스 연결 예시
import psycopg2
import pandas as pd

def load_candidates_from_db():
    conn = psycopg2.connect(
        host="your-host",
        database="your-db",
        user="your-user",
        password="your-password"
    )
    return pd.read_sql("SELECT * FROM candidates", conn)
```

### 스타일 커스터마이징
`assets/style.css`에서 UI 스타일을 수정할 수 있습니다.

### 새로운 차트 추가
`utils/charts.py`에서 새로운 시각화를 추가할 수 있습니다.

## 🔒 보안 고려사항

- 환경변수로 민감한 정보 관리
- API 키는 `.env` 파일 사용
- 데이터베이스 연결 시 SSL 사용 권장

## 🚀 배포

### Streamlit Cloud
1. GitHub 저장소 연결
2. 앱 설정에서 Python 버전 지정
3. requirements.txt 자동 인식

### Heroku
```bash
git push heroku main
```

### AWS/GCP
Docker 이미지를 사용하여 클라우드 플랫폼에 배포 가능

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 변경 로그

### v1.0.0 (2024-05-27)
- 초기 릴리즈
- 기본 대시보드 기능
- 지원자 관리 시스템
- AI 인사이트 기능

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 👥 개발팀

- **메인 개발자**: [Your Name](https://github.com/your-username)
- **데이터 분석**: [Contributor](https://github.com/contributor)

## 📞 문의

프로젝트 링크: [https://github.com/your-username/recruitment-dashboard](https://github.com/your-username/recruitment-dashboard)

이슈 리포트: [GitHub Issues](https://github.com/your-username/recruitment-dashboard/issues)

## 🙏 감사의 말

- [Streamlit](https://streamlit.io/) - 웹 앱 프레임워크
- [Plotly](https://plotly.com/) - 인터랙티브 차트
- [Pandas](https://pandas.pydata.org/) - 데이터 처리
- [NumPy](https://numpy.org/) - 수치 계산

---

⭐ 이 프로젝트가 도움이 되었다면 Star를 눌러주세요!
