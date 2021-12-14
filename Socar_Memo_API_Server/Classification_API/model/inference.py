import re
import numpy as np
import pandas as pd
import tensorflow as tf
from tqdm import tqdm
from Classification_API.model import transformer
import pickle
import os


class Inferencer:
    def __init__(self, max_len=8):
        with open(
            os.path.join(os.getcwd(), "data/Inference/word_to_num.pkl"),
            "rb",
        ) as f:
            word_to_num = pickle.load(f)
        self.word_to_num = word_to_num

        with open(
            os.path.join(os.getcwd(), "data/Inference/num_to_word.pkl"),
            "rb",
        ) as f:
            num_to_word = pickle.load(f)
        self.num_to_word = num_to_word

        with open(
            os.path.join(os.getcwd(), "data/Inference/label_to_num.pkl"),
            "rb",
        ) as f:
            label_to_num = pickle.load(f)
        self.label_to_num = label_to_num

        with open(
            os.path.join(os.getcwd(), "data/Inference/num_to_label.pkl"),
            "rb",
        ) as f:
            num_to_label = pickle.load(f)
        self.num_to_label = num_to_label

        self.MAX_LEN = max_len

        # 하이퍼파라미터
        NUM_LAYERS = 2  # 인코더와 디코더의 층의 개수
        D_MODEL = 256  # 인코더와 디코더 내부의 입, 출력의 고정 차원
        NUM_HEADS = 8  # 멀티 헤드 어텐션에서의 헤드 수
        UNITS = 512  # 피드 포워드 신경망의 은닉층의 크기
        DROPOUT = 0.1  # 드롭아웃의 비율

        tf.keras.backend.clear_session()

        model = transformer.transformer(
            encoder_vocab_size=len(self.num_to_word),
            decoder_vocab_size=len(self.num_to_label),
            num_layers=NUM_LAYERS,
            units=UNITS,
            d_model=D_MODEL,
            num_heads=NUM_HEADS,
            dropout=DROPOUT,
        )
        model.load_weights(os.path.join(os.getcwd(), "data/models/weights"))
        model.summary()

        self.model = model

    def tokenize(self, sentences):
        tokenized_sentence = [
            [self.word_to_num[x] for x in s.split()] for s in sentences
        ]
        inputs = tf.keras.preprocessing.sequence.pad_sequences(
            tokenized_sentence,
            maxlen=self.MAX_LEN,
            padding="pre",
            value=self.word_to_num["<PAD>"],
        )
        print(inputs)
        return inputs

    def predict(self, sentences):
        eos = self.label_to_num["<EOS>"]
        # sentence = preprocess_sentence(sentence)
        sentences = self.tokenize(sentences)
        final_result = []
        for sentence in sentences:
            sentence = tf.expand_dims(sentence, axis=0)
            output_sequence = tf.expand_dims([self.label_to_num["<BOS>"]], 0)
            result = []

            for _ in range(8):
                pred = self.model.predict([sentence, output_sequence])
                pred_num = np.argmax((tf.nn.softmax(pred[:, -1, :])))
                if pred_num == eos:
                    break

                output_sequence = tf.concat(
                    [output_sequence, tf.constant([[pred_num]])], axis=-1
                )
                result.append(pred_num)
            result = [self.num_to_label[x] for x in result]
            final_result.append(result)
        return final_result
