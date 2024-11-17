from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class TransformationResult:
    cost: int
    steps: List[Tuple[str, str]]

class GreedyWordTransformer:
    def __init__(self, source: str, target: str, costs: dict = None):
        self.source = source
        self.target = target
        # Default costs if none provided
        self.costs = costs
    
    def transform(self) -> Tuple[int, List[Tuple[str, str]]]:
        x, y = 0, 0  # Position pointers for source and target
        current_state = self.source
        total_cost = 0
        operations = []
        kill_used = False
        
        while x < len(current_state) and y < len(self.target):
            if current_state[x] == self.target[y]:
                # Advance operation
                operations.append((current_state, "advance"))
                x += 1
                y += 1
                total_cost += self.costs['advance']
            else:
                operation, new_state, new_x, new_y, cost = self._choose_best_operation(
                    current_state, x, y, kill_used
                )
                
                if operation.startswith("kill"):
                    kill_used = True
                
                current_state = new_state
                x, y = new_x, new_y
                total_cost += cost
                operations.append((current_state, operation))
                
                if kill_used:
                    break
        
        # Handle remaining characters
        total_cost, operations = self._handle_remaining_chars(
            current_state, x, y, total_cost, operations, kill_used
        )
        
        return total_cost, operations
    
    def _choose_best_operation(
        self, 
        current: str, 
        x: int, 
        y: int, 
        kill_used: bool
    ) -> Tuple[str, str, int, int, int]:
        """Choose the best operation based on costs."""
        chars_remaining = len(current) - x
        kill_cost = self.costs['kill']
        
        # Check if kill is the best option
        if not kill_used and kill_cost <= chars_remaining * self.costs['delete']:
            return (
                "kill from cursor to end",
                current[:x],
                x,
                y,
                kill_cost
            )
        
        # Compare costs of other operations
        operations = {
            'replace': (
                f"replace '{current[x]}' with '{self.target[y]}'",
                current[:x] + self.target[y] + current[x+1:],
                x + 1,
                y + 1,
                self.costs['replace']
            ),
            'delete': (
                f"delete '{current[x]}'",
                current[:x] + current[x+1:],
                x,
                y,
                self.costs['delete']
            ),
            'insert': (
                f"insert '{self.target[y]}'",
                current[:x] + self.target[y] + current[x:],
                x,
                y + 1,
                self.costs['insert']
            )
        }
        
        # Find operation with minimum cost
        min_cost = float('inf')
        best_operation = None
        
        for operation_data in operations.values():
            if operation_data[4] < min_cost:
                min_cost = operation_data[4]
                best_operation = operation_data
        
        return best_operation
    
    def _handle_remaining_chars(
        self,
        current: str,
        x: int,
        y: int,
        total_cost: int,
        operations: List[Tuple[str, str]],
        kill_used: bool
    ) -> Tuple[int, List[Tuple[str, str]]]:
        """Handle any remaining characters in either string."""
        # Insert remaining characters from target
        while y < len(self.target):
            current += self.target[y]
            operations.append((current, f"insert '{self.target[y]}'"))
            y += 1
            total_cost += self.costs['insert']
        
        # Kill remaining characters from source if not already killed
        if x < len(current) and not kill_used:
            operations.append((current[:x], "kill from cursor to end"))
            total_cost += self.costs['kill']
        
        return total_cost, operations

def main():
    # Example usage
    source = "ingeneero"
    target = "ingeniero"
    
    costs = {
        'advance': 1,  # a
        'delete': 2,   # d
        'replace': 3,  # r
        'insert': 2,   # i
        'kill': 1      # k
    }
    
    transformer = GreedyWordTransformer(source, target, costs)
    min_cost, steps = transformer.transform()
    
    print(f"El costo mínimo para transformar '{source}' en '{target}' es: {min_cost}")
    print("\nPasos de la transformación:")
    for state, operation in steps:
        print(f"{state:<15} -> {operation}")

if __name__ == "__main__":
    main()