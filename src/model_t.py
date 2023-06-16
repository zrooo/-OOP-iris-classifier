import collections
from typing import Optional, Counter, NamedTuple
import weakref
import sys

"""typing.NamedTuple은 @dataclass(frozen=True)와 비슷
    namedtuple은 상속 지원 X -> 디자인을 상속에서 구성으로 전환 (하위 클래스가 상위 클래스의 멤버인지 여부)"""

class Sample(NamedTuple):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


class KnownSample(NamedTuple):
    sample: Sample
    species: str

# KnownSample 객체를 포함하는 구성 객체
class TestingKnownSample:
    def __init__(
        self, sample: KnownSample, classification: Optional[str] = None
    ) -> None:
        self.sample = sample
        self.classification = classification

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(sample={self.sample!r}, "
            f"classification={self.classification!r})"
        )


class TrainingKnownSample(NamedTuple):
    sample: KnownSample


class UnknownSample:
    def __init__(
        self, sample: KnownSample, classification: Optional[str] = None
    ) -> None:
        self.sample = sample
        self.classification = classification

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(sample={self.sample!r}, classification={self.classification!r})"


class Distance:
    

    def distance(self, s1: Sample, s2: KnownSample) -> float:
        raise NotImplementedError


class Hyperparameter:

    def __init__(self, k: int, algorithm: Distance, data: "TrainingData") -> None:
        self.k = k
        self.algorithm = algorithm
        self.data = weakref.ref(data)

    def classify(self, unknown: Sample) -> str:
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


class TrainingData:
    def __init__(self) -> None:
        self.testing: list[TestingKnownSample] = list()
        self.training: list[TrainingKnownSample] = list()
        self.tuning: list[Hyperparameter] = list()
