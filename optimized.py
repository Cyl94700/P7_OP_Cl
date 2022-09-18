import csv
import time
from itertools import combinations

start_time = time.time()

MAX_INVEST = 500


def main():
    stocks_list = read_csv()

    print("\n        AlgoInvest&Trade")
    print(f"\nCalcul du meilleur portefeuille client parmi {len(stocks_list)} actions pour un seuil de {MAX_INVEST}€ "
          f":")
    print("\n")

    best_combination = stocks_portfolio(stocks_list)
    display_results(best_combination)


def read_csv():
    """Importe les données actions depuis le fichier dataset.csv
    @return: stock_list : liste des 20 actions possibles (nom, valeur en euros, rentabilité à 2 ans en %)
    """
    with open("data/dataset1.csv") as csvfile:
        stocks_file = csv.reader(csvfile, delimiter=',')

        stocks_list = []
        for row in stocks_file:
            stocks_list.append(
                (row[0], float(row[1]), float(row[2]))
            )

        return stocks_list


def stocks_portfolio(stocks_list):
    """Détermine toutes les combinaisons possibles d'actions
    Vérifie si la combinaison ne dépasse pas le plafond des 500 €
    Retient la meilleure combinaison possible en rentabilité

    @param stocks_list : liste des données actions
    @return : meilleure combinaison en rentabilité (liste)
    """
    profit = 0
    best_combination = []
    z = 0
    for i in range(len(stocks_list)):
        y = 0
        stocks_combinations = combinations(stocks_list, i+1)
        # print(len(list(stocks_combinations)))

        for stocks_combination in stocks_combinations:
            total_cost = combination_value(stocks_combination)
            z += 1
            y += 1

            if total_cost <= MAX_INVEST:
                total_profit = profit_value(stocks_combination)

                if total_profit > profit:
                    profit = total_profit
                    best_combination = stocks_combination
        print(str(y), "combinaisons pour " + str(i + 1), "action(s)")
    print("\n" + str(z), "combinaisons parcourues")

    return best_combination


def combination_value(stocks_combination):
    """Valeur en euros de la combinaison d'actions courantes

    @param stocks_combination : liste de la combinaison courante d'actions
    @return: sum prices (int)
    """
    prices = []
    for element in stocks_combination:
        prices.append(element[1])

    return sum(prices)


def profit_value(stock_combination):
    """Valeur en % de la combinaison courante

    @param stock_combination : liste des actions de la combinaison courante
    @return: sum profits (float) en %
    """
    profits = []
    for element in stock_combination:
        profits.append(element[1] * element[2] / 100)

    return sum(profits)


def display_results(best_combinations):
    """
    Affiche la meilleure combinaison d'actions, son coût, son rendement en € après 2 ans et le temps consommé
    en secondes.
    @param best_combinations : combinaison d'actions la plus rentable (liste)
    """
    print(f"\nMeilleur investissement ({len(best_combinations)} actions) :\n")

    for item in best_combinations:
        print(f"{item[0]} | {item[1]} € | +{item[2]} %")

    print("\nCoût du portefeuille : ", combination_value(best_combinations), "€")
    print("Rendement après 2 ans : +", profit_value(best_combinations), "€")
    print("\nTemps comsommé : ", time.time() - start_time, "secondes")


if __name__ == "__main__":
    main()
