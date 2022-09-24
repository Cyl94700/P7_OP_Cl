import csv
import time
import sys

start_time = time.time()

MAX_INVEST = 500
# récupération du csv saisi par l'utilisateur
try:
    filename = "data/" + sys.argv[1] + ".csv"
except IndexError:
    print("\nFichier non trouvé. Veuillez saisir un fichier existant.\n")
    time.sleep(1)
    sys.exit()


def main():
    """
        Vérifie le fichier csv passé en paramètre et lance le process
    """
    stocks_list = read_csv(filename)

    print("\n        AlgoInvest&Trade")
    print(f"\nCalcul du meilleur portefeuille client parmi {len(stocks_list)} actions pour un seuil de"
          f" {MAX_INVEST}€ "
          f":")

    best_combination = stocks_portfolio(stocks_list)
    display_results(best_combination)


def read_csv(filename):
    """
    Importe les données actions depuis les fichiers dataset, dataset1 ou dataset2 .csv
    @param : filename = nom csv saisi par l'utilisateur
    @return = stock_list : liste des 20 actions possibles (nom, valeur en euros, rentabilité à 2 ans en %)
    """
    with open(filename) as csvfile:
        stocks_file = csv.reader(csvfile, delimiter=',')
        if filename != "data/dataset.csv":
            next(csvfile)  # on ignore l'entête pour dataset1 et dataset2

        stocks_list = []
        for row in stocks_file:
            if float(row[1]) <= 0 or float(row[2]) <= 0:
                pass
            else:
                if filename != "data/dataset.csv":
                    stock = (
                        row[0],
                        int(float(row[1]) * 100),
                        float(float(row[1]) * float(row[2]) / 100)
                    )
                else:
                    stock = (
                        row[0],
                        int(row[1]),
                        int(row[1]) * int(row[2]) / 100
                    )
                stocks_list.append(stock)

        return stocks_list


def stocks_portfolio(stocks_list):
    """Fonction dynamique
    Initialise la matrice (matrix)
    Construit le meilleur profit possible
    Lecture inverse pour recupérer les actions
    @param stocks_list : liste d'actions
    @return = best_combination : Meilleure combinaison possible (liste)
    """
    if filename != "data/dataset.csv":
        max_inv = int(MAX_INVEST * 100)   # capacity
    else:
        max_inv = MAX_INVEST
    stocks_total = len(stocks_list)
    cost = []       # weights
    profit = []     # values

    for stock in stocks_list:
        cost.append(stock[1])
        profit.append(stock[2])

    # Initialisation matrice et récupération du meilleur rendement
    matrix = [[0 for x in range(max_inv + 1)] for x in range(stocks_total + 1)]
    z = 0
    for i in range(1, stocks_total + 1):
        for w in range(1, max_inv + 1):
            z += 1
            if cost[i-1] <= w:
                matrix[i][w] = max(profit[i-1] + matrix[i-1][w-cost[i-1]], matrix[i-1][w])
            else:
                matrix[i][w] = matrix[i-1][w]

    # Recherche de la meilleure combinaison complète (lecture inverse)
    best_combination = []
    y = 0
    while max_inv >= 0 and stocks_total >= 0:
        y += 1
        if matrix[stocks_total][max_inv] == \
                matrix[stocks_total-1][max_inv - cost[stocks_total-1]] + profit[stocks_total-1]:

            best_combination.append(stocks_list[stocks_total-1])
            max_inv -= cost[stocks_total-1]

        stocks_total -= 1
    iterations = z + y
    print("nombre de lignes lues  :", iterations)
    return best_combination


def display_results(best_combinations):
    """
    Affiche la meilleure combinaison d'actions, son coût, son rendement en € après 2 ans et le temps consommé
    en secondes.
    @param best_combinations : combinaison d'actions la plus rentable (liste)
    """
    print(f"\nMeilleur investissement ({len(best_combinations)} actions) :\n")
    cost = []
    profit = []

    for item in best_combinations:
        if filename != "data/dataset.csv":
            print(f"{item[0]} | {item[1] / 100} € | +{item[2]} %")
            cost.append(item[1] / 100)
            profit.append(item[2])
        else:
            print(f"{item[0]} | {item[1]} € | +{item[2]} %")
            cost.append(item[1])
            profit.append(item[2])

    print("\nCoût du portefeuille : ", sum(cost), "€")
    print("Rendement après 2 ans : +", sum(profit), "€")
    print("\nTemps consommé : ", time.time() - start_time, "seconde(s)")


if __name__ == "__main__":
    main()
