from pathlib import Path
import ast
BASE=Path(__file__).resolve().parent
print('[1/3] Checking Python syntax...')
for p in BASE.rglob('*.py'):
    ast.parse(p.read_text(encoding='utf-8'), filename=str(p))
print('      PASS')
print('[2/3] Checking quiz scoring...')
from quiz import QUIZ
from progress import score_quiz
answers={i:q['answer'] for i,q in enumerate(QUIZ)}
score,_=score_quiz(QUIZ,answers)
assert score==len(QUIZ)
print('      PASS')
print('[3/3] Checking content modules...')
from content.training import MODULES
assert len(MODULES)>=4 and all(m.get('title') and m.get('intro') for m in MODULES)
print('      PASS')
print('\nALL CHECKS PASSED')
