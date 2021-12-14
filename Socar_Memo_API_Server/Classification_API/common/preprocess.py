import re
import pandas as pd
import os
import sentencepiece as spm
import pickle


class Preprocessor:
    def __init__(self):
        with open(os.path.join(os.getcwd(), "data/tstation_center.txt"), "r") as f:
            centers = f.read()
        centers = centers.splitlines()
        self.centers = centers

        spm_model_path = os.path.join(os.getcwd(), "data/spm_txt/labeling.model")
        sp_0 = spm.SentencePieceProcessor()
        sp_0.load(spm_model_path)
        self.sp_0 = sp_0

        with open(
            os.path.join(os.getcwd(), "data/tokenization_dict.pickle"), "rb"
        ) as f:
            tokenization_dic = pickle.load(f)
        self.tokenizer_dic = tokenization_dic

        with open(os.path.join(os.getcwd(), "data/labels/labels_21179.txt"), "r") as f:
            labels = f.read().split("\n")
        self.labels = labels

        nouns = set()
        for tokens_list in tokenization_dic.values():
            for tokens in tokens_list:
                if len(tokens) > 1:
                    nouns.update(tokens)
        self.nouns = nouns
        print(f"Nouns:{len(self.nouns)}")

    def parentheses(self, s):
        if s.count("(") == s.count(")"):
            return s

        if s.count("(") > s.count(")"):
            s += ")"
        else:
            for match in re.finditer("\)", s):
                end = match.end() - 1
                if s[:end].count("(") <= s[:end].count(")"):
                    s = s[:end] + " " + s[end + 1 :]

        return s

    def replace_entity_to_keyword(
        self, s
    ):  # dict는 defuatdict같이 초기값이 set으로 설정된 사전이라고 가정
        s = re.sub(r"ㄴ", "\nㄴ", s)

        s = s.upper()
        s = re.sub(r"[\[\]\?]", "", s)
        s = re.sub(r"\)-", ") -", s)

        # 자동차 이름에 대한 전처리를 하려면 자동차이름(영어가 안썩인) 데이터가 필요할 것 같다.
        s = re.sub("(코나)|(아반떼)|(화성점)|(넥센+[가-힣])", "", s)

        s = re.sub(r"좌/우", "좌우", s)

        center_name = r"(^|(?<=\s))\(주\)\w+|\w+\(주\)($|(?=\s))"  # 앞,뒤로 (주)가 붙은 단어
        s = re.sub(center_name, "", s)

        center_name = "|".join(self.centers)  # 크롤링한 정비소 이름들
        s = re.sub(center_name, "", s)

        brand_name = r"(티스테이션)|(현대블루핸즈)|(기아오토큐)|(애니카랜드)|(스피드메이트)|(하이카)|(하이카서비스)|(T스테이션)|(블루핸즈)"  # 브랜드 정비소
        s = re.sub(brand_name, "", s)

        motors_name = r"[가-힣a-zA-Z0-9]+모터스"  # ~~ 모터스
        s = re.sub(motors_name, "", s)

        ts_name = r"(\b|(?<=[^a-zA-Z]))[tT]{1,2}[sS](?![a-zA-Z])"  # TS, 단 STS제외
        s = re.sub(ts_name, "", s)

        sm_name = r"(\b|(?<=[^a-zA-Z]))[sS]\/?[mM](?![a-zA-Z])"  # s/m
        s = re.sub(sm_name, "", s)

        branch_name = r"[가-힣a-zA-Z0-9]+(?<!백화|.접|.0)점(?!\w)"  # ~~점, 단 0점 접점 제외
        s = re.sub(branch_name, "", s)

        address_number = r"\d{5,6}[ ]*-[ ]*\d{3,5}[ ]*-[ ]*\d{3, 5}(?!\d)"  # 등기번호
        s = re.sub(address_number, "", s)

        phone_number = r"(?<!\d)\d{2,3}[ ]*-[ ]*\d{3,4}[ ]*-[ ]*\d{4}(?!\d)"  # 전화번호
        s = re.sub(phone_number, "", s)

        # tire_part = r'(?<!\d)[A-Z]?\d{3}[ \*\t\.\/\,\-]+\d{2,3}[ A-Z\*\t\.\/\,\-]+\d+[ A-Z\*\t\/\,\-]*\d*[A-Z\,]{0,2}\d*[A-Z\,]{0,2}\d*' # 타이어 규격
        # s = re.sub(tire_part, '',s)
        s = re.sub(r"규격", "", s)
        s = re.sub(r"되지", "", s)
        # s = re.sub(r'IQ', '',s)
        # s = re.sub(r'현대자동차', '',s)

        date = r"(?<!\d)(\d{4}|\d{2})[ \/\.\-]+\d{1,2}[ \/\.\-]+\d{1,2}(?!\d)"  # 날짜
        s = re.sub(date, "", s)

        date = r"(?<!\d)\d{1,2}[ \/]+\d{1,2}(?!\d)"  # 날짜
        s = re.sub(date, "", s)

        pattern = r"(이동서울정비)|(대성정비)|(동광정비)|(원스탑)|(종합정비)|(자동차종합정비)|(르노삼성자동차)|(기아시흥)|(비원카센타)|(가온오토)|(진주)|(무빙카서비스)|(원진엠엔에스)|(공업사)|(쉐보레)|(으로)|(벤츠)|(카랑)|(애니카)|(미쉐린)|(RH)"
        s = re.sub(pattern, "", s)

        distance_driven = (
            r"\d+\,?\d*(만|천|백|십)?[ \t]*[kK][mM](?![a-zA-Z])"  # 거리, todo: 속도가 들어올 경우
        )
        s = re.sub(distance_driven, "", s)

        url = r"HTTP\S+"
        s = re.sub(url, "", s)

        loc = r"(화성)|(남양주)|(금천)|(순천)|(창원)|(금호)|(당진)|(울산)|(고양)"
        s = re.sub(loc, "", s)

        service = r"[가-힣a-zA-Z0-9]+(서비스센터 |서비스센터$|서비스센터\n|서비스센터->|서비스센터-)"
        s = re.sub(service, "", s)

        service = r"[가-힣a-zA-Z0-9]*(?<!알림)(서비스)"
        s = re.sub(service, "", s)

        service = r"서비스센터"
        s = re.sub(service, "", s)

        result_x = r"(?<![a-zA-Z])X(?![0-9a-zA-Z])"
        s = re.sub(url, "[result_x]", s)

        car_id = r"\d+[ \t]*[가-힣][ \t]*\d+"  # 자동차 id, todo: 실제 자동차번호판 규칙을 안다면 \d{2,3}[가-힣]\d{4}이런식으로 작성
        s = re.sub(car_id, "", s)

        liter = r"\d*\.?\d+[lL](?![a-zA-Z])"  # 용량 6l, 1.8L 등.
        s = re.sub(liter, "", s)

        s = re.sub(
            r"(\s*[^가-힝A-Z\)\]]*\s*$)|(^\s*[^가-힝A-Z\[\(]*\s*)", "", s
        )  # 양 끝 특수 문자 제거
        s = re.sub(r'(?<!^)".*"(?!&)', "[text]", s)  # "지우는 중..." 같은 설명 문장 삭제
        s = re.sub(
            r"(\s*\n[\*ㅁ\#])|(\s*\n[0-9]+\.)", " [SEP]", s
        )  # 새로운 문단[new_sub] 이라고 할 수 있지만, 너무 개수가 적다.
        s = re.sub(r"(?<=\w)\s*\.\s+", "[SEP]", s)  # 일반적인 마침표.
        s = re.sub(
            r"\s*\nㄴ", " [SEP]", s
        )  # 줄내림이라고 할 수도 있지만, 이런 문장은 앞 문장에 종속적이나거나 추가 정보이다.
        s = re.sub(r"후에도", "[SEP]", s)
        # todo: 시간(11월, 30분), 개수(2EA, 4개), 가격 등의 키워드화(필요한가?)
        s = re.sub(r"\d*\,?\.?\d+", "", s)

        # 영단어 처리 방법
        # 1. 각 (a/s, a.s, as), (r-cam, r cam) 등을 하나씩 다 찾아서 고유명사로 통일한다.
        # 2. 일단 whitespace+특수문자 구분으로 각 단어 (a)(s)(r)(cam)을 토큰화 시키고 n-gram을 통해 고유명사를 찾는다.
        # 3. 모든 영어를 제거하거나, [en]으로 단일 키워드화 시키고 신경쓰지 않는다.
        # todo: 임시 조치(토큰나이저 사용시 고유명사로 등록, 토큰화 X)
        # s = re.sub(r'(^|[^a-zA-Z])[aA][ \t]?(필러|필라)', '[A필러]', s)
        # s = re.sub(r'[aA]\.?\/?[sS]', '[as]', s)
        # s = re.sub(r'(?<=[a-zA-Z])[\.\/]+(?=[a-zA-Z])', '/', s)
        # en_token = r'(?<!(\[|[a-zA-Z]))[a-zA-Z]+(?!(\w*\]))'
        # s = extract_and_replace(s, en_token, 'en_token', keyword_dict)

        # 나머지 특수문자와 줄내림 등 처리
        s = self.parentheses(s)
        # s = re.sub(r'\.', ' ', s)
        s = re.sub(r"[\=\-]*\>", " > ", s)
        s = re.sub(r"\=", " ", s)
        s = re.sub(r"[\!\"\%\※\.]", " ", s)
        s = re.sub(r"(?<![a-z])_", " ", s)
        s = re.sub(r"\#", " [SEP]", s)
        s = re.sub(r"[ㄱ-ㅎ]", "", s)  # todo: 오타를 먼저 처리하고 해야한다.(올바른 단어를 찾는 정보이다.)
        s = re.sub(r"\(\s*\)", "", s)
        s = re.sub(r"\s+\Z", "", s)
        s = re.sub(r"\n+\s*", " [SEP]", s)  # 줄내림
        s = re.sub(r"[\,\/]\s*(?=(\[line\_))", " ", s)
        s = re.sub(r"A/S", "AS", s)
        s = re.sub(r"A./S", "AS", s)
        s = re.sub(r"/VFS", "VFS", s)
        s = re.sub(r"/", "[SEP]", s)
        s = re.sub(r",", "[SEP]", s)
        s = re.sub(r"&", "[SEP]", s)

        # [SEP]
        pattern = r"(해도)|(인하여)|(하여)|(인해)|(:)|(및)"
        s = re.sub(pattern, "[SEP]", s)

        pattern_3 = r"교환(?!\w)"
        s = re.sub(pattern_3, "교환 [SEP]", s)

        pattern_4 = r"(했습니다)|(합니다)|(드립니다)|(니다)|(하였습)"
        s = re.sub(pattern_4, "[SEP]", s)

        s = re.sub(r"(않|없|있)[가-힣]+", "[SEP]", s)

        s = re.sub("부탁드립니다", "요청", s)
        s = re.sub("않습니다", "불가", s)
        s = re.sub("됩니다", "가능", s)
        s = re.sub(r"탁송회", "탁송", s)
        s = re.sub(r"교체", "교환", s)
        s = re.sub(r"EA", "", s)
        s = re.sub(r"초기화후", "초기화 후", s)

        # 모든 처리가 끝났다면
        s = s = re.sub(r"\s+", " ", s)
        return s

    def delete_lesion_id_to_description(self, row):
        row["description"] = re.sub(str(row["lesion_id"]), " ", row["description"])
        return row

    def delete_unnecessary_words(self, s):
        s = re.sub(r"장애[ \t]*(카드)?번호[0-9ㄱ-ㅎ가-힣]*[ \n\t:]*", " ", s)
        s = re.sub(r"장애[ \t]*:", " ", s)
        s = re.sub(r"법인[ \t]*카드[ \t]*(결제건|사용)", " ", s)
        s = re.sub(r"\(신규\)", " ", s)
        s = re.sub(r"└.*", "", s)
        s = re.sub(r"㈜", "", s)
        s = re.sub(r"×자로", "", s)
        s = re.sub(r"구\)삼성.{0,4}카드", "주유카드", s)
        s = re.sub(r"\(?주\)스피드총판", "스피드총판", s)
        s = re.sub(r"가온오토\)", "가온오토", s)
        s = re.sub(r"미션오일보충\)", "미션오일보충", s)
        s = re.sub(r"\s[a-zA-Z]\d+\.", " ", s)
        s = re.sub(r"([ \t\:\dA-Z]+[가-힣]?\~[ \t]*(?=\d))|(\~[ \t]*(?!\d))", " ", s)
        s = re.sub(r"\([^\(]*\\.*\)", "", s)
        s = re.sub(r"\+", " + ", s)
        s = re.sub(r"\.\,", ",", s)
        s = re.sub(r"[－ㅡ]+\-?", "-", s)
        s = re.sub(r"프라자", "", s)
        s = re.sub(r"인한", " ", s)
        s = re.sub(r"되어", " ", s)
        s = re.sub(
            r"(모닝)|(올리브영)|(쏘나타뉴라이즈)|(투싼)|(소나타)|(밀양역)|(올뉴 밀양역옆)|(에서)|(차랑)|(의당)|(vip)",
            " ",
            s,
        )
        return s

    def labeling(self, memo):
        morph_descriptions = []
        memo.replace("_", " ").replace("-", " ").replace("ㄴ", " ").replace(
            "#", " "
        ).replace("=", " ").replace(")", " ) ").replace("(", " ( ")
        sp_id = self.sp_0.encode_as_ids(
            memo
        )  # [43, 123, 4 ,435, 369, 23, 44, 55,4000,3500, 3  4 ,1242]
        for idx, token_id in enumerate(sp_id):
            if not idx:
                cut = []
                count = 0
            if token_id == 4 or idx == len(sp_id) - 1:

                if token_id != 4:
                    cut.append(token_id)
                temp_1 = sorted(cut)[:8]
                long_cut = [x for x in cut if x in temp_1]
                long_out = self.sp_0.id_to_piece(long_cut)
                long_out = [
                    i
                    for i in long_out
                    if not len(i) == 1 or i in ["휠", "액", "등"]
                    if not (len(i) == 2 and i[0] == "▁") or i in ["▁휠"]
                ]
                long_cand = " ".join(
                    [token.replace("▁", "").replace("하였", "") for token in long_out]
                )

                if long_cand:
                    morph_descriptions.append(long_cand)  # SentencePiece feature

                cut = []
                count += 1

            else:
                cut.append(token_id)
        if not morph_descriptions:
            return None
        return morph_descriptions

    def run_preprocess(self, s: str):
        s = self.delete_unnecessary_words(s)
        s = self.replace_entity_to_keyword(s)
        s = self.labeling(s)
        print(s)
        return s
