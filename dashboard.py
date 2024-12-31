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

# 대시보드 시각화 함수
def visualize_data(data):
    st.title("로또 번호 예측 대시보드")
    st.subheader("예측된 로또 번호")
    
    # 데이터 테이블 표시
    st.dataframe(data)

    # 히스토그램
    if not data.empty:
        all_numbers = data.iloc[:, 1:].values.flatten()  # 모든 번호를 하나의 배열로 변환
        plt.hist(all_numbers, bins=range(1, 47), edgecolor='black', alpha=0.7)
        plt.title("예측 번호 분포")
        plt.xlabel("번호")
        plt.ylabel("빈도")
        st.pyplot(plt)

if __name__ == "__main__":
    # CSV 파일 경로
    file_path = "predictions.csv"
    
    # 데이터 로드
    data = load_data(file_path)

    # 데이터 시각화
    visualize_data(data)
