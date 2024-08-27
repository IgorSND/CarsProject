import tensorflow as tf
from tensorflow import keras
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder, StandardScaler

df = pd.read_excel('D:\Imobiliaria\df_final.xlsx')
# Definindo as features e o target
features = ['vehicle_brand', 'vehicle_model', 'cartype', 'regdate',
            'mileage', 'motorpower', 'fuel', 'car_steering',
            'porta','fipe_preco']
target = 'price'
X = df[features]
y = df[target]

df['price'] = pd.to_numeric(df['price'])

# Dividir os dados em conjunto de treinamento, validação e teste
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.2, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# Pré-processamento dos dados
numeric_features = ['mileage', 'motorpower', 'regdate', 'porta','fipe_preco']
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])

categorical_features = ['vehicle_brand', 'vehicle_model', 'cartype', 'fuel', 'car_steering']
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

X_train_preprocessed = preprocessor.fit_transform(X_train).toarray()
X_val_preprocessed = preprocessor.transform(X_val).toarray()
X_test_preprocessed = preprocessor.transform(X_test).toarray()

# Construindo o modelo de rede neural
model = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=[X_train_preprocessed.shape[1]]),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(1)
])

# Compilando o modelo
model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# Treinando o modelo
history = model.fit(X_train_preprocessed, y_train, epochs=200, validation_data=(X_val_preprocessed, y_val), verbose=0)

# Fazendo previsões
y_pred = model.predict(X_test_preprocessed).flatten()

# Avaliando o desempenho do modelo
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("Erro quadrático médio (MSE):", mse)
print("RMSE:", rmse)
print("Coeficiente de determinação (R²):", r2)

# Calcular a diferença entre os valores previstos e reais 
diff = y_pred - y_test

# Criar DataFrame com informações dos carros no conjunto de teste
df_test = X_test.copy()
df_test['Valor_Real'] = y_test
df_test['Valor_Previsto'] = y_pred
df_test['Diferenca'] = diff
# Ordenar os carros com base na diferença calculada (do menor para o maior, alterar True ou False)
df_sorted = df_test.sort_values(by='Diferenca', ascending=True)

# Selecionar os cinco carros com as menores diferenças
#df_top_5 = df_sorted.head(5)

# Contar a ocorrência de cada carro selecionado no conjunto de teste
#recorrencias = df_sorted.head(100).groupby(['vehicle_brand', 'vehicle_model']).size().reset_index(name='Recorrencias')

# Criar DataFrame com as informações dos cinco carros selecionados e suas contagens
#top_5_with_count = pd.merge(df_top_5, recorrencias, on=['vehicle_brand', 'vehicle_model'], how='left')

# Exibir o DataFrame final
#print(top_5_with_count)

# Normalizar as variáveis 'price' e 'Valor_Previsto'
df_test['Valor_Real_norm'] = df_test['Valor_Real'] / df_test['Valor_Real'].max()
df_test['Valor_Previsto_norm'] = df_test['Valor_Previsto'] / df_test['Valor_Previsto'].max()

# Filtrar os carros cujos valores previstos pelo modelo são menores que os preços anunciados
carros_abaixo_do_preco_anunciado = df_test[df_test['Valor_Previsto_norm'] < df_test['Valor_Real_norm']]

# Exibir os carros abaixo do preço anunciado
print(carros_abaixo_do_preco_anunciado)
# na verdade precisa ver quando a diferença é negativa e comparar o valor previsto quando a diferença é negativa com o fipe_preco