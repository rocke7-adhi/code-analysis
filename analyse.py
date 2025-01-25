from typing import Dict, List
import re
import ast
import json

class CodeAnalysis:
    def analyze_code(self, code: str, language: str) -> Dict:
        """
        Analyze code for complexity, quality, and potential issues
        Returns formatted analysis results as a string
        """
        try:
            # Perform code analysis
            analysis_result = {
                "complexity_metrics": self._analyze_complexity(code),
                "code_quality": self._analyze_quality(code, language),
                "potential_issues": self._find_issues(code, language)
            }
            
            # Format the results as a readable string
            formatted_result = self._format_analysis_results(analysis_result)
            
            return formatted_result
            
        except Exception as e:
            return f"Error analyzing code: {str(e)}"

    def _analyze_complexity(self, code: str) -> Dict:
        """Analyze code complexity metrics"""
        try:
            tree = ast.parse(code)
            
            # Count function definitions
            function_count = len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)])
            
            # Count class definitions
            class_count = len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)])
            
            lines = code.split('\n')
            
            return {
                "total_lines": len(lines),
                "code_lines": self._count_code_lines(lines),
                "comment_lines": self._count_comment_lines(lines),
                "blank_lines": self._count_blank_lines(lines),
                "cyclomatic_complexity": self._calculate_cyclomatic_complexity(tree),
                "nesting_depth": self._calculate_nesting_depth(code),
                "function_count": function_count,
                "class_count": class_count
            }
        except SyntaxError:
            # Fallback for non-Python code or syntax errors
            lines = code.split('\n')
            return {
                "total_lines": len(lines),
                "code_lines": self._count_code_lines(lines),
                "comment_lines": self._count_comment_lines(lines),
                "blank_lines": self._count_blank_lines(lines),
                "cyclomatic_complexity": self._calculate_basic_complexity(code),
                "nesting_depth": self._calculate_nesting_depth(code),
                "function_count": "N/A",
                "class_count": "N/A"
            }

    def _analyze_quality(self, code: str, language: str) -> Dict:
        """Analyze code quality metrics"""
        lines = code.split('\n')
        
        # Calculate average line length
        code_lines = [line for line in lines if line.strip() and not line.strip().startswith('#')]
        avg_line_length = sum(len(line) for line in code_lines) / len(code_lines) if code_lines else 0
        
        return {
            "average_line_length": round(avg_line_length, 2),
            "long_lines": self._count_long_lines(lines),
            "naming_issues": self._check_naming_conventions(code, language),
            "duplication_score": self._check_code_duplication(code)
        }

    def _find_issues(self, code: str, language: str) -> List[Dict]:
        """Find potential code issues"""
        issues = []
        
        # Check for long functions
        long_functions = self._find_long_functions(code)
        if long_functions:
            issues.append({
                "type": "Long Functions",
                "message": f"Found {len(long_functions)} functions longer than 50 lines",
                "details": [f"Function at line {loc}" for loc in long_functions]
            })

        # Check for deep nesting
        deep_nesting = self._find_deep_nesting(code)
        if deep_nesting:
            issues.append({
                "type": "Deep Nesting",
                "message": "Found code blocks with deep nesting (> 4 levels)",
                "details": [f"Deep nesting at line {loc}" for loc in deep_nesting]
            })

        # Check for long lines
        long_lines = self._find_long_lines(code)
        if long_lines:
            issues.append({
                "type": "Long Lines",
                "message": f"Found {len(long_lines)} lines longer than 100 characters",
                "details": [f"Line {loc}" for loc in long_lines]
            })

        return issues

    def _calculate_cyclomatic_complexity(self, tree: ast.AST) -> int:
        """Calculate cyclomatic complexity using AST"""
        complexity = 1  # Base complexity
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
                
        return complexity

    def _calculate_basic_complexity(self, code: str) -> int:
        """Calculate basic complexity for non-Python code"""
        decision_patterns = [
            r'\bif\b', r'\bfor\b', r'\bwhile\b', r'\bswitch\b', 
            r'\bcatch\b', r'\bcase\b', r'\b&&\b', r'\|\|'
        ]
        complexity = 1
        
        for pattern in decision_patterns:
            complexity += len(re.findall(pattern, code))
            
        return complexity

    def _find_long_lines(self, code: str) -> List[int]:
        """Find lines longer than 100 characters"""
        lines = code.split('\n')
        return [i + 1 for i, line in enumerate(lines) if len(line.strip()) > 100]

    def _check_naming_conventions(self, code: str, language: str) -> List[str]:
        """Check for naming convention issues"""
        issues = []
        
        # Python-specific naming conventions
        if language.lower() == 'python':
            # Check for camelCase variables (Python prefers snake_case)
            camel_case = re.findall(r'\b[a-z]+[A-Z][a-zA-Z]*\b', code)
            if camel_case:
                issues.append(f"Found {len(camel_case)} camelCase names (prefer snake_case)")
                
            # Check for non-uppercase constants
            constants = re.findall(r'\b[a-z_]+\s*=\s*[0-9]+\b', code)
            if constants:
                issues.append(f"Found {len(constants)} non-uppercase constant names")
        
        return issues

    def _count_code_lines(self, lines: List[str]) -> int:
        """Count non-empty, non-comment lines"""
        return len([line for line in lines if line.strip() and not line.strip().startswith(('#', '//', '/*'))])

    def _count_comment_lines(self, lines: List[str]) -> int:
        """Count comment lines"""
        return len([line for line in lines if line.strip().startswith(('#', '//', '/*'))])

    def _count_blank_lines(self, lines: List[str]) -> int:
        """Count blank lines"""
        return len([line for line in lines if not line.strip()])

    def _count_long_lines(self, lines: List[str]) -> int:
        """Count lines longer than 100 characters"""
        return len([line for line in lines if len(line.strip()) > 100])

    def _calculate_nesting_depth(self, code: str) -> int:
        """Calculate maximum nesting depth"""
        lines = code.split('\n')
        max_depth = current_depth = 0
        
        for line in lines:
            indent = len(line) - len(line.lstrip())
            current_depth = indent // 4  # Assuming 4 spaces per indent level
            max_depth = max(max_depth, current_depth)
            
        return max_depth

    def _check_code_duplication(self, code: str) -> float:
        """Check for code duplication"""
        lines = code.split('\n')
        total_lines = len(lines)
        if total_lines == 0:
            return 0.0
            
        # Create chunks of 3 lines and check for duplicates
        chunks = ['\n'.join(lines[i:i+3]) for i in range(0, total_lines-2)]
        duplicates = len(chunks) - len(set(chunks))
        
        # Calculate duplication score (0-1)
        return round(duplicates / total_lines if total_lines > 0 else 0, 2)

    def _find_long_functions(self, code: str) -> List[int]:
        """Find functions longer than 50 lines"""
        lines = code.split('\n')
        function_starts = []
        current_function_start = None
        current_depth = 0
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith(('def ', 'function ')):
                current_function_start = i + 1
                current_depth = len(line) - len(line.lstrip())
            elif current_function_start is not None:
                indent = len(line) - len(line.lstrip())
                if indent <= current_depth and stripped:
                    if i - current_function_start > 50:
                        function_starts.append(current_function_start)
                    current_function_start = None
                    
        return function_starts

    def _find_deep_nesting(self, code: str) -> List[int]:
        """Find locations of deep nesting (> 4 levels)"""
        lines = code.split('\n')
        deep_nesting_lines = []
        
        for i, line in enumerate(lines):
            indent = len(line) - len(line.lstrip())
            if indent // 4 > 4:  # More than 4 levels of nesting
                deep_nesting_lines.append(i + 1)
                
        return deep_nesting_lines

    def _format_analysis_results(self, results: Dict) -> str:
        """Format analysis results as readable text"""
        output = []
        
        # Complexity Metrics
        output.append("=== Code Complexity Analysis ===")
        metrics = results["complexity_metrics"]
        output.append(f"Total Lines: {metrics['total_lines']}")
        output.append(f"Code Lines: {metrics['code_lines']}")
        output.append(f"Comment Lines: {metrics['comment_lines']}")
        output.append(f"Blank Lines: {metrics['blank_lines']}")
        output.append(f"Cyclomatic Complexity: {metrics['cyclomatic_complexity']}")
        output.append(f"Maximum Nesting Depth: {metrics['nesting_depth']}")
        if metrics['function_count'] != "N/A":
            output.append(f"Number of Functions: {metrics['function_count']}")
            output.append(f"Number of Classes: {metrics['class_count']}")
        
        # Code Quality
        output.append("\n=== Code Quality Metrics ===")
        quality = results["code_quality"]
        output.append(f"Average Line Length: {quality['average_line_length']} characters")
        output.append(f"Number of Long Lines: {quality['long_lines']}")
        if quality['naming_issues']:
            output.append("Naming Convention Issues:")
            for issue in quality['naming_issues']:
                output.append(f"  - {issue}")
        output.append(f"Code Duplication Score: {quality['duplication_score']} (0-1 scale)")
        
        # Issues
        if results["potential_issues"]:
            output.append("\n=== Potential Issues ===")
            for issue in results["potential_issues"]:
                output.append(f"\n{issue['type']}:")
                output.append(f"  {issue['message']}")
                for detail in issue['details']:
                    output.append(f"  - {detail}")
        
        return "\n".join(output) 