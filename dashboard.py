import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# 데이터 로드 함수
def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"{file_path} 파일을 찾을 수 없습니다. 데이터를 확인하세요.")
        return pd.DataFrame()

# 비교 분석 함수
def compare_data(previous_data, prediction_data):
    st.subheader("📊 예측 데이터와 이전 당첨 번호 비교")
    if previous_data.empty or prediction_data.empty:
        st.warning("데이터가 부족합니다. 이전 데이터와 예측 데이터를 확인하세요.")
        return

    # 테이블 표시
    st.write("**이전 데이터**")
    st.dataframe(previous_data)
    st.write("**예측 데이터**")
    st.dataframe(prediction_data)

    # 회차 선택
    st.subheader("🔍 특정 회차 비교")
    회차목록 = previous_data["회차"].unique()
    선택된_회차 = st.selectbox("비교할 회차를 선택하세요:", 회차목록)

    # 선택된 회차 데이터 필터링
    이전_회차_데이터 = previous_data[previous_data["회차"] == 선택된_회차]
    예측_데이터 = prediction_data.head(1)  # 최근 예측 데이터 한 개 선택

    # 비교 결과 표시
    st.write(f"**선택된 회차: {선택된_회차}**")
    st.write("**이전 당첨 번호**")
    st.dataframe(이전_회차_데이터)

    st.write("**예측 번호**")
    st.dataframe(예측_데이터)

    # 번호 일치 여부 분석
    당첨_번호 = 이전_회차_데이터.iloc[0, 1:7].values
    예측_번호 = 예측_데이터.iloc[0, 1:7].values
    일치_번호 = set(당첨_번호) & set(예측_번호)

    st.write(f"**일치하는 번호: {일치_번호}**")
    st.write(f"일치 개수: {len(일치_번호)}")

    # 히스토그램
    st.subheader("📊 번호 분포 비교")
    plt.figure(figsize=(10, 5))
    plt.hist(당첨_번호, bins=range(1, 47), alpha=0.7, label="이전 당첨 번호")
    plt.hist(예측_번호, bins=range(1, 47), alpha=0.7, label="예측 번호")
    plt.legend(loc="upper right")
    plt.xlabel("번호")
    plt.ylabel("빈도")
    plt.title("번호 분포 비교")
    st.pyplot(plt)

# 메인 대시보드 함수
def main():
    st.set_page_config(page_title="로또 번호 비교 대시보드", layout="wide")
    st.title("로또 번호 비교 대시보드 🎲")

    # 데이터 로드
    previous_data_path = "previous_results.csv"  # 이전 당첨 데이터 경로
    prediction_data_path = "predictions.csv"  # 예측 데이터 경로
    previous_data = load_data(previous_data_path)
    prediction_data = load_data(prediction_data_path)

    # 데이터 비교
    compare_data(previous_data, prediction_data)

# 실행
if __name__ == "__main__":
    main()
