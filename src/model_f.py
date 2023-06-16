#Hyperparameter 클래스에 frozen 속성을 추가

from __future__ import annotations
import collections
from dataclasses import dataclass, asdict
from typing import Optional, List, Counter
import weakref
import sys

"""데이터클래스의 일반적인 용도는 가변 객체 생성
   속성에 새로운 값을 할당해 객체의 상태를 변경"""

# <frozen>스테레오타입 추가 -> 객체를 불변으로 만드는 구현을 상기시키는 데 도움
@dataclass(frozen=True)
class Sample:
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

''' 클래스 내부에는 고정된 KnownSample 객체 존재, 
knownsample 객체를 포함하는 trainingknownsample 인스턴스의 중첩된 구성은 명시적 -> 불변의 knownsample 객체 노출 '''
@dataclass(frozen=True)
class KnownSample(Sample):
    species: str


@dataclass
class TestingKnownSample:
    sample: KnownSample
    classification: Optional[str] = None


@dataclass(frozen=True)
class TrainingKnownSample:
    """분류 불가능"""
    sample: KnownSample


@dataclass
class UnknownSample:
    sample: Sample
    classification: Optional[str] = None


class Distance:

    def distance(self, s1: Sample, s2: Sample) -> float:
        raise NotImplementedError


@dataclass
class Hyperparameter:

    k: int
    algorithm: Distance
    data: weakref.ReferenceType["TrainingData"]

    def classify(self, unknown: Sample) -> str:
        """The k-NN algorithm"""
        if not (training_data := self.data()):
            raise RuntimeError("No TrainingData object")
        distances: list[tuple[float, TrainingKnownSample]] = sorted(
            (self.algorithm.distance(unknown, known.sample), known)
            for known in training_data.training
        )
        k_nearest = (known.sample.species for d, known in distances[: self.k])
        frequency: Counter[str] = collections.Counter(k_nearest)
        best_fit, *others = frequency.most_common()
        species, votes = best_fit
        return species


@dataclass
class TrainingData:
    testing: List[TestingKnownSample]
    training: List[TrainingKnownSample]
    tuning: List[Hyperparameter]

