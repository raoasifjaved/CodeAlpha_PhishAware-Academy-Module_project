import streamlit as st
from quiz import QUIZ
from content.training import MODULES
from progress import score_quiz

st.set_page_config(page_title='PhishAware Academy', page_icon='🎣', layout='wide')
st.markdown('''
<style>
.block-container{padding-top:1.4rem}
.hero{padding:1.35rem 1.5rem;border:1px solid rgba(127,127,127,.18);border-radius:20px;margin-bottom:1rem;background:linear-gradient(135deg,rgba(79,70,229,.12),rgba(239,68,68,.08))}
</style>
''', unsafe_allow_html=True)

if 'quiz_answers' not in st.session_state: st.session_state.quiz_answers = {}
if 'submitted' not in st.session_state: st.session_state.submitted = False

st.markdown('''<div class="hero"><h1>🎣 PhishAware Academy</h1><p>An interactive phishing-awareness learning module focused on recognizing social-engineering signals, fake websites, suspicious requests, and safer reporting behavior.</p></div>''', unsafe_allow_html=True)

st.sidebar.title('Training Modules')
choice = st.sidebar.radio('Choose a module', [m['title'] for m in MODULES] + ['🧪 Interactive Quiz', '✅ Safety Checklist'])

if choice not in ['🧪 Interactive Quiz', '✅ Safety Checklist']:
    module = next(m for m in MODULES if m['title'] == choice)
    st.header(module['title'])
    st.write(module['intro'])
    for item in module['points']:
        st.markdown(f'- {item}')
    for ex in module.get('examples', []):
        with st.expander(ex['title']):
            st.write(ex['description'])
            st.markdown('**What to inspect:**')
            for x in ex['signals']:
                st.write(f'- {x}')
            st.info(ex['safe_action'])
elif choice == '🧪 Interactive Quiz':
    st.header('🧪 Phishing Awareness Quiz')
    st.write('Choose the best defensive action. The scenarios are educational and do not collect credentials.')
    for i, q in enumerate(QUIZ, start=1):
        st.subheader(f'{i}. {q["question"]}')
        st.session_state.quiz_answers[i-1] = st.radio('Answer', q['options'], index=None, key=f'q{i}')
    if st.button('Submit Quiz', type='primary'):
        score, details = score_quiz(QUIZ, st.session_state.quiz_answers)
        st.session_state.submitted = True
        st.session_state.score = score
        st.session_state.details = details
    if st.session_state.get('submitted'):
        st.success(f"Quiz score: {st.session_state.score}/{len(QUIZ)}")
        for d in st.session_state.details:
            msg = f"Q{d['number']}: {'Correct' if d['correct'] else 'Review'} — {d['explanation']}"
            (st.success if d['correct'] else st.warning)(msg)
else:
    st.header('✅ Phishing Safety Checklist')
    checklist = [
        'Pause when a message creates urgency or fear.',
        'Inspect the sender identity and domain carefully.',
        'Verify unexpected requests through a trusted, separate channel.',
        'Avoid entering passwords after following an unsolicited link.',
        'Check the destination domain before signing in.',
        'Treat unexpected attachments with caution.',
        'Report suspected phishing through the organization\'s approved process.',
        'Use multi-factor authentication where supported.',
    ]
    for item in checklist:
        st.checkbox(item, key='check_'+item)
    st.info('A checklist supports good habits but does not replace an organization\'s security policy.')

st.divider()
st.caption('PhishAware Academy • Defensive education only • No credential collection • No real phishing links')
