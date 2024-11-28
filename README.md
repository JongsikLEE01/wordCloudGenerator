# 1. 프로젝트 개요

### 목적

사용자의 Q&A를 모두 엑셀 파일에서 정리하고, 엑셀 파일에서 텍스트 데이터를 추출하여 단어 빈도수를 분석하고, 이를 시각화한 워드클라우드와 CSV로 제공
<br>

### 기능

- 엑셀 파일 업로드
- 텍스트 전처리(특정 단어 제거)
- 워드 클라우드 생성
- 단어 빈도수 CSV 다운로드

<br><br><br>

# 2. 주요 기능 및 흐름

### **A. 파일 업로드**
- 사용자로부터 엑셀 파일을 업로드
- 업로드된 파일은 Django의 **FileSystemStorage**로 서버에 저장
<br>

### **B. 데이터 처리**
- **텍스트 추출**: 엑셀 파일의 첫 번째 컬럼 데이터를 합쳐 하나의 문자열로 변환
- **전처리**: 불필요한 단어와 문구를 제거
- **빈도수 분석**: 단어별 등장 횟수를 계산
<br><br><br>

### **C. 결과물 생성**
1. **워드클라우드 이미지**
    - 단어 빈도수를 바탕으로 이미지 생성
    - `WordCloud` 라이브러리 사용
2. **CSV 파일**
    - 단어와 빈도수를 정리한 CSV 파일 제공
<br><br><br>

### **D. 사용자 피드백**
- 업로드된 엑셀 파일에서 처리된 결과를 HTML로 보여줌
- 결과물:
    - 워드클라우드 이미지
    - CSV 다운로드 링크
<br><br><br>

## 3. 주요 코드

### **3-1. 엑셀 파일에서 텍스트 추출 및 전처리**
사용자가 업로드한 엑셀 파일에서 텍스트 데이터를 읽고, 불필요한 단어(예: "문의", "안녕하세요")를 제거
<br>

**주요 코드**
```python
df = pd.read_excel(full_path)  # 업로드된 엑셀 파일 읽기
text_column = df.columns[0]  # 첫 번째 열 추출
text_data = ' '.join(df[text_column].dropna().astype(str).tolist())  # 데이터 병합

# 제외할 단어 리스트
exclude_words = ['문의', '안녕하세요', '시험', '관련', '드립니다']

# 텍스트 데이터에서 제외 단어 제거
for word in exclude_words:
    text_data = text_data.replace(word, '')
```
1. `pd.read_excel`: 업로드된 엑셀 파일을 데이터프레임으로 변환
2. `text_column`: 첫 번째 열의 데이터를 선택
3. 제외할 단어 리스트를 순환하며, 데이터를 정제

<br>

### 3-2. 워드클라우드 및 CSV 생성
- 정제된 데이터를 사용해 워드클라우드 이미지를 생성
- 단어 빈도수를 계산해 CSV 파일로 저장
<br>

**주요 코드**
```python
from collections import Counter

# 워드클라우드 생성
wordcloud = WordCloud(
    font_path="C:/Windows/Fonts/malgun.ttf",  # 한글 폰트 설정
    width=800,
    height=400,
    background_color="white"
).generate(text_data)

# 워드클라우드 이미지 저장
image_path = os.path.join(settings.STATICFILES_DIRS[0], 'wordcloud.png')
wordcloud.to_file(image_path)

# 단어 빈도수 계산
word_freq = Counter(text_data.split())

# DataFrame으로 변환 및 CSV 저장
word_freq_df = pd.DataFrame(word_freq.items(), columns=['Word', 'Frequency'])
word_freq_df = word_freq_df.sort_values(by='Frequency', ascending=False)  # 빈도수 기준 정렬
csv_path = os.path.join(settings.STATICFILES_DIRS[0], 'word_frequency.csv')
word_freq_df.to_csv(csv_path, index=False)
```
1. 워드클라우드 생성 `WordCloud` 객체를 생성하고 데이터를 시각화
2. 단어 빈도수 계산 `Counter`를 사용해 텍스트 데이터를 단어별로 집계
3. CSV 생성 ****단어 빈도 데이터를 `pandas` DataFrame으로 변환하고 저장
   
<br>

### 3-3. HTML 출력
- 워드클라우드 이미지 `/static/wordcloud.png`에 저장
- 단어 빈도 CSV 파일 `/static/word_frequency.csv`에 저장
<br>

**UI에서 워드클라우드와 CSV 제공**
```html
{% if wordcloud_path %}
    <h2>생성된 워드클라우드</h2>
    <img src="{{ wordcloud_path }}" alt="Word Cloud">
{% endif %}

{% if csv_path %}
    <h2>단어 빈도수 CSV 다운로드</h2>
    <a href="{{ csv_path }}" class="button" download>CSV 다운로드</a>
{% endif %}

```
엑셀 파일을 업로드해, 단어 분석 결과를 이미지와 CSV 형태로 얻을 수 있음

<br><br><br>

# 4. 실행 방법
### 라이브러리 설치
```bash
pip install django pandas wordcloud openpyxl
```
<br>

### 디렉토리 구조
```
word_server/
├── app/
│   ├── static/
│   │   ├── style.css
│   │   ├── wordcloud.png
│   │   ├── word_frequency.csv
│   ├── templates/
│   │   ├── upload.html
│   ├── views.py
│   ├── urls.py
├── media/
├── word_server/
│   ├── settings.py
│   ├── urls.py
├── manage.py
```
<br>

### 서버 실행
```bash
# 8000 포트에서 확인 가능
python manage.py runserver
```
<br><br><br>

# 5. 실행 화면
### HTML 화면
![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/78dc0e61-0667-415d-93d6-66223b91cf67/dfd8452d-6ee1-4b3e-bff8-6e4a0961c4cb/image.png)

<br>

### CSV 파일
```
Word,Frequency
이,53
제품의,53
알려주세요,53
대해,53
여부에,4
가능,4
정보에,2
지원,2
사용,2
공식,2
사용법에,2
구매,2
시간에,2
제품,2
소비량에,1
업데이트,1
유지보수,1
비용에,1
비교에,1
기타,1
액세서리에,1
타사,1
연락처,1
옵션에,1
수상,1
이력에,1
전력,1
후기에,1
FAQ,1
링크에,1
AS,1
행사에,1
특별,1
호환성에,1
색상에,1
구성품에,1
서비스,1
운영,1
도움이,1
되는,1
팁에,1
역사에,1
중고,1
성능에,1
주요,1
설명서에,1
반품,1
교환,1
거래,1
조에,1
수명에,1
언어에,1
쿠폰,1
평균,1
만족도에,1
고객,1
제조사에,1
환경,1
할인,1
친화성에,1
판매처에,1
장점에,1
대량,1
할인에,1
사양에,1
상세,1
웹사이트에,1
재질에,1
유명,1
사례에,1
배송,1
배송비에,1
원산지에,1
제조국에,1
이벤트,1
참여,1
방법에,1
재입고,1
일정에,1
디자인에,1
연령에,1
카테고리에,1
보증기간에,1
추천,1
이유에,1
사용자,1
수에,1
사이즈에,1
오프라인,1
가격에,1
가장,1
많이,1
묻는,1
질문에,1
```
