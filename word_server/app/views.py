import os
import pandas as pd
from collections import Counter
from django.core.files.storage import FileSystemStorage
from wordcloud import WordCloud
from django.conf import settings
from django.shortcuts import render

def upload_file(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']
        fs = FileSystemStorage()  # 파일 저장 처리
        file_path = fs.save(excel_file.name, excel_file)
        full_path = os.path.join(settings.MEDIA_ROOT, file_path)

        # 엑셀 읽기
        try:
            df = pd.read_excel(full_path)
            text_column = df.columns[0]
            text_data = ' '.join(df[text_column].dropna().astype(str).tolist())

            # 제외할 문자열 리스트
            exclude_words = [
                '문의', '문의드립니다.', '시험', '및', '관련 문의드립니다'
            ]

            # 제외할 문자열 제거
            for word in exclude_words:
                text_data = text_data.replace(word, '')

            # 한글 폰트 경로 설정
            font_path = "C:/Windows/Fonts/malgun.ttf"

            # 워드클라우드 생성
            wordcloud = WordCloud(
                font_path=font_path,
                width=800,
                height=400,
                background_color="white"
            ).generate(text_data)

            # 워드클라우드 이미지를 저장할 경로 (static 폴더 안에 저장)
            image_path = os.path.join(settings.BASE_DIR, 'app/static/wordcloud.png')
            wordcloud.to_file(image_path)

            # 단어 빈도수 계산
            word_freq = Counter(text_data.split())

            # DataFrame으로 변환
            word_freq_df = pd.DataFrame(word_freq.items(), columns=['Word', 'Frequency'])

            # 내림차순으로 정렬
            word_freq_df = word_freq_df.sort_values(by='Frequency', ascending=False)

            # CSV 파일 저장 (static 폴더에 저장)
            csv_path = os.path.join(settings.BASE_DIR, 'app/static/word_frequency.csv')
            word_freq_df.to_csv(csv_path, index=False)

            # HTML에 전달
            return render(request, 'upload.html', {
                'wordcloud_path': '/static/wordcloud.png',  # 워드클라우드 이미지 경로
                'csv_path': '/static/word_frequency.csv'  # CSV 파일 경로
            })
        except Exception as e:
            return render(request, 'upload.html', {'error': f'파일 처리 중 오류가 발생했습니다: {e}'})

    return render(request, 'upload.html')