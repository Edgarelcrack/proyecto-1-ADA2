from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class DPCell:
    cost: float
    operations: List[Tuple[str, str]]

class DynamicWordTransformer:
    def __init__(self, source: str, target: str, costs: dict = None):
        self.source = source
        self.target = target
        self.n = len(source)
        self.m = len(target)
        self.costs = costs
        
        # Initialize DP table
        self.dp_table: List[List[DPCell]] = self._initialize_dp_table()
    
    def _initialize_dp_table(self) -> List[List[DPCell]]:

        dp = [[DPCell(float('inf'), []) for _ in range(self.m + 1)] 
              for _ in range(self.n + 1)]
        
        # Base case
        dp[0][0] = DPCell(0, [(self.source, "No operation")])
        
        # (deletions)
        for x in range(1, self.n + 1):
            cost = dp[x-1][0].cost + self.costs['delete']
            new_source = self.source[:x-1]
            operations = dp[x-1][0].operations + [(new_source, f"delete '{self.source[x-1]}'")]
            dp[x][0] = DPCell(cost, operations)
        
        # (insertions)
        for y in range(1, self.m + 1):
            cost = dp[0][y-1].cost + self.costs['insert']
            new_source = dp[0][y-1].operations[-1][0] + self.target[y-1]
            operations = dp[0][y-1].operations + [(new_source, f"insert '{self.target[y-1]}'")]
            dp[0][y] = DPCell(cost, operations)
        
        return dp
    
    def _calculate_operation_costs(self, x: int, y: int) -> List[Tuple[float, str, str, List[Tuple[str, str]]]]:
        """Calculate costs and new states for all possible operations at position (x,y)."""
        operations = []
        current_cell = self.dp_table[x-1][y-1]
        
        # Advance or Replace
        if self.source[x-1] == self.target[y-1]:
            cost = current_cell.cost + self.costs['advance']
            new_source = current_cell.operations[-1][0]
            operations.append((
                cost,
                "advance",
                new_source,
                current_cell.operations
            ))
        else:
            cost = current_cell.cost + self.costs['replace']
            new_source = (current_cell.operations[-1][0][:x-1] + 
                         self.target[y-1] + 
                         current_cell.operations[-1][0][x:])
            operations.append((
                cost,
                f"replace '{self.source[x-1]}' with '{self.target[y-1]}'",
                new_source,
                current_cell.operations
            ))
        
        # Delete
        delete_cell = self.dp_table[x-1][y]
        cost = delete_cell.cost + self.costs['delete']
        new_source = delete_cell.operations[-1][0][:x-1] + delete_cell.operations[-1][0][x:]
        operations.append((
            cost,
            f"delete '{self.source[x-1]}'",
            new_source,
            delete_cell.operations
        ))
        
        # Insert
        insert_cell = self.dp_table[x][y-1]
        cost = insert_cell.cost + self.costs['insert']
        new_source = (insert_cell.operations[-1][0][:x] + 
                     self.target[y-1] + 
                     insert_cell.operations[-1][0][x:])
        operations.append((
            cost,
            f"insert '{self.target[y-1]}'",
            new_source,
            insert_cell.operations
        ))
        
        # Kill (only when reaching end of target)
        if y == self.m and x > self.m:
            kill_cell = self.dp_table[x-1][y]
            cost = kill_cell.cost + self.costs['kill']
            operations.append((
                cost,
                'kill',
                self.target,
                kill_cell.operations
            ))
        
        return operations
    
    def _find_best_operation(self, operations: List[Tuple[float, str, str, List[Tuple[str, str]]]]) -> DPCell:
        """Find the operation with minimum cost and return the resulting cell."""
        min_cost = float('inf')
        best_operation = None
        
        for cost, operation, new_source, prev_operations in operations:
            if cost < min_cost:
                min_cost = cost
                best_operation = (operation, new_source, prev_operations)
        
        operation, new_source, prev_operations = best_operation
        return DPCell(min_cost, prev_operations + [(new_source, operation)])
    
    def transform(self) -> Tuple[float, List[Tuple[str, str]]]:
        """Calculate the minimum cost transformation using dynamic programming."""
        # Fill the DP table
        for x in range(1, self.n + 1):
            for y in range(1, self.m + 1):
                operations = self._calculate_operation_costs(x, y)
                self.dp_table[x][y] = self._find_best_operation(operations)
                
                # Early return if kill operation was used
                if self.dp_table[x][y].operations[-1][1] == 'kill':
                    return (self.dp_table[x][y].cost, 
                           self.dp_table[x][y].operations)
        
        return (self.dp_table[self.n][self.m].cost, 
                self.dp_table[self.n][self.m].operations)

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
    
    transformer = DynamicWordTransformer(source, target, costs)
    min_cost, steps = transformer.transform()
    
    print(f"El costo mínimo para transformar '{source}' en '{target}' es: {min_cost}")
    print("\nPasos de la transformación:")
    for state, operation in steps:
        print(f"{state:<15} -> {operation}")

if __name__ == "__main__":
    main()