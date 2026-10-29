"""Small genuine supervised classifier; synthetic examples only, no generative AI."""
import json, re
from pathlib import Path
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity

ROOT=Path(__file__).resolve().parent
QUESTIONS={
 'manifest':'Which specimen identifier and source-file columns should the manifest include?',
 'metadata':'Which units, timestamps and context fields are required for your metadata checklist?',
 'handoff':'Who receives the handoff, and which review steps should the receiving collaborator follow?'}

class LocalClassifier:
    ready=True
    description='Local ML classifier (synthetic training, not generative AI)'
    def __init__(self):
        rows=json.loads((ROOT/'model_data/train.json').read_text())
        self.vectorizer=TfidfVectorizer(ngram_range=(1,2),stop_words="english",lowercase=True,sublinear_tf=True)
        self.training=self.vectorizer.fit_transform([r['text'] for r in rows])
        self.model=LogisticRegression(C=4.0,random_state=20261029,max_iter=500)
        self.model.fit(self.training,[r['label'] for r in rows])
    def predict(self,text):
        x=self.vectorizer.transform([text]);probs=self.model.predict_proba(x)[0]
        ranks=np.argsort(probs);best=int(ranks[-1]);score=float(probs[best]);margin=score-float(probs[int(ranks[-2])])
        similarity=float(cosine_similarity(x,self.training).max())
        # Lexical novelty, low model score or ambiguous category => no suggestion.
        domain=bool(re.search(r'\b(sample|samples|specimen|specimens|csv|dataset|data|files?|metadata|manifest|collaborator|handoff|handover)\b',text.lower()))
        abstain=not domain or x.nnz==0 or similarity<0.18 or score<0.45 or margin<0.08
        return {'category':None if abstain else str(self.model.classes_[best]),'score':round(score,4),'margin':round(margin,4),'similarity':round(similarity,4),'abstained':bool(abstain)}
    def scope(self,text):
        result=self.predict(text)
        if result['abstained']:
            questions=['Local ML abstained: the request is unfamiliar or ambiguous. Which catalog service best matches your intended scope?', 'Please clarify the required deliverable before approving the intake.']
        else:
            questions=[f"Local ML suggests {result['category']} (uncalibrated model score {result['score']:.2f}). Is this the correct primary scope?", QUESTIONS[result['category']]]
        # Source text is copied exactly, never generated or interpreted as scientific fact.
        quote=text[:400]
        return {'facts':[{'statement':quote,'quote':quote}],'questions':questions}
