import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.neighbors import KNeighborsClassifier

df = pd.read_csv("links.tsv", sep='\t')
df['Link Correto'] = df['Link Correto'].replace(['x'], 1)
df['Link Correto'].fillna(0, inplace=True)

df.loc[:, "consegui_html"] = None

df.loc[:, "plurianual"] = 0
df.loc[:, "despesas"] = 0
df.loc[:, "receitas"] = 0
df.loc[:, "servidores"] = 0
df.loc[:, "orçamentária"] = 0
df.loc[:, "licitações"] = 0
df.loc[:, "contratos"] = 0
df.loc[:, "inexigibilidade"] = 0
df.loc[:, "dispensa"] = 0
df.loc[:, "concurso"] = 0
df.loc[:, "contas públicas"] = 0
df.loc[:, "obras públicas"] = 0
df.loc[:, "portal da transparência"] = 0
df.loc[:, "transparência"] = 0

targets_for_text = ['plurianual', 'despesas', 'receitas', 'servidores', 'orçamentária', 'licitações', 'contratos', 'inexigibilidade',
                    'dispensa', 'concurso', 'contas públicas', 'obras públicas', 'portal da transparência', 'transparência']
targets = '|'.join(targets_for_text)

def pontuar_texto(text):
    find = re.findall(targets, text)
    return (find)

def pontuar_os_municipios():

    count = 0
    for municipio in df.loc[:, 'Município']:
        name = 'portais/' + str(count) + '.html'
        try:
            with open(name, 'r') as arq:
                page = arq.read()
                text = BeautifulSoup(page, "html5lib").get_text().lower()
                if len(text) < 300:
                    df.loc[count, "consegui_html"] = 0
                else: 
                    df.loc[count, "consegui_html"] = 1

                portal_estadual = re.findall('portaltransparencia.gov.br', df.loc[count, 'Portal da Transparência'])
                if portal_estadual:
                    df.loc[count, "consegui_html"] = None

                find_targets = pontuar_texto(text)
                for palavra in find_targets:
                    df.loc[count, palavra] += 1
            count += 1
        except:
            count += 1
            continue



def Decision_Tree_Classification(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.8, random_state = 0)
    classifier = DecisionTreeClassifier(criterion = 'gini', random_state = 0, min_samples_leaf = 5)
    classifier.fit(X_train, y_train.ravel())
    y_pred = classifier.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    print(cm)

    ac = accuracy_score(y_test, y_pred)

    print('Dec. Tree Class.: ', ac)

    fn=['consegui_html','plurianual','despesas','receitas','servidores','orçamentária','licitações','contratos',
        'inexigibilidade','dispensa','concurso','contas públicas','obras públicas','portal da transparência','transparência']
    fig, axes = plt.subplots(nrows = 1,ncols = 1,figsize = (4,4), dpi=500)
    plot_tree(classifier,
            filled = True,
            feature_names=fn);
    fig.savefig('imagename.png')
    data = df
    data = data.drop(columns=['Site Prefeitura', 'Site Camara', 'Desenvolvedores', 'Portal da Transparência', 'Url do Link Correto'])
    data = data.dropna(subset=['consegui_html'])
    z_pred = classifier.predict(data.iloc[ :, 2:].values)
    print (z_pred.tolist().count(1))


def classificar(dataset):

    X = dataset.iloc[:, 2:].values
    y = dataset.iloc[:, 1:2].values
    dataset.to_csv("data.csv", index = False)

    Decision_Tree_Classification(X,y)   


def main():
    pontuar_os_municipios()
    dataset = df.loc[ : 301, :]

    dataset = dataset.drop(columns=['Site Prefeitura', 'Site Camara', 'Desenvolvedores', 'Portal da Transparência', 'Url do Link Correto'])
    dataset = dataset.dropna(subset=['consegui_html'])

    classificar(dataset)

main()
