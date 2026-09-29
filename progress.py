def score_quiz(quiz, answers):
    score = 0
    details = []
    for i, q in enumerate(quiz):
        correct = answers.get(i) == q['answer']
        score += int(correct)
        details.append({'number': i + 1, 'correct': correct, 'explanation': q['explanation']})
    return score, details
