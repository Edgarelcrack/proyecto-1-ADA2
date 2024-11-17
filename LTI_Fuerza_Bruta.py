from typing import List, Tuple
from dataclasses import dataclass

# Costos de las operaciones
a = 1  
d = 2  
r = 3  
i = 2  
k = 1  

@dataclass
class TransformationResult:
    cost: int
    steps: List[Tuple[str, str]]

class WordTransformer:
    def __init__(self, source: str, target: str):
        self.source = list(source)
        self.target = list(target)
    
    @staticmethod
    def advance(word1: List[str], word2: List[str], pos1: int, pos2: int) -> Tuple[List[str], List[str], int, int]:
        return word1, word2, pos1 + 1, pos2 + 1
    
    @staticmethod
    def delete(word: List[str], pos: int) -> List[str]:
        return word[:pos] + word[pos + 1:]
    
    @staticmethod
    def replace(word1: List[str], word2: List[str], pos1: int, pos2: int) -> Tuple[List[str], int, int]:
        new_word = word1.copy()
        new_word[pos1] = word2[pos2]
        return new_word, pos1 + 1, pos2 + 1
    
    @staticmethod
    def insert(word1: List[str], word2: List[str], pos1: int, pos2: int) -> Tuple[List[str], int, int]:
        new_word = word1[:pos1] + [word2[pos2]] + word1[pos1:]
        return new_word, pos1 + 1, pos2 + 1
    
    @staticmethod
    def kill(word: List[str], pos: int) -> List[str]:
        return word[:pos]
    
    def _calculate_min_cost(
        self,
        word1: List[str],
        word2: List[str],
        pos1: int,
        pos2: int,
        operations: List[Tuple[str, str]],
        costs: List[int]) -> List[TransformationResult]:
        
        #Calcular costo final
        if pos1 == len(word1) and pos2 == len(word2):
            return [TransformationResult(sum(costs), operations)]
        
        results = []
        
        if pos1 == len(word1):
            new_word, new_pos1, new_pos2 = self.insert(word1, word2, pos1, pos2)
            results.extend(
                self._calculate_min_cost(
                    new_word, word2, new_pos1, new_pos2,
                    operations + [(self._to_str(new_word), 'insert')],
                    costs + [i]
                )
            )
        
        elif pos2 == len(word2):
            remaining_chars = len(word1[pos1:])
            if remaining_chars * d < k:
                new_word = self.delete(word1, pos1)
                results.extend(
                    self._calculate_min_cost(
                        new_word, word2, pos1, pos2,
                        operations + [(self._to_str(new_word), 'delete')],
                        costs + [d]
                    )
                )
            else:
                new_word = self.kill(word1, pos1)
                results.extend(
                    self._calculate_min_cost(
                        new_word, word2, pos1, pos2,
                        operations + [(self._to_str(new_word), 'kill')],
                        costs + [k]
                    )
                )
        
        else:
            if word1[pos1] == word2[pos2]:
                _, _, new_pos1, new_pos2 = self.advance(word1, word2, pos1, pos2)
                results.extend(
                    self._calculate_min_cost(
                        word1, word2, new_pos1, new_pos2,
                        operations + [(self._to_str(word1), 'advance')],
                        costs + [a]
                    )
                )
            else:
                operations_to_try = [
                    (self.insert, 'insert', i),
                    (self.delete, 'delete', d),
                    (self.replace, 'replace', r),
                    (self.kill, 'kill', k)
                ]
                
                for operation, op_name, cost in operations_to_try:
                    if op_name in ['insert', 'replace']:
                        new_word, new_pos1, new_pos2 = operation(word1, word2, pos1, pos2)
                    else:
                        new_word = operation(word1, pos1)
                        new_pos1, new_pos2 = pos1, pos2
                    
                    results.extend(
                        self._calculate_min_cost(
                            new_word, word2, new_pos1, new_pos2,
                            operations + [(self._to_str(new_word), op_name)],
                            costs + [cost]
                        )
                    )
        
        return results
    
    @staticmethod
    def _to_str(word_list: List[str]) -> str: #Convierte la lista de caracteres en un string
        return ''.join(word_list)
    
    def transform(self) -> Tuple[int, List[Tuple[str, str]]]: #Devuelve el costo minimo y los pasos para transformar la palabra
        results = self._calculate_min_cost(self.source, self.target, 0, 0, [], [])
        min_result = min(results, key=lambda x: x.cost)
        return min_result.cost, min_result.steps

def main():
    source = "francesa"
    target = "ancestro"
    
    transformer = WordTransformer(source, target)
    min_cost, steps = transformer.transform()
    
    print(f"Minimum cost to transform '{source}' to '{target}': {min_cost}")
    print("\nTransformation steps:")
    for word, operation in steps:
        print(f"{word:<15} -> {operation}")  # Using left alignment with '<'

if __name__ == "__main__":
    main()