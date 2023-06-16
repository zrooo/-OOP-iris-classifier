'''model_t.py와의 차이점
Hypereparameter 클래스를 class 키워드가 아닌 dataclass 데코레이터를 사용하여 클래스 생성'''

from __future__ import annotations
import collections
from dataclasses import dataclass, asdict
from typing import Optional, Counter, List
import weakref
import sys


@dataclass      #dataclass 데코레이터를 사용해 제공된 속성 타입 힌트로부터 클래스를 생성
class Sample:
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


#학습 데이터를 제공하고, 분류기를 테스트, 미지의 샘플을 분류 가능
@dataclass
class KnownSample(Sample):
    species: str


@dataclass
class TestingKnownSample(KnownSample):
    classification: Optional[str] = None


@dataclass
class TrainingKnownSample(KnownSample):
    pass


@dataclass
class UnknownSample(Sample):
    classification: Optional[str] = None


class Distance:
    def distance(self, s1: Sample, s2: Sample) -> float:
        raise NotImplementedError

# @dataclass 처리로 가장 큰 이점을 얻을 수 있는 클래스
@dataclass
class Hyperparameter:
    """k및 거리 계산 알고리즘이 있는 튜닝 매개변수 집합"""

    k: int
    algorithm: Distance
    data: weakref.ReferenceType["TrainingData"]  #아직 정의되지 않은 trainingdata 클래스에 대한 정방향 참조로서 문자열 사용

    def classify(self, sample: Sample) -> str:
        """k-NN 알고리즘  """
        if not (training_data := self.data()):
            raise RuntimeError("No TrainingData object")
        distances: list[tuple[float, TrainingKnownSample]] = sorted(
            (self.algorithm.distance(sample, known), known)
            for known in training_data.training
        )
        k_nearest = (known.species for d, known in distances[: self.k])
        frequency: Counter[str] = collections.Counter(k_nearest)
        best_fit, *others = frequency.most_common()
        species, votes = best_fit
        return species


@dataclass
class TrainingData:
    testing: List[TestingKnownSample]
    training: List[TrainingKnownSample]
    tuning: List[Hyperparameter]

