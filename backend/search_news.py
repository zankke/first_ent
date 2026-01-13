import os
import time
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
# from serpapi import GoogleSearch
from serpapi.client import GoogleSearch

import pandas as pd

# Optional: natural-language dates like "2 hours ago"
try:
    import dateparser
except Exception:
    dateparser = None

load_dotenv()
SERP_API_KEY = os.getenv("SERPAPI_API_KEY") or os.getenv("SERP_API_KEY")

def _parse_date(s: str):
    """Parse SerpAPI news 'date' which may be absolute or relative."""
    if not s:
        return pd.NaT
    s = str(s).strip()

    dt = pd.to_datetime(s, errors="coerce")
    if pd.notna(dt):
        return dt
    # Try dateparser if installed (handles '2 hours ago', etc.)
    if dateparser:
        dt2 = dateparser.parse(s, settings={"TIMEZONE": "UTC", "RETURN_AS_TIMEZONE_AWARE": True})
        if dt2:
            return dt2
    return pd.NaT

def search_news_serpapi(query: str, max_retries: int = 3) -> pd.DataFrame:
  
    load_dotenv()
    SERP_API_KEY = os.getenv("SERPAPI_API_KEY") or os.getenv("SERP_API_KEY")
  
    if not SERP_API_KEY:
        raise RuntimeError("SERPAPI_API_KEY environment variable is not set.")

    params = {
        "api_key": SERP_API_KEY,
        "engine": "google_news",
        "hl": "ko",
        "gl": "kr",
        "q": query,
        "no_cache": True,
    }

    results = None
    last_error = None
    
    for attempt in range(max_retries):
        try:
            print(f"SerpAPI 요청 시도 {attempt + 1}/{max_retries}")
            results = GoogleSearch(params).get_dict()
            news_results = results.get('news_results', [])
            if not news_results:
                print("뉴스 결과를 찾을 수 없습니다.")
                return pd.DataFrame()
            else:
                for news in news_results[:10]:
                    print(news.get('source', '출처 없음'))
                break  # 성공하면 루프 종료
        except Exception as e:
            last_error = e
            print(f"SerpAPI 요청 시도 {attempt + 1} 실패: {e}")
            print(f"에러 타입: {type(e).__name__}")
            print(f"에러 메시지: {str(e)}")
            
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 2  # 점진적으로 대기 시간 증가
                print(f"{wait_time}초 후 재시도...")
                time.sleep(wait_time)
            else:
                print("최대 재시도 횟수에 도달했습니다.")
                raise RuntimeError(f"SerpAPI request failed after {max_retries} attempts: {last_error}")

    # results가 None인 경우를 방지
    if results is None:
        print("API 응답을 받지 못했습니다.")
        return pd.DataFrame()

    news = results.get("news_results", [])
    if not isinstance(news, list) or not news:
        print("뉴스 결과를 찾을 수 없습니다.")
        return pd.DataFrame()

    # Normalize into DataFrame safely
    df = pd.DataFrame(news)

    processed_news = []
    for item in news:
        thumbnail = item.get("thumbnail", {}).get("url", "N/A")
        source = item.get("source", "N/A")
        title = item.get("title", "N/A")
        snippet = item.get("snippet", "본문 요약 없음")
        MAX_CHARS = 150
        trimmed_snippet = (snippet[:MAX_CHARS] + '.......') if len(snippet) > MAX_CHARS else snippet
        link = item.get("link", "N/A")

        processed_news.append({
            "thumbnail": thumbnail,
            "source": source,
            "title": title,
            "snippet": trimmed_snippet,
            "link": link,
            "date": item.get("date", "N/A") # Keep date for sorting/display
        })
    
    df = pd.DataFrame(processed_news)
    df = df.reset_index(drop=True)
    return df

def search_news_ui():
  import streamlit as st
  import functions as fns
  
  st.subheader(":material/search: Google News 검색", divider=True)
  
  df = pd.DataFrame()
  with st.container(border=True):
    r = st.columns([1.5,2,1], gap="small")
    sample_query = "캐치티니핑+케데헌+주가"
    r[0].caption(":material/search: 검색어 입력\n( 예 : {sample_query} )")
    use_sample = r[0].checkbox(f"샘플 검색어 사용\n(예:{sample_query})", value=False)
    if use_sample:
      query_kwd = r[1].text_input("검색어를 입력해 주세요(예:{sample_query})", value=sample_query, label_visibility="collapsed")
    else:
      query_kwd = r[1].text_input("검색어를 입력해 주세요(예:{sample_query})", placeholder=sample_query, label_visibility="collapsed")

    submit = r[2].button("Start Search", type="primary", icon=":material/search:", use_container_width=True)
    
    if submit:
      if use_sample:
        query_kwd = "캐치티니핑+케데헌+주가"
      if not query_kwd:
        st.error("검색어를 입력해 주세요.")
        st.stop()
      with st.spinner(":blue[:material/automation: [AI Report] Google News 검색 중...]"):
        df = search_news_serpapi(query_kwd)
    
    if not df.empty:
      df = df.applymap(lambda x: str(x) if isinstance(x, dict) else x)
      
      with st.container(border=True):
        st.subheader(":material/table_rows: 검색 결과", divider=True)
        fns.display_data_grid(df)
        
        for index, row in df.iterrows():
            with st.container():
                col1, col2 = st.columns([1, 3])
                with col1:
                    thumbnail = row.get("thumbnail")
                    if thumbnail and thumbnail != "N/A":
                        st.image(thumbnail, use_container_width=True)
                    else:
                        st.write("이미지 없음")
                with col2:
                    st.markdown(f"**{row.get('title', '제목 없음')}**")
                    source_name = row.get('source', '')
                    st.badge(f"[{source_name if source_name else ''}]", icon=":material/newspaper:", color="primary")
                    st.badge(f"{row.get('date', '날짜 없음')}", icon=":material/calendar_month:")
                    st.markdown(f"{row.get('snippet', '본문 요약 없음')}")
                    st.markdown(f":red[[:material/open_in_new: 기사 원문 보기]({row.get('link', '#')})]")
                st.divider()

      with st.container(border=True):
        st.subheader(":material/cloud: 키워드 클라우드", divider=True)
        if "title" in df.columns:
          fns.display_word_cloud(df["title"], width=1000, background_color='white')
      
    # st.write(df)


if __name__ == "__main__":
    query = "캐치티니핑+케데헌+주가"
    df = search_news_serpapi(query)

    # Save CSV
    result_path = "./responses/news"
    os.makedirs(result_path, exist_ok=True)
    file_name = f'google_news_search_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    out_path = os.path.join(result_path, file_name)

    df.to_csv(out_path, index=False, encoding="utf-8")
    print(f"News results saved to {out_path}")
    print(df.columns.tolist())
    print("=" * 60)
    print(df.head(10))
