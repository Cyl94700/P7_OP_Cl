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
         Lecture du csv passé en paramètre et lancement du calcul
    """
    stocks_list = read_csv(filename)

    print("\n        AlgoInvest&Trade")
    print(f"\nCalcul du meilleur portefeuille client parmi {len(stocks_list)} actions pour un seuil de"
          f" {MAX_INVEST}€ "
          f":")

    best_combination = greedy(stocks_list)
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
                        float(row[1]),
                        float(row[2]),
                        float(float(row[1]) * float(row[2]) / 100)
                    )
                else:
                    stock = (
                        row[0],
                        int(row[1]),
                        int(row[2]),
                        float(int(row[1]) * int(row[2]) / 100)
                    )
                stocks_list.append(stock)

        return stocks_list


def greedy(stocks_list):
    """
    Algorithme glouton qui cumule systématiquement la meilleure action en rentablité en approche descendante
    jusqu'à atteindre ou ne pas dépasser le plafond d'investissement
    Retourne la meilleure combinaison de rendement (stocks_selected)
    Pour N = nombre d'actions
    Complexité temporelle : O(NlogN) en raison du tri "sorted" préalable puis O(n)
    Complexité spatiale : O(N), uses "1D" lists.
    """
    stocks_selected = []
    cost = 0
    # tri de la liste d'action du taux de rendement le plus élevé au moins élevé
    stocks_sorted = sorted(stocks_list, key=lambda x: x[2], reverse=True)
    # Boucle de lecture de la liste stocks_sorted
    for stock in stocks_sorted:
        # Verification si seuil atteint pour sortir de la boucle
        if cost == MAX_INVEST:
            break
        # Vérification du seuil de dépassement
        elif (cost + stock[1]) <= MAX_INVEST:
            cost += stock[1]
            stocks_selected.append(stock)

    return stocks_selected


def display_results(best_combinations):
    """
    Affiche la meilleure combinaison d'actions, son coût, son rendement en € après 2 ans et le temps consommé
    en secondes.
    @param best_combinations : combinaison d'actions la plus rentable (tuple)
    """
    print(f"\nMeilleur investissement ({len(best_combinations)} actions) :\n")
    cost = []
    profit = []
    for item in best_combinations:
        print(f"{item[0]} | {item[1]} € | +{item[2]} %")
        cost.append(item[1])
        profit.append(item[3])

    print("\nCoût du portefeuille : ", sum(cost), "€")
    print("Rendement après 2 ans : +", sum(profit), "€")
    print("\nTemps comsommé : ", time.time() - start_time, "seconde(s)")


if __name__ == "__main__":
    main()
