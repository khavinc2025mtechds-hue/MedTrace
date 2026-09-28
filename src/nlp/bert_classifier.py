"""Runnable RoBERTa/BERT training. Requires curated labels and downloaded weights."""
import argparse,json
import numpy as np
from config.settings import path
from src.evaluation.splits import labeled_split

def train(csv_path,model_name='roberta-base',epochs=2,cutoff=None):
    import torch
    from transformers import AutoTokenizer,AutoModelForSequenceClassification,TrainingArguments,Trainer,set_seed
    from sklearn.metrics import classification_report,confusion_matrix
    set_seed(42);tr,te=labeled_split(csv_path,cutoff);labels=sorted(tr.label.unique());mapping={x:i for i,x in enumerate(labels)}
    tokenizer=AutoTokenizer.from_pretrained(model_name)
    class Dataset(torch.utils.data.Dataset):
        def __init__(self,df):self.df=df.reset_index(drop=True)
        def __len__(self):return len(self.df)
        def __getitem__(self,i):
            r=self.df.iloc[i];enc=tokenizer(r.narrative,truncation=True,padding='max_length',max_length=256,return_tensors='pt');out={k:v.squeeze(0) for k,v in enc.items()};out['labels']=torch.tensor(mapping[r.label]);return out
    model=AutoModelForSequenceClassification.from_pretrained(model_name,num_labels=len(labels),id2label=dict(enumerate(labels)),label2id=mapping)
    out=path('models/classifiers/transformer');out.mkdir(parents=True,exist_ok=True)
    args=TrainingArguments(output_dir=str(out),num_train_epochs=epochs,per_device_train_batch_size=4,per_device_eval_batch_size=8,gradient_accumulation_steps=4,learning_rate=2e-5,save_strategy='no',report_to=[],seed=42)
    trainer=Trainer(model=model,args=args,train_dataset=Dataset(tr));trainer.train();pred=np.argmax(trainer.predict(Dataset(te)).predictions,axis=1);truth=[mapping[x] for x in te.label]
    metrics=classification_report(truth,pred,labels=list(range(len(labels))),target_names=labels,output_dict=True,zero_division=0);metrics['confusion_matrix']=confusion_matrix(truth,pred,labels=list(range(len(labels)))).tolist();metrics['model']=model_name;metrics['train_rows']=len(tr);metrics['test_rows']=len(te)
    trainer.save_model(str(out));tokenizer.save_pretrained(str(out));path('reports/evaluation/transformer_metrics.json').write_text(json.dumps(metrics,indent=2));return metrics
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('csv');p.add_argument('--model',default='roberta-base');p.add_argument('--epochs',type=int,default=2);p.add_argument('--cutoff');a=p.parse_args();print(train(a.csv,a.model,a.epochs,a.cutoff))
