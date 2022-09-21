import csv
import time

start_time = time.time()

MAX_INVEST = 500


def main():
    stocks_list = read_csv()

    print("\n        AlgoInvest&Trade")
    print(f"\nCalcul du meilleur portefeuille client parmi {len(stocks_list)} actions pour un seuil de" 
          f" {MAX_INVEST}€ "
          f":")
    print("\n")

    best_combination = stocks_portfolio(stocks_list)
    display_results(best_combination)


def read_csv():
    """Importe les données actions depuis le fichier dataset.csv
    @return: stock_list : liste des 20 actions possibles (nom, valeur en euros, rentabilité à 2 ans en %)
    """
    with open("data/dataset.csv") as csvfile:
        stocks_file = csv.reader(csvfile, delimiter=',')

        stocks_list = []
        for row in stocks_file:
            stock = (
                row[0],
                int(row[1]),
                int(row[1]) * int(row[2]) / 100
            )
            stocks_list.append(stock)

        return stocks_list


def stocks_portfolio(stocks_list):
    """
    Fonction dynamique
    Initialise la matrice (matrix)
    Construit le meilleur profit possible
    @param stocks_list : liste d'actions
    @return : Meilleure combinaison possible (liste)
    """
    max_inv = MAX_INVEST   # capacity
    stocks_total = len(stocks_list)
    cost = []       # prix
    profit = []     # profit

    for stock in stocks_list:
        cost.append(stock[1])
        profit.append(stock[2])

    # Initialisation matrice et récupération du meilleur profit
    matrix = [[0 for w in range(max_inv + 1)] for i in range(stocks_total + 1)]
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
        print(f"{item[0]} | {item[1]} € | +{item[2]} %")

        cost.append(item[1])
        profit.append(item[2])

    print("\nCoût du portefeuille : ", sum(cost), "€")
    print("Rendement après 2 ans : +", sum(profit), "€")
    print("\nTemps comsommé : ", time.time() - start_time, "seconde(s)")


if __name__ == "__main__":
    main()
