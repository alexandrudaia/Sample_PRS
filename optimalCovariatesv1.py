#!/usr/bin/env python
# coding: utf-8

# In[360]:


import numpy as np
import pandas as pd
import random
def create_individual():
    """creates individual constructed with covariates"""
    param ={ 
        
     
        'Smoking_status' :np.random.choice([0,1,2]),
        'Duration_of_moderate_activity':np.random.choice([0,15,20,30,40,60,90,120]),
        'Vigorous_exercise_p_week':np.random.choice([0,15,20,30,40,60,90]),
        'Tea_intake':np.random.choice(list(range(12))),
        'Vitamin_D':np.random.choice([0,1]),
        'Alcohol_freq':np.random.choice([0,1,2,3,4,5,6]),
        'Exercise_p_week':np.random.choice([0,1,2,3,4,5,6,7]),
        'Smokers_in_household':np.random.choice([0,1,2])
        
            
           }
    
    return pd.DataFrame.from_dict(param,orient='index').T

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score , f1_score 

def PRS_fitness(model ,individual,pacent):
    param=individual#created a individual with  random params 
    #model is an allready trained Logistic Regression Model that will be loaded 
    pacent=pacent.reset_index()
    pacent=pacent.drop('index',axis=1)
    pacent[param.columns]=param
    scaler = load('scalerv1.joblib')
    pacent[['Age', 'BMI','Vitamin_D','Alcohol_freq']] = scaler.transform(pacent[['Age', 'BMI','Vitamin_D','Alcohol_freq']])
    
    
    
    
    pred=model.predict_proba(pacent)[:,1]
    return pred[0]

def crossover(mother , father):
     
    cross=random.sample(list(mother.columns),2)
    mother[cross]=father[cross]
    cross=random.sample(list(father.columns),2)
    father[cross]=mother[cross]
    
       
     
        

    #here mutated params must be choosen randomly
    
    return  random.sample([mother,father],1)[0]


               
       


# In[89]:


import random
np.random.choice(list(range(100)))


# In[90]:


import pandas as pd
train=pd.read_csv('holdoutOptim.csv', low_memory=True)


# In[91]:


import joblib
from joblib import dump, load
 
model= load('modelOptimized0.joblib')


# In[92]:


scaler = load('scalerv1.joblib')


# In[180]:


pacent=pd.DataFrame(train.iloc[313]).T
pacent


# In[ ]:





# In[165]:


pacent[['Age', 'BMI','Vitamin_D','Alcohol_freq']] = scaler.transform(pacent[['Age', 'BMI','Vitamin_D','Alcohol_freq']])


# In[166]:


model.predict_proba(pacent)


# In[167]:


sample_covs=create_individual()


# In[168]:


sample_covs


# In[169]:


pacent=pacent.reset_index()


# In[170]:


pacent=pacent.drop('index',axis=1)


# In[171]:


pacent[sample_covs.columns]


# In[172]:


pacent[sample_covs.columns]=sample_covs


# In[173]:


pacent[sample_covs.columns]


# In[176]:


model.predict_proba(pacent)


# In[196]:


random.sample(list( sample_covs.columns),4)


# In[181]:


pacent


# In[333]:


individual1=create_individual()


# In[334]:


PRS_fitness(model ,individual1,pacent)


# In[335]:


individual2=create_individual()


# In[336]:


individual1


# In[337]:


individual2


# In[340]:


s=crossover(individual1,individual2)
s


# In[261]:


cross=random.sample(list(individual1.columns),4)
cross


# In[232]:


individual1[cross]=individual2[cross]
individual1


# In[ ]:





# In[259]:


crossover(individual1,individual2)


# In[344]:


initial_pop=[create_individual() for i in range(11)]


# In[347]:


initial_pop[:2]


# In[361]:


fits=[PRS_fitness(model,p,pacent) for p in initial_pop]


# In[362]:


fits


# In[363]:


import heapq


# In[364]:


heapq.nsmallest(3,fits)


# In[369]:


idx = np.argpartition(np.array(fits), 3)[:3]
idx


# In[368]:


idx


# In[367]:


gens=[initial_pop]


# In[430]:


class generation(object):
    def __init__(self,p):
        """here  the  class is initialized with initial(stone age population) . Meaning
        random   neural net arhitectures or  xgb"""
        self.gen=p
        self.perf=[]
    
    def fitness(self):
        for model_ in self.gen:
            b=PRS_fitness(model,model_,pacent)
           
            self.perf.append(b)
 
    


# In[ ]:





# In[442]:


n=100
stone_age=[create_individual() for i in range(n)]
 


# In[443]:


s


# In[444]:


g=generation(stone_age)
g.fitness()


# In[445]:


import heapq


# In[448]:


smallest_indices = heapq.nsmallest(20, range(len(g.perf)), key=g.perf.__getitem__)


# In[449]:


smallest_indices


# In[440]:


for  i in range(20,100):
    mother=np.random.choice(smallest_indices)
    father=np.random.choice(smallest_indices)
    child=crossover(mothe,fater)
    


# In[475]:


n=100
stone_age=[create_individual() for i in range(n)]
import warnings

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)


# In[476]:


import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")
fits=[PRS_fitness(model,p,pacent) for p in stone_age]


# In[477]:


smallest_indices = heapq.nsmallest(20, range(len(fits)), key=fits.__getitem__)
smallest_indices


# In[478]:


new_pop=[]
for s in smallest_indices:
    new_pop.append(stone_age[s])


# In[479]:


len(new_pop)


# In[480]:


for i in range(80):
    mother=np.random.choice(smallest_indices)
    father=np.random.choice(smallest_indices)
    child=crossover(stone_age[mother],stone_age[father])
    new_pop.append(child)


# In[481]:


fits=[PRS_fitness(model,p,pacent) for p in new_pop]


# In[482]:


fits


# In[483]:


smallest_indices = heapq.nsmallest(20, range(len(fits)), key=fits.__getitem__)
smallest_indices


# In[484]:


new_pop[7]


# In[486]:


PRS_fitness(model,new_pop[7],pacent)


# In[487]:


stone_age=new_pop


# In[488]:


#and this maybe in a repeat  while


# In[ ]:




