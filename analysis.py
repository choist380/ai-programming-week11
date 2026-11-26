import pandas as pd


def 정제(df):
    # 원본 손상을 막기 위해 데이터프레임 복사본을 생성합니다.
    df = df.copy()
    print("시작:", len(df))

    # 1) 점수가 비어 있는 행을 삭제합니다.
    df = df.dropna(subset=["점수"])
    print("빈 칸 제거 후:", len(df))

    # 2) 모든 열이 완전히 같은 중복 행은 하나만 남깁니다.
    df = df.drop_duplicates()
    print("중복 제거 후:", len(df))

    # 3) 반과 과목 문자열의 앞뒤 공백을 제거합니다.
    df["반"] = df["반"].str.strip()
    df["과목"] = df["과목"].str.strip()
    print("공백 제거 후:", len(df))

    # 4) 점수가 0 이상 100 이하인 행만 남깁니다.
    df = df[(df["점수"] >= 0) & (df["점수"] <= 100)]
    print("범위 밖 제거 후:", len(df))

    return df


def 반별평균(df):
    # 반으로 묶어 점수 평균을 구한 뒤 딕셔너리 형태로 반환합니다.
    return df.groupby("반")["점수"].mean().to_dict()


if __name__ == "__main__":
    # 데이터 불러오기 (cp949 파일의 경우 encoding="cp949" 옵션 추가)
    raw_df = pd.read_csv("scores_2026.csv")
    clean_df = 정제(raw_df)

    # B. 필터링 (STEP 3-①)
    math_df = clean_df[clean_df["과목"] == "수학"]
    print("수학 과목 행 수:", len(math_df))

    class1_high_df = clean_df[(clean_df["반"] == "1반") & (clean_df["점수"] >= 90)]
    print("1반 90점 이상 행 수:", len(class1_high_df))

    # C. 그룹화 (STEP 3-②)
    print("\n[반별 평균]")
    print(clean_df.groupby("반")["점수"].mean())

    print("\n[과목 및 반별 평균]")
    print(clean_df.groupby(["과목", "반"])["점수"].mean())

    # D. 통계 (STEP 3-③)
    print("\n[반별 요약 통계]")
    stats = (
        clean_df.groupby("반")["점수"]
        .agg(개수="count", 평균="mean", 중앙값="median", 최댓값="max")
        .round(2)
    )
    print(stats)