import json
import time
import re
import os
from datetime import datetime, timedelta, timezone
import firebase_admin
from firebase_admin import credentials, db
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# ... (Firebase 초기화 부분은 기존과 동일하므로 중략) ...

def clean_num(text):
    if not text: return 0
    # 모든 텍스트에서 숫자와 점(.)만 남기고 나머지는 제거한 뒤 숫자 뭉치들을 리스트로 반환
    nums = re.findall(r'\d[\d,.]*', text.replace(',', ''))
    return nums

def run_mtpl_final_engine():
    url = "https://metaplanet.jp/jp/analytics"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        print(f"🌐 메타플래닛 접속 시작: {url}")
        driver.get(url)
        print("⏳ 15초 대기 중... (사이트 로딩 및 데이터 렌더링)")
        time.sleep(15) 

        # 모든 텍스트 엘리먼트 수집
        elements = driver.find_elements(By.CSS_SELECTOR, "h1, h2, h3, h4, p, span, div")
        all_content = [el.text.strip() for el in elements if el.text.strip()]

        # --- [사장님 요청: 정밀 탐색 로직] ---
        # 기존에 사용하던 인덱스들
        target_indices = [12, 27, 42, 66, 77, 91, 340]
        
        print("\n🔍 [인덱스 정밀 탐색 보고서]")
        print("-" * 50)
        
        checked = set()
        for idx in sorted(target_indices):
            print(f"\n📍 기준 인덱스 {idx} 주변 (앞뒤 10칸):")
            for i in range(idx - 10, idx + 11):
                if i <= 0 or i > len(all_content) or i in checked:
                    continue
                
                raw_text = all_content[i-1]
                nums = clean_num(raw_text)
                
                # 숫자 뭉치 최대 3개까지만 포맷팅
                num_display = " / ".join(nums[:3]) if nums else "숫자 없음"
                print(f"Index {i:03d}: {num_display}")
                checked.add(i)
        
        print("-" * 50)
        print("위 로그에서 정확한 데이터가 위치한 Index 번호를 확인해 주세요, 사장님!")

        # ------------------------------------------------------------------
        # 아래 부분은 번호 확인 후 다시 복구할 부분입니다 (현재는 스킵 방지용)
        # ------------------------------------------------------------------
        
    except Exception as e:
        print(f"❌ 실행 중 오류 발생: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_mtpl_final_engine()
