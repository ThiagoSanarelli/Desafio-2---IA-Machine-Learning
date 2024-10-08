# -*- coding: utf-8 -*-
"""Desafio 2 - Ia Machine Learning Dataset Heart.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1h6gGfWFPlf-GpDsqMGX08ikA5BkIJxZq
"""

# Importando as bibliotecas necessárias
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.utils import to_categorical

# Carregar o dataset de doenças cardíacas
url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data'
colunas = ['idade', 'sexo', 'tipo_dor_peito', 'pressao_sanguinea_repouso', 'colesterol', 'acucar_sangue_jejum', 
           'resultado_eletrocardiografico', 'frequencia_cardiaca_maxima', 'angina_exercicio', 'depressao_st', 
           'inclinação_st', 'vasos_cardiacos', 'talassemia', 'diagnostico_doenca_cardiaca']
dados = pd.read_csv(url, names=colunas)

# Exibir as primeiras linhas do dataset
print(dados.head())

# Tratar valores ausentes, se houver
dados.replace('?', np.nan, inplace=True)
dados.dropna(inplace=True)

# Separar variáveis independentes (X) e alvo (y)
X = dados.drop('diagnostico_doenca_cardiaca', axis=1)
y = dados['diagnostico_doenca_cardiaca']

# Padronizar os dados
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Dividir em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convertendo o alvo (y) para formato categórico (one-hot encoding)
y_train_cat = to_categorical(y_train)
y_test_cat = to_categorical(y_test)

# Criando o modelo de rede neural
model = Sequential()

# Adicionando a camada de entrada
model.add(Input(shape=(X_train.shape[1],)))

# Adicionando camadas ocultas
model.add(Dense(64, activation='relu'))  # Primeira camada oculta
model.add(Dense(32, activation='relu'))  # Segunda camada oculta
model.add(Dense(y_train_cat.shape[1], activation='softmax'))  # Camada de saída (softmax para classificação multiclasses)

# Compilando o modelo
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Treinando o modelo
model.fit(X_train, y_train_cat, epochs=100, batch_size=10, validation_split=0.2)

# Avaliando o modelo no conjunto de teste
test_loss, test_acc = model.evaluate(X_test, y_test_cat)

# Previsão no conjunto de teste
y_pred = model.predict(X_test)
y_pred_classes = np.argmax(y_pred, axis=1)
y_test_classes = np.argmax(y_test_cat, axis=1)

# Exibindo a acurácia e relatório de classificação
print(f"Acurácia da Rede Neural: {test_acc}")
print(classification_report(y_test_classes, y_pred_classes))
