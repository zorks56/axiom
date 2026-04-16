#!/usr/bin/env python3
"""
AXIOM Compiler v1.0
Il compilatore definitivo per il linguaggio del futuro profondo.
Traduce AXIOM in Python eseguibile.
"""

import re
import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

class AxiomLexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.tokens = []
        self.line = 1
        self.col = 1
        
    KEYWORDS = {
        'manifest', 'phase', 'observe', 'entangle', 'collapse',
        'superpose', 'evolve', 'for_each', 'when', 'network',
        'resonate', 'range', 'else', 'true', 'false', 'null'
    }
    
    OPERATORS = {
        '->', '<->', '(loop)', 'INF', '(tensor)', '~=', '=>', 'Xi', 'SELF', 'Psi',
        '->', '<-', '<->', '=>', '==', '!=', '<=', '>=',
        '<=', '>=', '!='
    }
    
    def tokenize(self) -> List[tuple]:
        patterns = [
            ('COMMENT', r'//.*|#.*'),
            ('BLOCK_COMMENT', r'/\*[\s\S]*?\*/'),
            ('PHASE_ARROW', r'->'),
            ('DOUBLE_ARROW', r'=>'),
            ('INFINITY', r'INF'),
            ('QUANTUM', r'Xi'),
            ('PSI', r'Psi'),
            ('SELF', r'SELF'),
            ('LESS_EQUAL', r'<='),
            ('GREATER_EQUAL', r'>='),
            ('NOT_EQUAL', r'!='),
            ('NUMBER', r'\d+\.?\d*'),
            ('STRING', r'"[^"]*"|\'[^\']*\''),
            ('IDENT', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('OPERATOR', r'[+\-*/%=<>!|&^~]+'),
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('LBRACE', r'\{'),
            ('RBRACE', r'\}'),
            ('LBRACKET', r'\['),
            ('RBRACKET', r'\]'),
            ('COMMA', r','),
            ('DOT', r'\.'),
            ('COLON', r':'),
            ('NEWLINE', r'\n'),
            ('WHITESPACE', r'[ \t]+'),
        ]
        
        while self.pos < len(self.source):
            matched = False
            for token_type, pattern in patterns:
                regex = re.compile(pattern)
                match = regex.match(self.source, self.pos)
                if match:
                    value = match.group(0)
                    if token_type == 'NEWLINE':
                        self.line += 1
                        self.col = 1
                    elif token_type not in ('WHITESPACE', 'COMMENT', 'BLOCK_COMMENT'):
                        if token_type == 'IDENT' and value in self.KEYWORDS:
                            self.tokens.append(('KEYWORD', value, self.line))
                        else:
                            self.tokens.append((token_type, value, self.line))
                    self.pos = match.end()
                    matched = True
                    break
            if not matched:
                raise SyntaxError(f"Token sconosciuto a linea {self.line}: {self.source[self.pos]}")
        
        return self.tokens

class AxiomParser:
    def __init__(self, tokens: List[tuple]):
        self.tokens = tokens
        self.pos = 0
        
    def peek(self, offset: int = 0) -> Optional[tuple]:
        if self.pos + offset < len(self.tokens):
            return self.tokens[self.pos + offset]
        return None
        
    def consume(self, expected_type: str = None, expected_value: str = None) -> tuple:
        token = self.peek()
        if token is None:
            raise SyntaxError("Fine inattesa del file")
        if expected_type and token[0] != expected_type:
            if expected_value and token[1] != expected_value:
                raise SyntaxError(f"Atteso {expected_type}/{expected_value}, trovato {token}")
        self.pos += 1
        return token
        
    def parse(self) -> List[Dict[str, Any]]:
        statements = []
        while self.pos < len(self.tokens):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return statements
    
    def parse_statement(self) -> Optional[Dict[str, Any]]:
        token = self.peek()
        if token is None:
            return None
            
        if token[0] == 'KEYWORD':
            if token[1] == 'manifest':
                return self.parse_manifest()
            elif token[1] == 'phase':
                return self.parse_phase()
            elif token[1] == 'observe':
                return self.parse_observe()
            elif token[1] == 'entangle':
                return self.parse_entangle()
            elif token[1] == 'for_each':
                return self.parse_for_each()
            elif token[1] == 'when':
                return self.parse_when()
            elif token[1] == 'network':
                return self.parse_network()
            elif token[1] == 'evolve':
                self.consume()
                return {'type': 'evolve'}
            elif token[1] == 'resonate':
                return self.parse_resonate()
            elif token[1] == 'collapse':
                return self.parse_collapse()
        elif token[0] == 'IDENT':
            return self.parse_expression_statement()
            
        self.consume()
        return None
    
    def parse_manifest(self) -> Dict[str, Any]:
        self.consume()
        name = self.consume('IDENT')[1]
        
        if self.peek() and self.peek()[0] == 'OPERATOR' and self.peek()[1] == '=':
            self.consume()
            value = self.parse_expression()
            return {'type': 'manifest_assign', 'name': name, 'value': value}
        
        params = []
        if self.peek() and self.peek()[0] == 'LPAREN':
            self.consume('LPAREN')
            while self.peek() and self.peek()[0] != 'RPAREN':
                param_name = self.consume('IDENT')[1]
                self.consume('COLON')
                param_type = self.consume('IDENT')[1]
                params.append({'name': param_name, 'type': param_type})
                if self.peek() and self.peek()[0] == 'COMMA':
                    self.consume()
            self.consume('RPAREN')
        
        body = []
        if self.peek() and self.peek()[0] == 'LBRACE':
            self.consume('LBRACE')
            while self.peek() and self.peek()[0] != 'RBRACE':
                stmt = self.parse_statement()
                if stmt:
                    body.append(stmt)
            self.consume('RBRACE')
        
        return {'type': 'manifest', 'name': name, 'params': params, 'body': body}
    
    def parse_phase(self) -> Dict[str, Any]:
        self.consume()
        name = self.consume('IDENT')[1]
        params = []
        return_type = None
        
        if self.peek() and self.peek()[0] == 'LPAREN':
            self.consume('LPAREN')
            while self.peek() and self.peek()[0] != 'RPAREN':
                param_name = self.consume('IDENT')[1]
                if self.peek() and self.peek()[0] == 'COLON':
                    self.consume()
                    param_type = self.consume('IDENT')[1]
                else:
                    param_type = None
                params.append({'name': param_name, 'type': param_type})
                if self.peek() and self.peek()[0] == 'COMMA':
                    self.consume()
            self.consume('RPAREN')
        
        if self.peek() and self.peek()[0] == 'PHASE_ARROW':
            self.consume()
            return_type = self.consume('IDENT')[1]
        
        body = []
        if self.peek() and self.peek()[0] == 'LBRACE':
            self.consume('LBRACE')
            while self.peek() and self.peek()[0] != 'RBRACE':
                stmt = self.parse_statement()
                if stmt:
                    body.append(stmt)
            self.consume('RBRACE')
        
        return {'type': 'phase', 'name': name, 'params': params, 'return': return_type, 'body': body}
    
    def parse_observe(self) -> Dict[str, Any]:
        self.consume()
        expr = self.parse_expression()
        return {'type': 'observe', 'value': expr}
    
    def parse_entangle(self) -> Dict[str, Any]:
        self.consume()
        name = self.consume('IDENT')[1]
        var_type = None
        value = None
        
        if self.peek() and self.peek()[0] == 'COLON':
            self.consume()
            var_type = self.consume('IDENT')[1]
        
        if self.peek() and self.peek()[0] == 'OPERATOR' and self.peek()[1] == '=':
            self.consume()
            value = self.parse_expression()
        
        return {'type': 'entangle', 'name': name, 'var_type': var_type, 'value': value}
    
    def parse_for_each(self) -> Dict[str, Any]:
        self.consume()
        var_name = self.consume('IDENT')[1]
        
        if self.peek() and self.peek()[1] == 'in':
            self.consume()
        
        iterable = self.parse_expression()
        body = []
        
        if self.peek() and self.peek()[0] == 'LBRACE':
            self.consume('LBRACE')
            while self.peek() and self.peek()[0] != 'RBRACE':
                stmt = self.parse_statement()
                if stmt:
                    body.append(stmt)
            self.consume('RBRACE')
        
        return {'type': 'for_each', 'var': var_name, 'iterable': iterable, 'body': body}
    
    def parse_when(self) -> Dict[str, Any]:
        self.consume()
        condition = self.parse_expression()
        body = []
        else_body = []
        in_when = True
        inline_return = None
        
        if self.peek() and self.peek()[0] == 'PHASE_ARROW':
            self.consume()
            when_return = self.parse_expression()
            
            else_return = None
            if self.peek() and self.peek()[0] == 'KEYWORD' and self.peek()[1] == 'else':
                self.consume()
                if self.peek() and self.peek()[0] == 'PHASE_ARROW':
                    self.consume()
                    else_return = self.parse_expression()
            
            return {'type': 'when_inline', 'condition': condition, 'when_return': when_return, 'else_return': else_return}
        
        if self.peek() and self.peek()[0] == 'LBRACE':
            self.consume('LBRACE')
            while self.peek() and self.peek()[0] != 'RBRACE':
                token = self.peek()
                if token[0] == 'KEYWORD' and token[1] == 'else':
                    self.consume()
                    in_when = False
                    if self.peek() and self.peek()[0] == 'LBRACE':
                        self.consume('LBRACE')
                        while self.peek() and self.peek()[0] != 'RBRACE':
                            stmt = self.parse_statement()
                            if stmt:
                                else_body.append(stmt)
                        self.consume('RBRACE')
                    break
                stmt = self.parse_statement()
                if stmt:
                    body.append(stmt)
            if in_when:
                self.consume('RBRACE')
        
        return {'type': 'when', 'condition': condition, 'body': body, 'else': else_body}
    
    def parse_network(self) -> Dict[str, Any]:
        self.consume()
        name = self.consume('IDENT')[1]
        return {'type': 'network', 'name': name}
    
    def parse_resonate(self) -> Dict[str, Any]:
        self.consume()
        expr = self.parse_expression()
        body = []
        
        if self.peek() and self.peek()[0] == 'LBRACE':
            self.consume('LBRACE')
            while self.peek() and self.peek()[0] != 'RBRACE':
                stmt = self.parse_statement()
                if stmt:
                    body.append(stmt)
            self.consume('RBRACE')
        
        return {'type': 'resonate', 'iterable': expr, 'body': body}
    
    def parse_collapse(self) -> Dict[str, Any]:
        self.consume()
        expr = self.parse_expression()
        return {'type': 'collapse', 'value': expr}
    
    def parse_expression(self) -> Dict[str, Any]:
        return self.parse_comparison()
    
    def parse_comparison(self) -> Dict[str, Any]:
        left = self.parse_additive()
        
        while self.peek() and self.peek()[0] in ('OPERATOR', 'LESS_EQUAL', 'GREATER_EQUAL', 'NOT_EQUAL'):
            op = self.peek()[1]
            self.consume()
            right = self.parse_additive()
            left = {'type': 'binary', 'op': op, 'left': left, 'right': right}
        
        return left
    
    def parse_additive(self) -> Dict[str, Any]:
        left = self.parse_multiplicative()
        
        while self.peek() and self.peek()[0] == 'OPERATOR' and self.peek()[1] in ('+', '-'):
            op = self.peek()[1]
            self.consume()
            right = self.parse_multiplicative()
            left = {'type': 'binary', 'op': op, 'left': left, 'right': right}
        
        return left
    
    def parse_multiplicative(self) -> Dict[str, Any]:
        left = self.parse_unary()
        
        while self.peek() and self.peek()[0] == 'OPERATOR' and self.peek()[1] in ('*', '/', '%'):
            op = self.peek()[1]
            self.consume()
            right = self.parse_unary()
            left = {'type': 'binary', 'op': op, 'left': left, 'right': right}
        
        return left
    
    def parse_unary(self) -> Dict[str, Any]:
        if self.peek() and self.peek()[0] == 'OPERATOR' and self.peek()[1] == '-':
            self.consume()
            return {'type': 'unary', 'op': '-', 'operand': self.parse_unary()}
        return self.parse_primary()
    
    def parse_primary(self) -> Dict[str, Any]:
        token = self.peek()
        if token is None:
            return {'type': 'literal', 'value': None}
            
        if token[0] == 'NUMBER':
            self.consume()
            return {'type': 'number', 'value': float(token[1]) if '.' in token[1] else int(token[1])}
        
        if token[0] == 'STRING':
            self.consume()
            return {'type': 'string', 'value': token[1][1:-1]}
        
        if token[0] in ('IDENT', 'PSI', 'QUANTUM', 'SELF'):
            self.consume()
            name = token[1]
            
            if self.peek() and self.peek()[0] == 'LPAREN':
                self.consume('LPAREN')
                args = []
                while self.peek() and self.peek()[0] != 'RPAREN':
                    args.append(self.parse_expression())
                    if self.peek() and self.peek()[0] == 'COMMA':
                        self.consume()
                self.consume('RPAREN')
                return {'type': 'call', 'name': name, 'args': args}
            
            if self.peek() and self.peek()[0] == 'DOT':
                self.consume()
                method = self.peek()[1]
                self.consume()
                if self.peek() and self.peek()[0] == 'LPAREN':
                    self.consume('LPAREN')
                    args = []
                    while self.peek() and self.peek()[0] != 'RPAREN':
                        args.append(self.parse_expression())
                        if self.peek() and self.peek()[0] == 'COMMA':
                            self.consume()
                    self.consume('RPAREN')
                    return {'type': 'method_call', 'obj': name, 'method': method, 'args': args}
                return {'type': 'attribute', 'obj': name, 'attr': method}
            
            if self.peek() and self.peek()[0] == 'LBRACKET':
                self.consume('LBRACKET')
                index = self.parse_expression()
                self.consume('RBRACKET')
                return {'type': 'index', 'obj': name, 'index': index}
            
            return {'type': 'var', 'name': name}
        
        if token[0] == 'LBRACKET':
            self.consume()
            items = []
            while self.peek() and self.peek()[0] != 'RBRACKET':
                items.append(self.parse_expression())
                if self.peek() and self.peek()[0] == 'COMMA':
                    self.consume()
            self.consume('RBRACKET')
            return {'type': 'list', 'items': items}
        
        if token[0] == 'LBRACE':
            self.consume()
            items = []
            while self.peek() and self.peek()[0] != 'RBRACE':
                items.append(self.parse_expression())
                if self.peek() and self.peek()[0] == 'COMMA':
                    self.consume()
            self.consume('RBRACE')
            return {'type': 'set', 'items': items}
        
        if token[0] == 'KEYWORD':
            keyword = token[1]
            self.consume()
            if keyword == 'true':
                return {'type': 'boolean', 'value': True}
            if keyword == 'false':
                return {'type': 'boolean', 'value': False}
            if keyword == 'null':
                return {'type': 'null', 'value': None}
            if keyword in ('range', 'superpose', 'collapse', 'evolve'):
                args = []
                if self.peek() and self.peek()[0] == 'LPAREN':
                    self.consume('LPAREN')
                    while self.peek() and self.peek()[0] != 'RPAREN':
                        args.append(self.parse_expression())
                        if self.peek() and self.peek()[0] == 'COMMA':
                            self.consume()
                    self.consume('RPAREN')
                return {'type': 'call', 'name': keyword, 'args': args}
        
        self.consume()
        return {'type': 'literal', 'value': None}
    
    def parse_expression_statement(self) -> Dict[str, Any]:
        expr = self.parse_expression()
        return {'type': 'expr_stmt', 'expr': expr}

class AxiomCodeGenerator:
    def __init__(self, ast: List[Dict[str, Any]]):
        self.ast = ast
        self.indent_level = 0
        self.functions = []
        self.global_vars = []
        self.main_body = []
        
    def generate(self) -> str:
        lines = [
            '#!/usr/bin/env python3',
            '# Compilato da AXIOM v1.0',
            '# Il linguaggio del futuro profondo',
            '',
            'from typing import List, Any, Optional, Union',
            'from collections.abc import Iterable',
            'import threading',
            'import time',
            '',
            '# ============ AXIOM RUNTIME ============',
            '',
            '_quantum_cache = {}',
            '_entangle_registry = {}',
            '_evolution_enabled = True',
            '',
            'def superpose(*states):',
            '    """AXIOM: Crea uno stato quantistico sovrapposto"""',
            '    return {"_axiom_quantum": True, "states": list(states)}',
            '',
            'def is_quantum(val):',
            '    """AXIOM: Verifica se un valore e quantistico"""',
            '    return isinstance(val, dict) and val.get("_axiom_quantum", False)',
            '',
            'def collapse(qval):',
            '    """AXIOM: Collassa uno stato quantistico"""',
            '    if is_quantum(qval):',
            '        return qval["states"][0]',
            '    return qval',
            '',
        ]
        
        for node in self.ast:
            if node['type'] in ('manifest', 'phase'):
                self.functions.append(self.generate_function(node))
        
        main_nodes = [n for n in self.ast if n['type'] not in ('manifest', 'phase')]
        if main_nodes:
            self.main_body = self.generate_body(main_nodes, {})
        
        lines.extend(self.functions)
        lines.append('')
        lines.append('# ============ MAIN ENTRY ============')
        lines.append('')
        lines.append('def _axiom_main():')
        lines.append('    print("=" * 50)')
        lines.append('    print("AXIOM Runtime v1.0 - Anno 52026 d.C.")')
        lines.append('    print("=" * 50)')
        lines.append('    print()')
        
        for stmt in self.main_body:
            lines.append('    ' + stmt)
        
        lines.append('')
        lines.append('if __name__ == "__main__":')
        lines.append('    main()')
        
        return '\n'.join(lines)
    
    def generate_function(self, node: Dict[str, Any]) -> str:
        params = [p['name'] for p in node.get('params', [])]
        param_str = ', '.join(params)
        
        lines = [f'def {node["name"]}({param_str}):']
        
        if node.get('body'):
            body_lines = self.generate_body(node['body'], {p['name']: p['name'] for p in node.get('params', [])})
            for line in body_lines:
                lines.append('    ' + line)
        else:
            lines.append('    pass')
        
        return '\n'.join(lines)
    
    def generate_body(self, body: List[Dict], local_vars: Dict) -> List[str]:
        lines = []
        for stmt in body:
            lines.extend(self.generate_statement(stmt, local_vars))
        return lines
    
    def generate_statement(self, stmt: Dict[str, Any], local_vars: Dict) -> List[str]:
        stype = stmt['type']
        
        if stype == 'observe':
            value = self.resolve_expr_str(stmt['value'], local_vars)
            return [f'print({value})']
        
        elif stype == 'entangle':
            if stmt.get('value'):
                val_str = self.resolve_expr_str(stmt['value'], local_vars)
                local_vars[stmt['name']] = stmt['name']
                return [f'{stmt["name"]} = {val_str}']
            else:
                local_vars[stmt['name']] = stmt['name']
                return [f'{stmt["name"]} = None']
        
        elif stype == 'manifest_assign':
            val_str = self.resolve_expr_str(stmt['value'], local_vars)
            local_vars[stmt['name']] = stmt['name']
            return [f'{stmt["name"]} = {val_str}']
        
        elif stype == 'for_each':
            iter_str = self.resolve_expr_str(stmt['iterable'], local_vars)
            lines = [f'for {stmt["var"]} in {iter_str}:']
            body_lines = self.generate_body(stmt.get('body', []), {**local_vars, stmt['var']: stmt['var']})
            for line in body_lines:
                lines.append('    ' + line)
            return lines
        
        elif stype == 'when':
            cond_str = self.resolve_expr_str(stmt['condition'], local_vars)
            lines = [f'if {cond_str}:']
            body_lines = self.generate_body(stmt.get('body', []), local_vars)
            for line in body_lines:
                lines.append('    ' + line)
            if stmt.get('else'):
                lines.append('else:')
                else_lines = self.generate_body(stmt['else'], local_vars)
                for line in else_lines:
                    lines.append('    ' + line)
            return lines
        
        elif stype == 'resonate':
            iter_str = self.resolve_expr_str(stmt['iterable'], local_vars)
            lines = [f'threading.Thread(target=lambda: list({iter_str})).start()']
            return lines
        
        elif stype == 'evolve':
            return ['print("* Evoluzione del codice in corso...")']
        
        elif stype == 'collapse':
            val_str = self.resolve_expr_str(stmt['value'], local_vars)
            return [f'collapse({val_str})']
        
        elif stype == 'expr_stmt':
            val_str = self.resolve_expr_str(stmt['expr'], local_vars)
            return [val_str]
        
        elif stype == 'network':
            return [f'global {stmt["name"]}']
        
        elif stype == 'when_inline':
            cond_str = self.resolve_expr_str(stmt['condition'], local_vars)
            when_str = self.resolve_expr_str(stmt['when_return'], local_vars)
            lines = []
            lines.append(f'if {cond_str}: return {when_str}')
            if stmt.get('else_return'):
                else_str = self.resolve_expr_str(stmt['else_return'], local_vars)
                lines.append(f'else: return {else_str}')
            return lines
        
        return []
    
    def resolve_expr_str(self, expr: Dict, local_vars: Dict) -> str:
        if not expr:
            return 'None'
        
        etype = expr['type']
        
        if etype == 'number':
            return str(expr['value'])
        elif etype == 'string':
            return f'f"{expr["value"]}"' if '{' in expr['value'] else f'"{expr["value"]}"'
        elif etype == 'boolean':
            return 'True' if expr['value'] else 'False'
        elif etype == 'null':
            return 'None'
        elif etype == 'var':
            return expr['name']
        elif etype == 'binary':
            left = self.resolve_expr_str(expr['left'], local_vars)
            right = self.resolve_expr_str(expr['right'], local_vars)
            return f'({left} {expr["op"]} {right})'
        elif etype == 'unary':
            operand = self.resolve_expr_str(expr['operand'], local_vars)
            return f'({expr["op"]} {operand})'
        elif etype == 'list':
            items = ', '.join(self.resolve_expr_str(item, local_vars) for item in expr['items'])
            return f'[{items}]'
        elif etype == 'call':
            args = ', '.join(self.resolve_expr_str(arg, local_vars) for arg in expr['args'])
            return f'{expr["name"]}({args})'
        elif etype == 'method_call':
            obj = expr['obj']
            args = ', '.join(self.resolve_expr_str(arg, local_vars) for arg in expr['args'])
            return f'{obj}.{expr["method"]}({args})'
        elif etype == 'index':
            obj = expr['obj']
            idx = self.resolve_expr_str(expr['index'], local_vars)
            return f'{obj}[{idx}]'
        
        return 'None'

class AxiomCompiler:
    def __init__(self):
        self.lexer = None
        self.parser = None
        self.generator = None
        
    def compile_file(self, input_path: str, output_path: str = None):
        source = Path(input_path).read_text(encoding='utf-8')
        return self.compile(source, output_path)
    
    def compile(self, source: str, output_path: str = None) -> str:
        print('=' * 50)
        print('* AXIOM COMPILER v1.0 *')
        print('Anno 52026 d.C. - Oltre la singolarità')
        print('=' * 50)
        print()
        
        print('[1/4] Tokenizzazione in corso...')
        self.lexer = AxiomLexer(source)
        tokens = self.lexer.tokenize()
        print(f'      {len(tokens)} token generati')
        
        print('[2/4] Parsing AST...')
        self.parser = AxiomParser(tokens)
        ast = self.parser.parse()
        print(f'      {len(ast)} nodi AST generati')
        import json
        Path('debug_ast.json').write_text(json.dumps(ast, indent=2), encoding='utf-8')
        
        print('[3/4] Generazione codice Python...')
        self.generator = AxiomCodeGenerator(ast)
        python_code = self.generator.generate()
        
        print('[4/4] Scrittura output...')
        if output_path:
            Path(output_path).write_text(python_code, encoding='utf-8')
            print(f'      [OK] Compilato: {output_path}')
        
        print()
        print('=' * 50)
        print('[OK] COMPILAZIONE COMPLETATA')
        print('=' * 50)
        
        return python_code
    
    def run(self, source: str):
        code = self.compile(source)
        print()
        print('=' * 50)
        print('* ESECUZIONE IN CORSO *')
        print('=' * 50)
        print()
        exec(code, {})

def main():
    compiler = AxiomCompiler()
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.axm', '_compiled.py')
        
        if input_file == '--run':
            code = sys.argv[2] if len(sys.argv) > 2 else None
            if code:
                compiler.run(open(code).read())
        else:
            compiler.compile_file(input_file, output_file)
    else:
        print()
        print('+-' * 30 + '+')
        print('|         AXIOM Language Compiler v1.0           |')
        print('|     Il linguaggio del futuro profondo          |')
        print('+-' * 30 + '+')
        print('                                                  ')
        print('  Uso: axiom_compiler.py <input.axm> [output.py] ')
        print('                                                  ')
        print('  Esempi:                                         ')
        print('    axiom_compiler.py program.axm                 ')
        print('    axiom_compiler.py program.axm output.py       ')
        print()
        print()
        print('=' * 50)
        print('  AXIOM Language Compiler v1.0')
        print('  Il linguaggio del futuro profondo')
        print('=' * 50)
        print()
        print('  Uso: axiom_compiler.py <input.axm> [output.py]')
        print()
        print('  Esempi:')
        print('    axiom_compiler.py program.axm')
        print('    axiom_compiler.py program.axm output.py')
        print()
        print()
        
        demo_code = '''
phase fibonacci(n) {
    when n <= 1 -> n
    else -> fibonacci(n - 1) + fibonacci(n - 2)
}

phase main() {
    manifest sequenza = []

    for_each i in range(10) {
        sequenza.append(fibonacci(i))
    }

    observe "=" * 40
    observe "AXIOM Demo - Fibonacci Quantistico"
    observe "=" * 40
    observe ""
    observe "Sequenza di Fibonacci primordiale:"
    observe sequenza

    entangle Psi = superpose(1, 2, 3, 5, 8)
    observe ""
    observe "Stati quantistici disponibili: Psi = {1, 2, 3, 5, 8}"

    entangle messaggio = "La singolarita' e' vicina. Benvenuti nel futuro profondo."
    observe ""
    observe messaggio
    observe ""
    observe "=" * 40
    observe "Fine computazione quantistica"
    observe "=" * 40
}
'''
        print('Esecuzione demo integrata:')
        print()
        compiler.run(demo_code)

if __name__ == '__main__':
    main()
