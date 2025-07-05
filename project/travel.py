import sqlite3

def recommend_places_by_mbti(mbti_type):
<<<<<<< HEAD
    # 1. SQLite DB 연결
    conn = sqlite3.connect("project/database/mbti_places.db")
    cursor = conn.cursor()

    # 2. SQL 실행 (대소문자 무관 검색을 위해 대문자로 변환)
    query = """
    SELECT mbti_recommendation, country, city_or_area, region_type, continent, description
    FROM places
    WHERE UPPER(mbti_recommendation) = UPPER(?)
    """
    cursor.execute(query, (mbti_type,))
    results = cursor.fetchall()

    # 3. 결과 출력
    if results:
        print(f"\n🔍 MBTI 유형 '{mbti_type.upper()}'에 추천되는 여행지 {len(results)}곳:")
        for i, row in enumerate(results, 1):
            print(f"\n[{i}] {row[1]} - {row[2]} ({row[3]}, {row[4]})\n → {row[5]}")
    else:
        print(f"\n '{mbti_type}'에 해당하는 여행지 추천이 없습니다.")

    # 4. 종료
    conn.close()
=======
    try:
        # 1. SQLite DB 연결
        conn = sqlite3.connect("project/database/mbti_places.db")
        cursor = conn.cursor()

        # 2. SQL 실행 (대소문자 무관 검색을 위해 대문자로 변환)
        query = """
        SELECT mbti_recommendation, country, city_or_area, region_type, continent, description
        FROM places
        WHERE UPPER(mbti_recommendation) = UPPER(?)
        """
        cursor.execute(query, (mbti_type,))
        results = cursor.fetchall()
        
        # 3. 결과 포맷팅
        if results:
            formatted_results = [f"🔍 {mbti_type.upper()} 유형님을 위한 추천 여행지\n"]
            for i, row in enumerate(results, 1):
                formatted_results.append(f"{i}. {row[1]} - {row[2]} ({row[3]}, {row[4]})\n   → {row[5]}\n")
            return "\n".join(formatted_results)
        else:
            return f"'{mbti_type}'에 해당하는 여행지 추천이 없습니다."
            
    except Exception as e:
        print(f"여행지 추천 중 오류 발생: {e}")
        return "여행지 추천을 가져오는 중 오류가 발생했습니다."
    finally:
        # 4. 종료
        conn.close()
>>>>>>> api-integrator

# 5. 사용자 입력 받기
if __name__ == "__main__":
    user_mbti = input("🔎 MBTI 유형을 입력하세요 (예: INFP, ESTJ 등): ")
    recommend_places_by_mbti(user_mbti)
