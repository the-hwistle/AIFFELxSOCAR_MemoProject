# AIFFELxSOCAR_MemoProject

- **해커톤 주제**: 정비 메모 분석 및 프로세스 자동화
- **프로젝트명**: 정비 메모를 활용한 자동완성 및 카테고리 분류 어플리케이션

<br>

## 프로젝트 요약

이 프로젝트는 모두의연구소 산하 교육기관 **AIFFEL**과 카셰어링 기업 **SOCAR**가 협력하여 진행한 해커톤에서 아이카센터 팀이 SOCAR로부터 제공받은 정비 메모 데이터를 활용하여 주어진 문제를 해결한 프로젝트입니다.

<br>

## 포스터
![해커톤3_최종발표_포스터_아이카센터](https://user-images.githubusercontent.com/59644774/146108530-a0be415b-d5dc-4ecf-bba0-b7557071b7df.png)
<br>

## 구성원 및 역할

* 최혜림  
  [![Tech Blog Badge](http://img.shields.io/badge/-Github-black?style=flat-square&logo=github&link=https://github.com/hyelimchoi1223)](https://github.com/hyelimchoi1223)  [![Blog Badge](http://img.shields.io/badge/-Blog-EF2D5E?style=flat-square&logo=GitHub%20Sponsors&logoColor=white&link=https://hyelimchoi1223.github.io/)](https://hyelimchoi1223.github.io/)
  
  
  - 팀장
  - MongoDB를 이용한 단어장 구성
  - API 개발 및 배포
      - 웹 크롤링 모듈 구현
      - 단어 자동완성 모듈 구현
          - 크롤링 + LRNounsStructure
  - Flask를 이용한 웹 개발 및 배포
  - GCP 웹 서버 및 API 서버 구성
  
* 윤세휘  
  [![Tech Blog Badge](http://img.shields.io/badge/-Github-black?style=flat-square&logo=github&link=https://github.com/Beatriz-Yun)](https://github.com/Beatriz-Yun)    [![Blog Badge](http://img.shields.io/badge/-Blog-EF2D5E?style=flat-square&logo=GitHub%20Sponsors&logoColor=white&link=https://beatriz-yun.github.io/)](https://beatriz-yun.github.io/)
  
  
  - 데이터 전처리
  - 명사추출
  - 카테고리 재정의
  - 카테고리 분류 모델
  - 데이터 불균형 해소 (마르코프 체인)
  - 웹 서버 기본 세팅
  
* 안형준  
  [![Tech Blog Badge](http://img.shields.io/badge/-Github-black?style=flat-square&logo=github&link=https://github.com/hjkornn-phys)](https://github.com/hjkornn-phys)     [![Blog Badge](http://img.shields.io/badge/-Blog-EF2D5E?style=flat-square&logo=GitHub%20Sponsors&logoColor=white&link=https://velog.io/@gibonki77)](https://velog.io/@gibonki77)
  
  
  - 카테고리 재정의 아이디어 및 구현
  - SPM으로 정비 용어 필터링 & 문장 분리
  - 요약된 문장 군집화 아이디어 및 구현
  - 신규 라벨 재정의
  - 카테고리 분류 모듈 구현
  
* 신관수  
  [![Tech Blog Badge](http://img.shields.io/badge/-Github-black?style=flat-square&logo=github&link=https://github.com/kwansu)](https://github.com/kwansu)
  
  
  - 데이터 전처리(문장 정제)
  - 단어 임베딩 후 유사도 테스트
  - 문장 토크나이저 개발 및 명사 추출
  - 키워드 사전 구축
  - 카테고리 분류 모델(Transformer, BERT) 구성
  
* 김영협  
  [![Tech Blog Badge](http://img.shields.io/badge/-Github-black?style=flat-square&logo=github&link=https://github.com/KimYoungHyeop)](https://github.com/KimYoungHyeop) [![Blog Badge](http://img.shields.io/badge/-Blog-EF2D5E?style=flat-square&logo=GitHub%20Sponsors&logoColor=white&link=https://blog.naver.com/kyh568)](https://blog.naver.com/kyh568)
  
  
  - 웹 개발 및 디자인 구성
  - 자동완성 기능 탐색
  - 카테고리 분류 모델(BERT) 구성


## Project milestone
![ppt_milestone](https://user-images.githubusercontent.com/15683086/145965057-f6164f19-3c15-4b42-820a-332d19ca1236.png)


## 사용한 기술 스택

- Python
- Pytorch, Tensorflow
- Goole Colab, Jupyter Notebook
- Google Cloud Platform
- Git
- Flask, Bootstrap 
- RestAPI, MongoDB


## 프로젝트 세부 동작

### 크롤링을 통한 Tokenizing and Extracting nouns
구글 크롤링을 통해 여러 단어가 조합된 조합어를 토큰화 및 명사 추출한다.


#### 1. 셀레니움 객체를 생성해서 크롤링된 문장등을 가져온다.
크롤링된 제목, 내용을 크롤링
```python
searcher = GoogleSearcher()
searcher.search('도어밸트끼임수리')

# (['안전벨트가 풀리지 않습니다. 어떻게 해야 하나요? DIY 안전 ...',
#   '11 okt. 2019 — 짧은 Phillips 드라이버를 사용하여 중간 도어 기둥의 바닥판에 있는 나사 4개를 풉니다. 그런 다음 덮개를 살짝 위로 살짝 당겨 제거합니다. 수리의 다음\xa0...',
#   '다양한 수리 솔루션! 관성 벨트 오작동의 주요 원인',
#   '29 sep. 2019 — 그러나 자가 수리 안전 벨트는 가계 예산에서 상당한 돈을 절약하는 데 도움이 될 것 ... 도어 필러 (중간)의 하단 트림에서 4 개의 볼트가 풀립니다.',
#   ....
#   "'도어 결함'기아 카니발 등 30개 차종 29만대 리콜 - 카가이",
#   '24 mei 2018 — ... 가 제작·판매한 카니발(YP) 22만4615대는 파워 슬라이딩 도어 내 끼임 방지 ... 해당차량은 24일부터 기아차 서비스센터에서 무상 수리를 받을 수\xa0...'],
#  '도어 벨트 끼임 수리')
```

하이트라이트로 강조되어 검색된 내용만 크롤링
```python
searcher.search('도어밸트끼임수리')

# ['도어', '수리', '수리', '벨트', '도어', '벨트', '도어', '끼임', '수리', '도어', '끼임', '수리', '도어', '벨트', '도어', '수리', '도어', '수리']
```

#### 2. 크롤링된 결과와 n-gram, 자모 유사도를 바탕으로 조합을 만든다.
```python
s = '정지에서출발할때떨림발생건'
searcher = GoogleSearcher()
create_continuous_likely_dict(searcher, s)

# 정지에서출발할때떨림발생건
# {0: [('정지', 6)],
#  2: [('에', 6), ('에서', 6)],
#  4: [('출발', 8)],
#  6: [('할', 4), ('할때', 1)],
#  7: [('때', 4)],
#  8: [('떨림', 5)],
#  10: [('발생건', 0)]}
```

#### 3. 실제 토큰화가 가능한 모든 조합을 생성한다.
```python
tokenize_all_case(searcher, '정지에서출발할때떨림발생건')

# [('정지', '에서', '출발', '할', '때', '떨림', '발생건'),
#  ('정지', '에서', '출발', '할때', '떨림', '발생건')]


extract_nouns(google_searcher, '거제시외버스터미널')

# [('거제', '시외', '버스', '터미널'),
#  ('거제', '시외', '버스터미널'),
#  ('거제', '시외버스', '터미널'),
#  ('거제', '시외버스터미널'),
#  ('거제시외버스터미널')]
```

#### 4. 동사,접속사,부사,조사,어미 등을 제거하여 명사만 추출한다.
```python
extract_nouns(searcher, '정지에서출발할때떨림발생건')

# 정지, 출발, 때, 발생건
```


### Category Extraction & Recategorization

![토큰화_과정](https://user-images.githubusercontent.com/59644774/146131448-15944e16-e5b1-47b2-a884-495b80134f9a.png)


#### 0. Preprocess & Separate Sentences

전처리 후 \[SEP] token을 사용하여 문장을 의미 단위로 분리한다.

#### 1.  Tokenize with SentencePiece 

전문용어를 잘 분절하는 SentencePiece를 사용한다.  Corpus에 의존적이므로 일반적인 한국어 Corpus와 다른 분포를 가져도 subword 분절이 잘 이루어진다. 

```python
# SentencePiece Model 학습
spm_train('preprocessed.txt', 'labeling', MAX_VOCAB_SIZE)
```

```python
sp_0 = spm.SentencePieceProcessor()
vocab_file = spm_path + '/labeling.model'
sp_0.load(vocab_file)
```

#### 2. Extract summarized sentences

```python
# 단일 스트링에 대한 결과
s = '신규 충전카드 비치하였고 배터리 오프[SEP] 점프 완료'
labeling(s)

# ['신규 충전카드 비치  배터리 오프', '점프 완료']
```

Tokenization 결과 점수가 높고, 두 글자 이상인 의미있는 token으로 문장을 요약한다.

```python
# DataFrame에 적용
data, cnt, label_list, label_set = label_and_count(data)
len(label_set)

# 9597개의 서로 다른 요약문을 얻었다
```

#### 3. Tokenize(split) & Detokenize(join) summarized results

띄어쓰기에 대해 강건하게 만들기 위해 웹 크롤링을 통해 띄어쓰기를 수행한다.

띄어쓰기 된 어절을 붙였을 때, 그 결과가 키워드 사전에 존재한다면, 두 어절을 붙인다.

이 과정은 군집화 성능을 높인다.

```python
data['tokenized_summary']= data['labeled'].apply(tokenize_sentences)
data

tokenize_sentences('주유카드 비치완료')
# ['주유 카드 비치완료']

data['tokenized_summary'] = data['tokenized_summary'].map(lambda x: detokenize_setences(x, nouns))

detokenize_setences(['현장 방문 오작동 발견', '네비게이션 정상 작동 확인'], nouns)
# ['현장방문 오작동 발견', '네비게이션 정상작동확인']

```

#### 4. Clustering

의미가 유사한 요약문을 묶어 재분류 카테고리로 사용할 수 있는 핵심 label을 추출하고,  출현 빈도를 기준으로 필터링한다. 핵심 label 중 의미가 너무 포괄적이거나 불필요한 경우는 핵심 label이 될 수 없도록 한다.

```python
# 과정 3을 거친 서로 다른 요약문의 개수
len(freq_tk)
# 8942

# 의미상 핵심 label이 될 수 있는 서로 다른 요약문의 개수
len(freq_tk_ls)
# 8231

new_category = {}
temp = dict(group_duplicated_word_tk(set(freq_tk_ls)))
[print(key,':',value) for key,  value in temp.items()]
for k, v in temp.items():
    if v:
        new_category[v[0][0]] = [x[0] for x in v]

# 합계 출현 횟수 20을 기준으로
# 핵심 label 885가지 중 238가지가 카테고리로 선택되었다.

# 신규 카테고리 출력
print(new_cateory.keys())
# dict.keys(['CSA', '전우 타이어교환', '메모리카드', '하이패스카드', '에어컨필터', ...])
```

![클러스터링_결과](https://user-images.githubusercontent.com/59644774/146131164-e7b30932-3423-424b-beaa-7086da75c2db.png)

#### 5. Recategorize with new category

신규 카테고리를 적용한다. 

`get_category`: 요약문이 신규 카테고리를 포함하면 해당 label을 적용한다.

`rm_duplicate_v2`:  중복되는 label을 제거한다.

```python
data['new_inspect_type'] = data['tokenized_summary'].apply(get_category)

data['new_inspect_type'] = data['new_inspect_type'].apply(rm_duplicate_v2)

get_category(['후 디스크교환'])
# [['디스크', '디스크교환']]

rm_duplicate_v2([['디스크', '디스크교환']])
# [['디스크교환']]
```

## 시연
![시연결과](https://user-images.githubusercontent.com/63278762/145804249-70e3d9af-3422-4c52-b452-f9fa5581f555.gif)

## 화면 캡쳐
<img width="1440" alt="스크린샷 2021-12-14 오후 12 04 21" src="https://user-images.githubusercontent.com/63278762/145925898-569f378f-b93c-4d85-883b-a16bb8cb4c6b.png">
<img width="1440" alt="스크린샷 2021-12-14 오후 12 04 15" src="https://user-images.githubusercontent.com/63278762/145925932-c6118b00-14e5-4a9d-931d-37c14a9db8a5.png">
<img width="1440" alt="스크린샷 2021-12-14 오후 12 04 48" src="https://user-images.githubusercontent.com/63278762/145925919-9811cf29-21b2-4502-a3ee-0b6a9d0bef98.png">
<img width="1440" alt="스크린샷 2021-12-14 오후 12 05 09" src="https://user-images.githubusercontent.com/63278762/145925922-3552184a-b37a-4b47-853f-bfab9159c526.png">
<img width="1440" alt="스크린샷 2021-12-14 오후 12 05 47" src="https://user-images.githubusercontent.com/63278762/145925927-19070398-e2f7-4c19-8d86-0f67aa04d0ba.png">

## Reference
* [LR-NounsExtrator](https://lovit.github.io/nlp/2018/04/09/three_tokenizers_soynlp/)
* [KR-WordRank](https://lovit.github.io/nlp/2018/04/16/krwordrank/)
* [Jaccard Similarity](https://wikidocs.net/24654)
* [자모 분리 및 결합](https://needjarvis.tistory.com/627)
* [한국어 단어 자동완성 시스템의 성능 분석 및 새로운 평가 방법](http://koreascience.kr/article/JAKO201525249160709.pdf)
