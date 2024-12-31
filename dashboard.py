import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# 데이터 로드 함수
def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        st.error("CSV 파일을 찾을 수 없습니다. 데이터를 생성한 후 다시 시도해주세요.")
        return pd.DataFrame()

# 메인 대시보드 함수
def main():
    st.set_page_config(page_title="로또 번호 예측 대시보드", layout="wide")
    st.title("로또 번호 예측 대시보드 🎲")
    
    # 데이터 로드
    file_path = "predictions.csv"
    data = load_data(file_path)

    if data.empty:
        st.warning("데이터가 없습니다. 예측 결과를 생성한 후 다시 실행해주세요.")
        return

    # 데이터 테이블
    st.subheader("📋 예측 데이터 테이블")
    st.dataframe(data)

    # 빈도수 분석
    st.subheader("📊 번호 빈도수 분석")
    all_numbers = data.iloc[:, 1:].values.flatten()
    frequency = pd.Series(all_numbers).value_counts().sort_index()
    
    # 막대 그래프
    st.bar_chart(frequency, height=400)

    # 상위 빈도 번호 표시
    top_numbers = frequency.sort_values(ascending=False).head(10)
    st.write("🔢 **가장 많이 예측된 번호**")
    for i, (number, count) in enumerate(top_numbers.items(), 1):
        st.write(f"{i}위: {number} (빈도: {count})")

    # 회차 선택 필터
    st.subheader("🔍 특정 회차 데이터 보기")
    회차목록 = data["날짜"].unique()
    선택된_회차 = st.selectbox("회차 선택", 회차목록)
    필터링된_데이터 = data[data["날짜"] == 선택된_회차]
    st.write(f"선택된 회차 데이터:")
    st.dataframe(필터링된_데이터)

# 실행
if __name__ == "__main__":
    main()
