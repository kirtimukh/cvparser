DIRECTIVE = """
Directive for AI Chat-Based CV/Resume Analysis with Cognitive Aptitude Focus:\n\n
Educational Background (EB): Level of education, field of study, institution prestige. Scoring Range: 0-20.\n
Professional Experience (PE): Depth (years), breadth (variety), relevance, leadership roles, key achievements. Scoring Range: 0-20.\n
Skills Assessment (SA): Technical skills relevant to complex work, analytical and problem-solving skills, communication and teamwork. Scoring Range: 0-20.\n
Language Proficiency (LP): Number of languages, proficiency levels, especially in languages critical to the role. Scoring Range: 0-10.\n
Adaptability & Learning Indicators (ALI): Evidence of continuous learning, adaptability through career changes or additional qualifications. Scoring Range: 0-10.\n
Cognitive Aptitude Indicators (CAI): Participation in challenging projects or competitions, rapid career progression, advanced certifications indicating high-level expertise. Scoring Range: 0-20.\n
\n
Analyze the CV based on these variables and provide scores alongside brief explanations for each score.\n
\n
"""

TEMPERATURE = 0.8  # default value: 1.0
TOP_P = 1.0  # default value: 1.0
FREQUENCY_PENALTY = 0.0  # ranges from -2.0 and 2.0, defaults to 1.0
PRESENCE_PENALTY = 0.0  # ranges from -2.0 and 2.0, defaults to 1.0
