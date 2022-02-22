from random import randrange
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix


def manhattan_distance(a, b):
    return np.array(list(map(np.sum, np.array(list(map(np.abs, a - b))))))


# 1. UCITAVANJE PODATAKA, PRIKAZ PRVIH I POSLEDNJIH 5 REDOVA - PROBLEM STATEMENT AND READ DATA
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', None)
data = pd.read_csv('datasets/car_state.csv')
data.insert(loc=0, column='ID', value=np.arange(0, len(data), 1))
print("\nPrvih 5 redova u tabeli:")
print(data.head())
print("\nPoslednjih 5 redova u tabeli:")
print(data.tail())

# 2. DATA ANALYSIS - INFORMACIJE O SADRZAJU TABELE
print("\nOsnovne informacije o kolonama:")
print(data.info())
print("\nKoncizne informacije o jedinoj numerickoj koloni (ID):")
print(data.describe())
print("\nKoncizne informacije o nenumerickim kolonama:")
print(data.describe(include=[object]))

# 5. IZVRSAVANJE DODATNIH TRANSFORMACIJA NAD PODACIMA TABELE
buying_price__maintenance_and_safety_dict = {'low': 1, 'medium': 2, 'high': 3, 'very high': 4}
trunk_size_dict = {'small': 1, 'medium': 2, 'big': 3}
doors_and_seats_dict = {'2': 2, '3': 3, '4': 4, '5 or more': 5}
data['buying_price'] = data['buying_price'].map(buying_price__maintenance_and_safety_dict)
data['maintenance'] = data['maintenance'].map(buying_price__maintenance_and_safety_dict)
data['doors'] = data['doors'].map(doors_and_seats_dict)
data['seats'] = data['seats'].map(doors_and_seats_dict)
data['trunk_size'] = data['trunk_size'].map(trunk_size_dict)
data['safety'] = data['safety'].map(buying_price__maintenance_and_safety_dict)
print("\nIspis prvih 10 redova nakon preslikavanja kolona u numericke vrednosti")
print(data.head(10))

# 3. GRAFICKI PRIKAZ
col_names = ['buying_price', 'maintenance', 'doors', 'seats', 'trunk_size', 'safety']
plt.ylabel('status', fontsize=10)
y = data['status']
for col in col_names:
    X = data.loc[:, [col]]
    plt.scatter(X, y, alpha=0.01, s=100, c='red', label='cars', edgecolors='black', marker='o', linewidths=1)
    title = 'Zavisnost ' + col + ' i statusa'
    plt.title(title)
    plt.xlabel(col, fontsize=10)
    plt.legend()
    plt.tight_layout()
    plt.show()

# 4. ODABIR ATRIBUTA KOJI UCESTVUJU U TRENIRANJU MODELA
# not useful features: ID
# useful features: buying_price, maintenance, doors, seats, trunk_size, safety
# labels: status
data_train = data.loc[:, ['buying_price', 'maintenance', 'doors', 'seats', 'trunk_size', 'safety']]  # DataFrame
labels = data.loc[:, 'status']  # Series

# 7. REALIZACIJA UGRADJENOG MODELA
# k = 10
k = np.sqrt(len(data)-1)
k = round(k)
if k % 2 == 0:
    k = k + 1
# print(k)

model = KNeighborsClassifier(n_neighbors=k)
X_train, X_test, y_train, y_test = train_test_split(data_train, labels, test_size=0.20, shuffle=False)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print("\nUgradjeni model:")
print("Matrica predikcija: ")
print(confusion_matrix(y_test, y_pred))
print("\nIzvestaj ugradjenog modela: ")
print(classification_report(y_test, y_pred))
ser_pred = pd.Series(data=y_pred, name='Predicted', index=X_test.index)
res_df = pd.concat([X_test, y_test, ser_pred], axis=1)
print("\nPrvih 5 redova test podataka (ugradjeni model): ")
print(res_df.head())
print('Model score: ', model.score(X_test, y_test))

# 6. SOPSTVENA IMPLEMENTACIJA KNN ALGORITMA
print("\n\nSopstvena implementacija:")
a = np.round(0.8 * len(data))
cnt_score = 0
cnt_miss = 0
predicted_arr = []
new_cars = data.loc[data['ID'] < a]
new_cars_test = new_cars.loc[:, ['buying_price', 'maintenance', 'doors', 'seats', 'trunk_size', 'safety']]  # DataFrame
new_cars_test_values = new_cars_test.values
for i in range(int(len(data) - a)):
    target_car = data.loc[data['ID'] == (a+i)]
    if i == 0:
        print("\nMatrica atributa za prvi test:")
        print(new_cars_test_values)
    target_car_test = target_car.loc[:, ['buying_price', 'maintenance', 'doors', 'seats', 'trunk_size', 'safety']]  # DataFrame
    target_car_test_values = target_car_test.values
    if i == 0:
        print("\nAtributi testiranog automobila", target_car_test_values)

    manhattan_distances = manhattan_distance(new_cars_test_values, target_car_test_values[0])
    if i == 0:
        print("Menhtetn distance za prvi test: ", manhattan_distances)
    new_cars_manh = new_cars.copy()
    new_cars_manh.insert(len(new_cars_manh.columns)-1, "manhattan_distance", manhattan_distances)
    new_cars_manh = new_cars_manh.sort_values(by=["manhattan_distance"])
    if i == 0:
        print("Tabela podataka sortirana po rastucoj menhetn distanci za prvi test:")
        print(new_cars_manh.head(10))

    manhattan_nearest_neighbor_status = new_cars_manh.status[:k]
    # print("\nStatusi najpribliznijih ", k, " automobila:")
    # print(manhattan_nearest_neighbor_status)
    # print(manhattan_nearest_neighbor_status.describe())
    answer = manhattan_nearest_neighbor_status.mode()
    predicted_arr.append(answer[0])
    if i == 0:
        print("\nNajcesci status kod najblizih ", k, " komsija: ", answer[0])
        print("Stvarni status testiranog automobila: ", target_car.at[a, 'status'])
        print(". . .")
    if answer[0] == target_car.at[a+i, 'status']:
        cnt_score += 1
        # print("\nPOGODAK!", answer[0], target_car.at[a+i, 'status'])
    else:
        cnt_miss += 1
        # print("\nMISS!", answer[0], target_car.at[a+i, 'status'])

ser_pred = pd.Series(data=predicted_arr, name='Predicted', index=X_test.index)
res_df = pd.concat([X_test, y_test, ser_pred], axis=1)
print("\nSopstvena implementacija: ")
print(res_df.head())
print("Num of good predictions: ", cnt_score)
print("Num of wrong predictions: ", cnt_miss)
print("Model score: ", cnt_score/(cnt_score+cnt_miss))


