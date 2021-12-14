# Socar_Memo_API_Server
쏘카 메모팀  API 서버

## 가상환경 설정
```bash
python3 -m venv venv
```
## 가상환경 시작
```bash
source ./venv/bin/activate 
```

## 가상환경 종료
```bash
deactivate
```

> ## 필요한 패키지 없을 경우
> ```bash
> pip install -r requirements.txt
> ```

## 서버 실행
```bash
python3 api.py
```

****

# Search API 사용법

```python
import requests
import json

res  = requests.get("[GCP URL]/vocab/search?word=쏘나타")
# 쏘나타에 원하는 단어 입력
# 단, 단어 사전에 없으면 서칭해야할 단어로 옮겨짐
dict_test = json.loads(res.content.decode('unicode-escape'))
dict_test
# result:
# [{'neighbors': [{'node': '현대자동차', 'weight': 0}], 'node': '쏘나타'}]
```

* node : 중심단어
* neighbors : 중심단어와 가까운 단어들 목록
  * weight : 단어에 부여하는 가중치
  
**결과가 dictionary로 나옴**

# Crawling API 사용법
## 구글
```python
import requests
import json
import re

res  = requests.get("[GCP URL]/crawling/google?p=요소수")
data = res.content.decode('unicode-escape')
result = []
# 이 과정을 통해 str list로 만듦
for text in data.split("\","):
  text = re.sub(r"([\"\[\]])", r" ", text)
  result.append(text.strip())
```

## 네이버

```python
import requests
import json
import re

res  = requests.get("[GCP URL]/crawling/naver?p=요소수")
data = res.content.decode('unicode-escape')
result = []
# 이 과정을 통해 str list로 만듦
for text in data.split("\","):
  text = re.sub(r"([\"\[\]])", r" ", text)
  result.append(text.strip())
```

**결과가 문자열로 나옴**

# Classify API 사용법

```python
import requests
import json

res  = requests.get("[GCP URL]/classify?desc=내용")

result_list = json.loads(res.content.decode('unicode-escape'))
result_list
# result:
# [[ "포켓파이 교환", "교환후 정상"],,["점검"]]
```

**결과가 문자열로 나옴**
