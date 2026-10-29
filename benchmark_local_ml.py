"""Transparent tiny synthetic benchmark; no claim of general-world validation."""
import json,hashlib,datetime
from pathlib import Path
from local_ml import LocalClassifier
p=Path(__file__).resolve().parent
model=LocalClassifier()
train=json.loads((p/'model_data/train.json').read_text())
rows=json.loads((p/'model_data/heldout.json').read_text())
ood=json.loads((p/'model_data/out_of_domain.json').read_text())
assert not {r['text'].casefold() for r in train}&{r['text'].casefold() for r in rows}
results=[{**r,'prediction':model.predict(r['text'])} for r in rows]
unknown=[{**r,'prediction':model.predict(r['text'])} for r in ood]
report={'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'training_count':len(train),'heldout_count':len(rows),'correct':sum(r['prediction']['category']==r['label'] for r in results),'ood_count':len(ood),'ood_abstained':sum(r['prediction']['abstained'] for r in unknown),'results':results,'out_of_domain':unknown,'data_sha256':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in (p/'model_data').glob('*.json')},'limits':'Hand-authored small synthetic benchmark, same author/domain vocabulary. Not an independent experimental evaluation; lexical/template-family overlap is not excluded. Development fixtures informed stopword/domain guards; final heldout files were created after those choices. Scores are uncalibrated, not correctness probabilities. No general accuracy or OOD guarantee.'}
output=p/'evidence/local-ml-benchmark.json'
output.parent.mkdir(parents=True,exist_ok=True)
output.write_text(json.dumps(report,indent=2)+'\n')
print({k:report[k] for k in ['training_count','heldout_count','correct','ood_count','ood_abstained']})
