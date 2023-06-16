from __future__ import annotations
import abc
from pathlib import Path
from typing import cast, Type, Union, List
import time


class DirectoryVisitor(abc.ABC):
    queue_class: Type["PathQueue"]

    def __init__(self, base: Path) -> None:
        self.queue = self.queue_class()
        self.queue.put(base)

    @abc.abstractmethod
    def file(self, path: Path) -> None:
        print(path)

    def visit(self) -> None:
        while not self.queue.empty():
            item = self.queue.get()
            if item.is_file():
                self.file(item)
            elif item.is_dir():
                if item.name.startswith("."):
                    continue
                if item.name == "__pycache__":
                    continue
                for sub_item in item.iterdir():
                    self.queue.put(sub_item)


class ListQueue(List[Path]):
   

    def put(self, item: Path) -> None:
        self.append(item)

    def get(self) -> Path:
        return self.pop(0)

    def empty(self) -> bool:
        return len(self) == 0


from typing import Deque


class DeQueue(Deque[Path]):
    
    def put(self, item: Path) -> None:
        self.append(item)

    def get(self) -> Path:
        return self.popleft()

    def empty(self) -> bool:
        return len(self) == 0


import queue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    BaseQueue = queue.Queue[Path]  
else:
    BaseQueue = queue.Queue

    
class ThreadQueue(BaseQueue):
  
    pass


PathQueue = Union[ListQueue, DeQueue, ThreadQueue]


class WalkList(DirectoryVisitor):
    queue_class = ListQueue

    def file(self, path: Path) -> None:
        pass 


class WalkDeque(DirectoryVisitor):
    queue_class = DeQueue

    def file(self, path: Path) -> None:
        pass  


class WalkThread(DirectoryVisitor):
    queue_class = ThreadQueue

    def file(self, path: Path) -> None:
        pass 


if __name__ == "__main__":
    performance: dict[str, float] = {}
    for cls in WalkList, WalkDeque, WalkThread:
        print(cls)
        start = time.perf_counter()
        for _ in range(100):
            walker = cls(Path.cwd())  
            walker.visit()
        end = time.perf_counter()
        performance[cls.__name__] = (end - start) * 1000
        print()
    for cls_name, run_time in performance.items():
        print(f"{cls_name:10s} {run_time:5.2f}ms")
