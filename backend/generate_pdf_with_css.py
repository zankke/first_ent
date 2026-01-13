import xml.etree.ElementTree as ET
from weasyprint import HTML, CSS
import os

# ----------------------------------------------------------------------
# I. 고윤정 배우 7P 정보 기반 XML 데이터 (소스 [1], [2], [3], [4] 기반)
# ----------------------------------------------------------------------
# 소스 [2]의 '고윤정' 페이지에 있는 모든 정보를 구조화했습니다.
SAMPLE_XML_DATA = """
<ArtistProfile name="고윤정" source="R.book_03_7P" category="R.celeb">
    <BasicInfo birthYear="1996" estimatedAnnualModelFee="1년 8억"/>
    <SocialMedia platform="X">
        <Posts count="386"/>
        <Followers count="782.8만"/>
        <AverageViews count="991.93만"/>
        <AudienceDemographics>
            <Region main="한국" percentage="59.3%"/>
            <Gender main="여성" percentage="65.4%"/>
            <Age main="18-24" percentage="32.6%"/>
            <FollowerTop5Regions>
                <Region name="한국" percentage="59.3%"/>
                <Region name="미국" percentage="16.5%"/>
                <Region name="인도네시아" percentage="4.5%"/>
                <Region name="캐나다" percentage="1.8%"/>
                <Region name="태국" percentage="1.6%"/>
            </FollowerTop5Regions>
            <FollowerAgeBreakdown>
                <AgeGroup range="13-17" percentage="8.7%"/>
                <AgeGroup range="18-24" percentage="32.6%"/>
                <AgeGroup range="25-34" percentage="20.9%"/>
                <AgeGroup range="35-44" percentage="17.6%"/>
            </FollowerAgeBreakdown>
        </AudienceDemographics>
        <CountrySearchVolume recent90Days="true">
            <Country name="한국" index="100"/>
            <Country name="인도네시아" index="23"/>
            <Country name="미얀마" index="19"/>
            <Country name="대만" index="16"/>
            <Country name="홍콩" index="15"/>
        </CountrySearchVolume>
    </SocialMedia>
    <AdvertisingContracts>
        <Contract name="하이엔드뷰티" scope="신규/글로벌"/>
        <Contract name="마리떼"/>
        <Contract name="NH농협은행" scope="국내" contractPeriod="2024.04~/12개월"/> 
        <Contract name="상쾌환"/>
        <Contract name="렌즈미"/>
        <Contract name="푸라닭"/>
        <Contract name="디스커버리"/>
        <Contract name="캐롯손해보험" scope="국내" contractPeriod="2023.07~/12개월"/>
        <Contract name="샤넬" scope="글로벌"/>
        <Contract name="디디에두보" scope="한국+홍콩"/>
        <Contract name="려" scope="한국+대만+싱가폴+말레이시아+태국"/>
    </AdvertisingContracts>
    <Projects>
        <TV name="언젠가는 슬기로울 전공의 생활" platform="tvN" status="방영예정" date="04.12"/>
        <NETFLIX name="이 사랑 통역 되나요?" status="방영예정" date="2025"/>
    </Projects>
</ArtistProfile>
"""

# ----------------------------------------------------------------------
# II. PDF 생성 함수 (레이아웃 최적화된 HTML 템플릿 사용)
# ----------------------------------------------------------------------

def generate_artist_profile_pdf_with_css(xml_data, css_file_path, output_filename="artist_profile_goyounjung.pdf"):

    root = ET.fromstring(xml_data)
    artist_name = root.get('name', 'N/A')
    source = root.get('source', 'N/A')
    category = root.get('category', 'N/A')
    SAVE_PATH='./responses/report'

    # CSS 파일 경로 확인 및 로드 (이 경로는 `./static/css/artist_profile.css`로 가정함)
    if not os.path.exists(css_file_path):
        print(f"오류: CSS 파일 경로를 찾을 수 없습니다: {css_file_path}")
        return

    with open(css_file_path, 'r', encoding='utf-8') as f:
        css_data = f.read()

    # --- 레이아웃 반영을 위한 HTML 구조 시작 ---
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{artist_name} Profile - {source}</title>
        <style>
            {css_data}
        </style>
    </head>
    <body>
    <div class="R-book-7P-layout">
        
        <!-- 1. 헤더 섹션 (R.celeb, 아티스트명, 모델료) [1, 2] -->
        <div class="profile-header">
            <span class="category-tag">{category}</span>
            <span class="x-logo">X</span>
            
            <div class="artist-identity">
                <h1 class="artist-name">{artist_name}</h1>
                <p class="artist-birth-year">{root.find('BasicInfo').get('birthYear', 'N/A')}</p>
            </div>
            
            <div class="model-fee-box">
                <span class="fee-label">1년</span>
                <span class="estimated-fee">{root.find('BasicInfo').get('estimatedAnnualModelFee', 'N/A')}</span>
            </div>
        </div>

        <!-- 아티스트 이미지/핵심 정보 영역 (소스의 시각적 요소) [2] -->
        <div class="artist-main-visual">
            <div class="image-placeholder">[image: GO YOUNJUNG Profile Image]</div>
        </div>

        <!-- 2. 메인 콘텐츠 랩퍼 (소스의 2단/그리드 구성을 위해) -->
        <div class="main-content-wrapper">
            
            <!-- A. 좌측 상단: 소셜 미디어 지표 [1] -->
            <div class="section social-metrics-section">
                <div class="metrics-grid">
                    <div class="metric-box">
                        <span class="metric-label">게시물</span>
                        <span class="metric-count">{root.find('SocialMedia/Posts').get('count', 'N/A')}</span>
                    </div>
                    <div class="metric-box">
                        <span class="metric-label">팔로워</span>
                        <span class="metric-count">{root.find('SocialMedia/Followers').get('count', 'N/A')}</span>
                    </div>
                    <div class="metric-box">
                        <span class="metric-label">평균 조회수</span>
                        <span class="metric-count">{root.find('SocialMedia/AverageViews').get('count', 'N/A')}</span>
                    </div>
                </div>
            </div>

            <!-- B. 주요 오디언스 요약 [1] -->
            <div class="section audience-summary-section">
                <div class="audience-box">
                    <p class="audience-label">주요 오디언스 지역</p>
                    <p class="audience-value">{root.find('SocialMedia/AudienceDemographics/Region').get('main', 'N/A')} ({root.find('SocialMedia/AudienceDemographics/Region').get('percentage', 'N/A')})</p>
                </div>
                <div class="audience-box">
                    <p class="audience-label">주요 오디언스 성별</p>
                    <p class="audience-value">{root.find('SocialMedia/AudienceDemographics/Gender').get('main', 'N/A')} ({root.find('SocialMedia/AudienceDemographics/Gender').get('percentage', 'N/A')})</p>
                </div>
                <div class="audience-box">
                    <p class="audience-label">주요 오디언스 연령</p>
                    <p class="audience-value">{root.find('SocialMedia/AudienceDemographics/Age').get('main', 'N/A')} ({root.find('SocialMedia/AudienceDemographics/Age').get('percentage', 'N/A')})</p>
                </div>
            </div>

            <!-- C. 데이터 시각화 및 TOP 5 목록 [2] -->
            <div class="section data-visualization-area">
                
                <!-- 1. 팔로워 연령 비율 (막대 그래프) [2] -->
                <div class="chart-container age-chart">
                    <p class="chart-title">• 팔로워 연령 비율</p>
                    <div class="chart-wrapper">
                        
    """
    age_groups = root.findall('SocialMedia/AudienceDemographics/FollowerAgeBreakdown/AgeGroup')
    max_percentage = 32.6 
    
    # 연령 비율 그래프 생성
    for age_group in age_groups:
        age_range = age_group.get('range', 'N/A')
        percentage_str = age_group.get('percentage', '0%').replace('%', '')
        percentage = float(percentage_str) if percentage_str.replace('.', '').isdigit() else 0
        
        # 막대 그래프의 높이를 비율에 따라 조정 (CSS에서 배경색 정의 필요)
        bar_height = (percentage / max_percentage) * 100 if max_percentage > 0 else 0
        
        html_content += f"""
                        <div class="age-bar-item">
                            <div class="bar-range">{age_range}</div>
                            <div class="bar-fill" style="height: {bar_height:.1f}%"></div>
                            <div class="bar-percentage">{percentage:.1f}%</div>
                        </div>
        """
    html_content += f"""
                    </div>
                </div>

                <!-- 2. 인스타 팔로워 TOP 5 [2] -->
                <div class="list-container follower-top5">
                    <p class="list-title">• 인스타 팔로워 TOP5</p>
                    <ul class="region-list">
    """
    regions = root.findall('SocialMedia/AudienceDemographics/FollowerTop5Regions/Region')
    for region in regions:
        region_name = region.get('name', 'N/A')
        percentage = region.get('percentage', 'N/A')
        html_content += f"""
                        <li>{region_name} <span class="percentage-value">{percentage}</span></li>
        """
    html_content += f"""
                    </ul>
                </div>

                <!-- 3. 국가별 검색량 (인덱스 막대 그래프) [2] -->
                <div class="chart-container search-volume-chart">
                    <p class="chart-title">• 국가별 검색량 (최근 90일)</p>
                    <div class="index-wrapper">
    """
    countries = root.findall('SocialMedia/CountrySearchVolume/Country')
    max_index = 100 
    
    # 국가별 검색량 그래프 생성
    for country in countries:
        country_name = country.get('name', 'N/A')
        index = int(country.get('index', '0'))
        
        # 막대 그래프의 길이를 인덱스에 따라 조정
        bar_width = (index / max_index) * 100 if max_index > 0 else 0
        
        html_content += f"""
                        <div class="search-bar-item">
                            <span class="country-name">{country_name}</span>
                            <div class="index-bar-background">
                                <div class="index-bar-fill" style="width: {bar_width:.1f}%"></div>
                            </div>
                            <span class="country-index">{index}</span>
                        </div>
        """
    html_content += f"""
                    </div>
                </div>
            </div> 

            <!-- D. 광고 계약 및 프로젝트 섹션 [2] -->
            <div class="section contract-project-section">
                
                <h2 class="section-title">AD</h2>
                <div class="contract-list">
    """
    # 광고 목록 처리 (소스 [2], [3], [4] 정보 통합)
    contracts = []
    for contract in root.findall('AdvertisingContracts/Contract'):
        name = contract.get('name', 'N/A')
        scope = contract.get('scope', 'N/A')
        period = contract.get('contractPeriod', 'N/A')
        
        detail = ""
        if scope != 'N/A':
            detail += scope
        if period != 'N/A':
            if scope != 'N/A':
                detail += "/"
            detail += period
            
        if detail:
            # 소스 [2]과 [3]에서 광고주가 쉼표로 나열되어 있음을 반영하여 처리
            contracts.append(f"{name}{' (' + detail + ')' if detail else ''}")
        else:
            contracts.append(name)
            
    html_content += f"""
                    <p>{', '.join(contracts)}</p>
    """
    html_content += f"""
                </div>

                <h2 class="section-title">Projects</h2>
                <div class="project-list">
    """
    # 프로젝트 목록 처리 [2]
    for project in root.findall('Projects/TV'):
        name = project.get('name', 'N/A')
        platform = project.get('platform', 'N/A')
        status = project.get('status', 'N/A')
        date = project.get('date', 'N/A')
        html_content += f"""
                    <p class="project-item tv-project">TV: {platform} {name} ({date} {status})</p>
        """
        
    for project in root.findall('Projects/NETFLIX'):
        name = project.get('name', 'N/A')
        status = project.get('status', 'N/A')
        date = project.get('date', 'N/A')
        html_content += f"""
                    <p class="project-item netflix-project">NETFLIX: {name} ({date} {status})</p>
        """
    
    html_content += f"""
                </div>
                
                <!-- 고윤정 최근 관심도 차트 Placeholder [2] -->
                <div class="recent-interest-placeholder">[image: 고윤정 최근 관심도 그래프]</div>
                
            </div> 
        </div> 

    </div>
    </body>
    </html>
    """

    # WeasyPrint를 사용하여 HTML을 PDF로 변환
    try:
        HTML(string=html_content, base_url=os.getcwd()).write_pdf(output_filename, stylesheets=[CSS(css_file_path)])
        print(f"PDF 파일이 성공적으로 생성되었습니다: {output_filename}")
    except Exception as e:
        print(f"PDF 생성 중 오류 발생: {e}")
        # Note: WeasyPrint는 정확한 PDF 생성을 위해 시스템에 필요한 라이브러리(예: Cairo)가 설치되어 있어야 합니다.

if __name__ == "__main__":
    CSS_FILE_PATH = "./static/css/artist_profile.css" 
    
    if not os.path.exists(os.path.dirname(CSS_FILE_PATH)):
        pass 
    
    # 레이아웃을 정확히 반영하려면 artist_profile.css 파일에
    # R-book-7P-layout, profile-header, metrics-grid, chart-wrapper 등의
    # 클래스에 대한 상세한 스타일 정의가 포함되어야 합니다.

    generate_artist_profile_pdf_with_css(
        xml_data=SAMPLE_XML_DATA, 
        css_file_path=CSS_FILE_PATH,
        output_filename=f"Test_프로필.pdf"
    )