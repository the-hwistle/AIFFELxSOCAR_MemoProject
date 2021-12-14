# from konlpy.tag import Komoran, Okt
# import tensorflow as tf
import re

mapping_table = {
    "내비게이션": "네비게이션",
    "내비": "네비게이션",
    "네비": "네비게이션",
    "딜리버리": "탁송",
    "탁송비": "탁송",
    "브레이크 오일": "브레이크액",
    "브레이크오일": "브레이크액",
    "라디오": "오디오",
    "agm60": "배터리",
    "agm": "배터리",
    "a/s": "as",
    "얼라이먼트": "차량쏠림",
    "225 55 17": "타이어",
    "전조등": "라이트",
    "데이라이트": "라이트",
    "헤드라이트": "라이트",
    "깜빡이": "라이트",
    "주간": "라이트",
    "백미러": "라이트",
    "DRL": "라이트",
}


def change_tire_word(text):
    # 175/65R14, 04, H724
    try:
        text = re.sub(
            r"([0-9]{3}[/][0-9]{2}R[0-9]{2}[A-Z0-9]*, *[0-9]{2}, *[A-Z0-9]{4})",
            r" 타이어 ",
            text,
        )
    except:
        pass
    return text


def check_vocab(text):
    for word in mapping_table.keys():
        if word in text:
            text = text.replace(word, mapping_table[word])
    return text


def delete_url(text):
    try:
        text = re.sub(
            r"(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*))",
            r" ",
            text,
        )
    except:
        pass
    return text


def preprocessing(sentence):
    # 타이어 기종을 타이어로 변경
    sentence = change_tire_word(sentence)
    # url 형태 삭제
    sentence = delete_url(sentence)
    # 소문자 변환
    sentence = str(sentence).lower()
    # 비슷한 단어 사전 체크 후 변경
    sentence = check_vocab(sentence)
    # 6자리 숫자 삭제 -> 정비 아이디
    sentence = re.sub(r"([0-9]){6}", r" ", sentence)
    # 금액 표현 00,000 삭제
    sentence = re.sub(r"([0-9]{2},[0-9]{3})", r" ", sentence)
    # 불필요한 글자 삭제
    sentence = re.sub(r'[\n#.,\(\)&\-ㄴ\_"/>└]', r" ", sentence)
    # 긴 공백 제거
    sentence = re.sub(r"[ ]{2,}", r" ", sentence)

    return sentence


def parentheses(s):
    if s.count('(') == s.count(')'):
        return s

    if s.count('(') > s.count(')'):
        s += ')'
    else:
        for match in re.finditer('\)', s):
            end = match.end() - 1
            if s[:end].count('(') <= s[:end].count(')'):
                s = s[:end] + ' ' + s[end+1:]

    return s


def extract_and_replace(s, pattern, repl=' ', keyword_dict=None):
    if keyword_dict:
        for match in re.finditer(pattern, s):
            # get함수를 이용하는 할 수 있지만, 매번 set()을 만드는 오버헤드 발생
            keyword_dict[repl].add(match.group())
    return re.sub(pattern, repl, s)


def replace_entity_to_keyword(s, keyword_dict):
    '''
    keyword_dict : 사용하려면 defaultdict로 생성된 사전이여야한다.
    '''
    s = s.upper()
    s = re.sub(r'[\[\]\?]', '', s)

    s = re.sub(r'\)-', ') -', s)

    # 자동차 이름에 대한 전처리를 하려면 자동차이름(영어가 안썩인) 데이터가 필요할 것 같다.
    car_name = r'(모닝)|(쏘나타뉴라이즈)|(투싼)|(소나타)|(코나)|(아반떼)|(쉐보레)|(벤츠)'
    s = extract_and_replace(s, car_name, 'c', keyword_dict=keyword_dict)

    s = re.sub(r'좌/우', '좌우', s)

    center_name = r'(^|(?<=\s))\(주\)\w+|\w+\(주\)($|(?=\s))'  # 앞,뒤로 (주)가 붙은 단어
    s = extract_and_replace(s, center_name, 'b', keyword_dict=keyword_dict)

    #center_name = '|'.join(centers)  # 크롤링한 정비소 이름들
    #s = extract_and_replace(s, center_name, 'b', keyword_dict=keyword_dict)

    # 브랜드 정비소
    brand_name = r'(이동서울정비)|(대성정비)|(동광정비)|(원스탑)|(대성종합정비)|(종합정비)|(자동차종합정비)|(르노삼성자동차)|(기아시흥)|(비원카센타)|(가온오토)|(진주)|(무빙카서비스)|(원진엠엔에스)|(공업사)|(카랑)|(애니카)|(화성점)'
    s = extract_and_replace(s, brand_name, 'b', keyword_dict=keyword_dict)

    brand_name = r"(티스테이션)|(현대블루핸즈)|(기아오토큐)|(애니카랜드)|(스피드메이트)|(하이카)|(하이카서비스)|(T스테이션)|(블루핸즈)|(아우토랩)"
    s = extract_and_replace(s, brand_name, 'b', keyword_dict=keyword_dict)

    motors_name = r"[가-힣a-zA-Z0-9]+모터스"  # ~~ 모터스
    s = extract_and_replace(s, motors_name, 'b', keyword_dict=keyword_dict)

    ts_name = r"(\b|(?<=[^a-zA-Z]))[tT]{1,2}[sS](?![a-zA-Z])"  # TS, 단 STS제외
    s = extract_and_replace(s, ts_name, 'b', keyword_dict=keyword_dict)

    sm_name = r"(\b|(?<=[^a-zA-Z]))[sS]\/?[mM](?![a-zA-Z])"  # s/m
    s = extract_and_replace(s, sm_name, 'b', keyword_dict=keyword_dict)

    service = r'[가-힣a-zA-Z0-9]*서비스센터'
    s = extract_and_replace(s, service, 'b', keyword_dict=keyword_dict)

    service = r'[가-힣a-zA-Z0-9]*(?<!알림)(서비스)'
    s = extract_and_replace(s, service, 'b', keyword_dict=keyword_dict)

    branch_name = r"[가-힣a-zA-Z0-9]+(?<!백화|.접|.0)점(?!\w)"  # ~~점, 단 0점 접점 제외
    s = extract_and_replace(s, ts_name, 'b', keyword_dict=keyword_dict)

    address_number = r'\d{5,6}[ ]*-[ ]*\d{3,5}[ ]*-[ ]*\d{3, 5}(?!\d)'  # 등기번호
    s = re.sub(address_number, ' ', s)

    # 전화번호
    phone_number = r'(?<!\d)\d{2,3}[ ]*-[ ]*\d{3,4}[ ]*-[ ]*\d{4}(?!\d)'
    s = re.sub(phone_number, ' ', s)

    # 타이어 규격
    tier_part = r'(?<!\d)[A-Z]?\d{3}[ \*\t\.\/\,\-]+\d{2,3}[ A-Z\*\t\.\/\,\-]+\d+[ A-Z\*\t\/\,\-]*\d*[A-Z\,]{0,2}\d*[A-Z\,]{0,2}\d*'
    s = extract_and_replace(s, tier_part, 't', keyword_dict)

    # 날짜
    date = r'(?<!\d)(\d{4}|\d{2})[ \/\.\-]+\d{1,2}[ \/\.\-]+\d{1,2}(?!\d)'
    s = re.sub(date, ' ', s)

    date = r'(?<!\d)\d{1,2}[ \/]+\d{1,2}(?!\d)'  # 날짜
    s = re.sub(date, ' ', s)

    # 거리, todo: 속도가 들어올 경우
    distance_driven = r'\d+\,?\d*(만|천|백|십)?[ \t]*[kK][mM](?![a-zA-Z])'
    s = re.sub(distance_driven, 'd', s)

    url = r'HTTP\S+'
    s = re.sub(url, ' ', s)

    loc = r'(화성)|(남양주)|(금천)|(순천)|(창원)|(금호)|(당진)|(울산)|(고양)'
    s = re.sub(loc, 'l', s)

    # result_x = r'(?<![a-zA-Z])X(?![0-9a-zA-Z])'
    # s = re.sub(result_x, '[result_x]', s)

    add_info = r'(?<=(tierpart))[ \t]?[A-Z]+\-?\d+\-?[A-Z]*'
    s = re.sub(add_info, ' ', s)

    # 자동차 id, todo: 실제 자동차번호판 규칙을 안다면 \d{2,3}[가-힣]\d{4}이런식으로 작성
    car_id = r'\d+[ \t]*[가-힣][ \t]*\d+'
    s = re.sub(car_id, ' ', s)

    liter = r'\d*\.?\d+[lL](?![a-zA-Z])'  # 용량 6l, 1.8L 등.
    s = re.sub(liter, ' ', s)

    # 양 끝 특수 문자 제거
    s = re.sub(r'(\s*[^가-힝a-zA-Z\)\]]*\s*$)|(^\s*[^가-힝a-zA-Z\[\(]*\s*)', '', s)
    s = re.sub(r'(?<!^)".*"(?!&)', 'text', s)  # "지우는 중..." 같은 설명 문장 삭제
    # 새로운 문단[new_sub] 이라고 할 수 있지만, 너무 개수가 적다.
    s = re.sub(r'(\s*\n[\*ㅁ\#])|(\s*\n[0-9]+\.)', '\n', s)
    s = re.sub(r'(?<=\w)\s*\.\s+', '\n', s)  # 일반적인 마침표.
    # 줄내림이라고 할 수도 있지만, 이런 문장은 앞 문장에 종속적이나거나 추가 정보이다.
    s = re.sub(r'\s*\nㄴ', '\n', s)

    # todo: 시간(11월, 30분), 개수(2EA, 4개), 가격 등의 키워드화(필요한가?)
    s = re.sub(r'\d*\,?\.?\d+', '', s)

    # 나머지 특수문자와 줄내림 등 처리
    s = parentheses(s)
    #s = re.sub(r'\.', ' ', s)
    s = re.sub(r'[\=\-]*\>', ' > ', s)
    s = re.sub(r'\=', ' ', s)
    s = re.sub(r'[\!\"\%\※\.]', ' ', s)
    #s = re.sub(r'(?<![a-z])_', ' ', s)
    s = re.sub(r'\#', '\n', s)
    s = re.sub(r'[ㄱ-ㅎ]', '', s) # todo: 오타를 먼저 처리하고 해야한다.(올바른 단어를 찾는 정보이다.)
    s = re.sub(r'\(\s*\)', '', s)
    s = re.sub(r'\s+\Z', '', s)
    s = re.sub(r'\n+\s*', '\n', s) # 줄내림
    s = re.sub(r'[\,\/]\s*(?=(\[line\_))', ' ', s)
    s = re.sub(r'A/S', 'AS', s)
    s = re.sub(r'A./S', 'AS', s)
    s = re.sub(r'/VFS', 'VFS', s)
    s = re.sub(r'교체', '교환', s)    

    # 모든 처리가 끝났다면
    s = s = re.sub(r'\s+', ' ', s)
    return s


def delete_unnecessary_words(s):
    s = re.sub(r'장애[ \t]*(카드)?번호[0-9ㄱ-ㅎ가-힣]*[ \n\t:]*', ' ', s)
    s = re.sub(r'장애[ \t]*:', ' ', s)
    s = re.sub(r'법인[ \t]*카드[ \t]*(결제건|사용)', ' ', s)
    s = re.sub(r'\(신규\)', ' ', s)
    s = re.sub(r'└.*', '', s)
    s = re.sub(r'㈜', '', s)
    s = re.sub(r'×자로', '', s)
    s = re.sub(r'구\)삼성.{0,4}카드', '주유카드', s)
    s = re.sub(r'\(?주\)스피드총판', '스피드총판', s)
    s = re.sub(r'가온오토\)', '가온오토', s)
    s = re.sub(r'미션오일보충\)', '미션오일보충', s)
    s = re.sub(r'\s[a-zA-Z]\d+\.', ' ', s)
    s = re.sub(r'([ \t\:\dA-Z]+[가-힣]?\~[ \t]*(?=\d))|(\~[ \t]*(?!\d))', ' ', s)
    s = re.sub(r'\([^\(]*\\.*\)', '', s)
    s = re.sub(r'\+', ' + ', s)
    s = re.sub(r'\.\,', ',', s)
    s = re.sub(r'[－ㅡ]+\-?', '-', s)
    s = re.sub(r'프라자', '', s)
    s = re.sub(r'(올리브영)|(밀양역)|(올뉴 밀양역옆)|(차랑)|(의당)|(vip)', ' ', s)
    return s


def preprocess_sentence(s):
    s = delete_unnecessary_words(s)
    s = replace_entity_to_keyword(s, None)
    return s


# def to_okt_token(sentence: str):
#     okt = Okt()

#     if sentence is None:
#         return ""
#     sentence = preprocessing(sentence)
#     morph_out = []
#     try:
#         morph_out = okt.morphs(sentence)
#     except:
#         morph_out = []
#     return morph_out


# def get_tf_pad_sequences(data: list, max_len=100):
#     return tf.keras.preprocessing.sequence.pad_sequences(data, maxlen=max_len)
