import os
import xml.etree.ElementTree as ET

from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

def _find_first_existing_font(font_paths):
    for path in font_paths:
        if os.path.isfile(path):
            return path
    return None

def _register_cjk_fonts():
    """
    Register CJK fonts. Use NanumGothic by default, else fallback to Helvetica.
    """
    font_candidates = [
        # NanumGothic candidates (권장 순서대로)
        ("NanumGothic", [
            '/usr/share/fonts/truetype/nanum/NanumGothic.ttf',
            '/usr/share/fonts/nanum/NanumGothic.ttf',
            '/Library/Fonts/NanumGothic.ttf',
            'NanumGothic.ttf'
        ]),
        ("NotoSansCJKkr-Regular", [
            '/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/truetype/noto/NotoSansCJKkr-Regular.otf',
            '/Library/Fonts/NotoSansCJKkr-Regular.otf',
            'NotoSansCJKkr-Regular.otf',
            '/usr/share/fonts/google-noto-cjk/NotoSansCJKkr-Regular.otf'
        ]),
        ("NotoSansCJKsc-Regular", [
            '/usr/share/fonts/google-noto-cjk/NotoSansCJKsc-Regular.otf',
            '/usr/share/fonts/opentype/noto/NotoSansCJKsc-Regular.otf',
            '/usr/share/fonts/truetype/noto/NotoSansCJKsc-Regular.otf',
            '/Library/Fonts/NotoSansCJKsc-Regular.otf',
            'NotoSansCJKsc-Regular.otf'
        ]),
    ]
    for font_name, paths in font_candidates:
        font_path = _find_first_existing_font(paths)
        if font_path:
            try:
                pdfmetrics.registerFont(TTFont(font_name, font_path))
                print(f"폰트 등록 성공: {font_name} ({font_path})")
                return font_name
            except Exception:
                continue
    import warnings
    warnings.warn("NanumGothic 폰트를 찾을 수 없습니다. 한글이 올바르게 출력되지 않을 수 있습니다. 디폴트 폰트(Helvetica)로 대체합니다.")
    return None

def add_paragraph(story, text, style):
    story.append(Paragraph(text, style))

def add_spacer(story, height=0.2):
    story.append(Spacer(1, height * inch))

def get_attribute(element, attr, default='N/A'):
    return element.get(attr, default) if element is not None else default

def generate_artist_profile_pdf(xml_data, output_filename="artist_profile.pdf"):
    fontname = _register_cjk_fonts() or "Helvetica"
    root = ET.fromstring(xml_data)

    doc = SimpleDocTemplate(
        output_filename,
        pagesize=landscape(letter),
        encoding='utf-8'
    )

    styles = getSampleStyleSheet()
    # Define or replace styles only if not exists
    def ensure_style(name, **kwargs):
        if name in styles:
            styles[name].__dict__.update(**kwargs)
        else:
            styles.add(ParagraphStyle(name=name, **kwargs))
    ensure_style('CustomTitle', fontSize=24, leading=28, alignment=TA_CENTER,
        spaceAfter=20, fontName=fontname)
    ensure_style('CustomHeading1', fontSize=18, leading=22, spaceAfter=12,
        fontName=fontname)
    ensure_style('CustomHeading2', fontSize=14, leading=18, spaceAfter=8,
        fontName=fontname)
    ensure_style('CustomBodyText', fontSize=10, leading=12, spaceAfter=6,
        fontName=fontname)
    ensure_style('CustomListItem', fontSize=10, leading=12, spaceAfter=3,
        leftIndent=20, fontName=fontname)

    s = styles  # shortcut

    story = []

    # Artist Name
    add_paragraph(story, f"아티스트 프로필: {root.get('name', 'N/A')}", s['CustomTitle'])
    add_spacer(story)

    # Basic Info
    add_paragraph(story, "기본 정보", s['CustomHeading1'])
    basic_info = root.find('BasicInfo')
    if basic_info is not None:
        add_paragraph(story, f"출생년도: {get_attribute(basic_info, 'birthYear')}", s['CustomBodyText'])
        add_paragraph(story, f"연간 모델 예상 개런티: {get_attribute(basic_info, 'estimatedAnnualModelFee')}", s['CustomBodyText'])
    add_spacer(story)

    # Social Media
    add_paragraph(story, "소셜 미디어", s['CustomHeading1'])
    social_media = root.find('SocialMedia')
    if social_media is not None:
        add_paragraph(story, f"플랫폼: {get_attribute(social_media, 'platform')}", s['CustomHeading2'])

        def add_simple_info(tag, label):
            el = social_media.find(tag)
            if el is not None:
                add_paragraph(story, f"{label}: {get_attribute(el, 'count')}", s['CustomBodyText'])
        add_simple_info('Posts', "게시물 수")
        add_simple_info('Followers', "팔로워")
        add_simple_info('AverageViews', "평균 조회수")

        audience_demographics = social_media.find('AudienceDemographics')
        if audience_demographics is not None:
            add_paragraph(story, "주요 오디언스", s['CustomHeading2'])
            def add_demo_info(tag, label, field='main'):
                el = audience_demographics.find(tag)
                if el is not None:
                    main = get_attribute(el, field)
                    perc = get_attribute(el, 'percentage')
                    add_paragraph(story, f"{label}: {main} ({perc})", s['CustomBodyText'])
            add_demo_info("Region", "주요 국가")
            add_demo_info("Gender", "주요 성별")
            add_demo_info("Age", "주요 연령대")

            # Top 5 Regions
            follower_top5 = audience_demographics.find('FollowerTop5Regions')
            if follower_top5 is not None:
                add_paragraph(story, "팔로워 상위 5개국:", s['CustomBodyText'])
                for region in follower_top5.findall('Region'):
                    add_paragraph(story, f"- {get_attribute(region, 'name')} ({get_attribute(region, 'percentage')})", s['CustomListItem'])

            # Follower Age Breakdown
            follower_ages = audience_demographics.find('FollowerAgeBreakdown')
            if follower_ages is not None:
                add_paragraph(story, "팔로워 연령대 분포:", s['CustomBodyText'])
                for age_group in follower_ages.findall('AgeGroup'):
                    add_paragraph(story, f"- {get_attribute(age_group, 'range')} ({get_attribute(age_group, 'percentage')})", s['CustomListItem'])

        # Country Search Volume
        country_volume = social_media.find('CountrySearchVolume')
        if country_volume is not None:
            add_paragraph(story, "검색지수 상위 국가 (최근 90일):", s['CustomHeading2'])
            for country in country_volume.findall('Country'):
                add_paragraph(story, f"- {get_attribute(country, 'name')}: 인덱스 {get_attribute(country, 'index')}", s['CustomListItem'])

    add_spacer(story)

    # Advertising Contracts
    add_paragraph(story, "광고 계약 현황", s['CustomHeading1'])
    advertising_contracts = root.find('AdvertisingContracts')
    if advertising_contracts is not None:
        for contract in advertising_contracts.findall('Contract'):
            contract_name = get_attribute(contract, 'name')
            scope = get_attribute(contract, 'scope', '')
            period = get_attribute(contract, 'contractPeriod', '')
            detail = f"- {contract_name}"
            if scope: detail += f" (범위: {scope})"
            if period: detail += f" (기간: {period})"
            add_paragraph(story, detail, s['CustomListItem'])
    add_spacer(story)

    # Projects
    add_paragraph(story, "주요 프로젝트", s['CustomHeading1'])
    projects = root.find('Projects')
    if projects is not None:
        def add_project(tag, prefix, *fields):
            for proj in projects.findall(tag):
                values = [f"{desc}{get_attribute(proj, attr)}" for desc, attr in fields]
                joined = ', '.join(values)
                add_paragraph(story, f"- {prefix}: {get_attribute(proj, 'name')} ({joined})", s['CustomListItem'])
        # TV (name, platform, status, date)
        add_project('TV', 'TV', 
            ("플랫폼: ", 'platform'), ("상태: ", 'status'), ("날짜: ", 'date')
        )
        # NETFLIX (name, status, date)
        add_project('NETFLIX', '넷플릭스', 
            ("상태: ", 'status'), ("날짜: ", 'date')
        )
    add_spacer(story)

    doc.build(story)
    print(f"PDF '{output_filename}' 이(가) 성공적으로 생성되었습니다.")

if __name__ == "__main__":
    sample_xml_data = """<ArtistProfile name="고윤정" source="R.book_03_7P" category="R.celeb">
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
        <!-- [2-4] 참고 -->
        <Contract name="하이엔드뷰티" scope="신규/글로벌"/>
        <Contract name="NH농협은행" scope="국내" contractPeriod="2024.04~/12개월"/>
        <Contract name="샤넬" scope="글로벌"/>
        <Contract name="려" scope="한국+대만+싱가폴+말레이시아+태국"/>
        <Contract name="마리떼"/>
        <Contract name="상쾌환"/>
        <Contract name="렌즈미"/>
        <Contract name="푸라닭"/>
        <Contract name="디스커버리"/>
        <Contract name="캐롯손해보험" scope="국내" contractPeriod="2023.07~/12개월"/>
        <Contract name="디디에두보" scope="한국+홍콩"/>
    </AdvertisingContracts>
    <Projects>
        <TV name="언젠가는 슬기로울 전공의 생활" platform="tvN" status="방영예정" date="04.12"/>
        <NETFLIX name="이 사랑 통역 되나요?" status="방영예정" date="2025"/>
    </Projects>
</ArtistProfile>"""
    generate_artist_profile_pdf(sample_xml_data)
