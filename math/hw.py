from univ_statistics import info, relations
from data import dir_met, indir_met
from sklearn import linear_model

import matplotlib.pyplot as plt

dir_keys = ["LOC", "NOM", "NOP", "HDD", "HIT"]
indir_keys = ["CC", "CDISP", "CINT", "WMC", "ATFD"]


def disp_hists():
    """Displays histograms of data
    :returns: TODO

    """
    fig_dir, ax = plt.subplots(3, 2, figsize=(10, 10))
    fig_dir.canvas.set_window_title("Direct metrics")

    for i, key in enumerate(dir_keys):
        ax[i % 3][i // 3].hist(dir_met[key])
        ax[i % 3][i // 3].set_title(key)

    plt.tight_layout()
    fig_dir.show()
    plt.waitforbuttonpress()
    plt.close()

    fig_indir, ax = plt.subplots(3, 2, figsize=(12, 8))
    fig_indir.canvas.set_window_title("Indirect metrics")
    for i, key in enumerate(indir_keys):
        ax[i % 3][i // 3].hist(indir_met[key])
        ax[i % 3][i // 3].set_title(key)

    plt.tight_layout()
    fig_indir.show()
    plt.waitforbuttonpress()
    plt.close()


def disp_stat_data():
    """Displays various info for metrics
    :returns: TODO

    """
    print("Direct metrics")
    for key in dir_keys:
        stat = info(dir_met[key].copy())
        print()
        print("  Key:", key)
        print("    Mean:", round(stat["mean"], 3), "Var", round(stat["var"], 3))
        mu3 = info([(x - stat["mean"]) ** 3 for x in dir_met[key]])["mean"]
        mu4 = info([(x - stat["mean"]) ** 4 for x in dir_met[key]])["mean"]
        print("    Skewness:", round(mu3/(stat["std"] ** 3), 3),
              "Kurtosis", round(mu4/(stat["std"] ** 4), 3))

    print()
    print()
    print("Indirect metrics")
    for key in indir_keys:
        stat = info(indir_met[key].copy())
        print()
        print("  Key:", key)
        print("    Mean:", round(stat["mean"], 3), "Var", round(stat["var"], 3))
        mu3 = info([(x - stat["mean"]) ** 3 for x in indir_met[key]])["mean"]
        mu4 = info([(x - stat["mean"]) ** 4 for x in indir_met[key]])["mean"]
        print("    Skewness:", round(mu3/(stat["std"] ** 3), 3),
              "Kurtosis", round(mu4/(stat["std"] ** 4), 3))


def part1():
    disp_hists()
    disp_stat_data()


def display_correlation():
    keys = dir_keys + indir_keys
    met = {**dir_met, **indir_met}
    fig_dir, ax = plt.subplots(len(keys), len(keys), figsize=(10, 10))
    fig_dir.canvas.set_window_title("Spearman correlation")
    for i, key1 in enumerate(keys):
        for j, key2 in enumerate(keys):
            ax[(i, j)].axis('off')
            if key1 == key2:
                ax[(i, j)].text(0.3, 0.5, key1, fontsize=20, ha='center',
                                va='center', color="red")
            else:
                coef = round(relations(met[key1], met[key2])["coefS"], 3)
                if abs(coef) > 0.4:
                    ax[(i, j)].text(0.3, 0.5, coef, fontsize=20, ha='center',
                                    va='center', color="green")
                else:
                    ax[(i, j)].text(0.3, 0.5, coef, fontsize=15, ha='center',
                                    va='center')

    plt.tight_layout()
    fig_dir.show()
    plt.waitforbuttonpress()
    plt.close()


def display_regression():
    keys = [
        ["LOC", "NOM"],
        ["LOC", "HIT"],
        ["LOC", "ATFD"],
        ["NOM", "HIT"],
        ["NOP", "WMC"]
    ]
    met = {**dir_met, **indir_met}
    fig_dir, ax = plt.subplots(3, 2, figsize=(10, 10))
    fig_dir.canvas.set_window_title("Spearman correlation")
    for i, k in enumerate(keys):
        key1, key2 = k
        vals1 = met[key1]
        stat1 = info(vals1)
        vals1 = [(val - stat1["mean"]) / stat1["std"] for val in vals1]
        vals2 = met[key2]
        stat2 = info(vals1)
        vals2 = [(val - stat2["mean"]) / stat2["std"] for val in vals2]
        ax[i % 3][i // 3].scatter(range(len(vals1)), vals1, label=key1)
        ax[i % 3][i // 3].scatter(range(len(vals2)), vals2, label=key2)
        ax[i % 3][i // 3].legend()
        m1, k1 = relations(vals1, range(len(vals1)))["lsq"]
        m2, k2 = relations(vals2, range(len(vals2)))["lsq"]
        ax[i % 3][i // 3].plot([m1 * x + k1 for x in range(-1, 3)], range(-1,
                                                                          3))
        ax[i % 3][i // 3].plot([m2 * x + k2 for x in range(-1, 3)], range(-1,
                                                                          3))
    plt.tight_layout()
    fig_dir.show()
    plt.waitforbuttonpress()
    plt.close()


def part2():
    display_correlation()
    display_regression()


def part3():
    """Trying to make more features
    :returns: TODO

    """
    keys = [
        ["LOC", "NOM"],
        ["LOC", "HIT"],
        ["LOC", "ATFD"],
        ["NOM", "HIT"],
        ["NOP", "WMC"]
    ]
    met = {**dir_met, **indir_met}
    fig_dir, ax = plt.subplots(3, 2, figsize=(10, 10))
    fig_dir.canvas.set_window_title("Spearman correlation")
    for i, k in enumerate(keys):
        key1, key2 = k
        vals1 = met[key1]
        stat1 = info(vals1)
        vals1 = [(val - stat1["mean"]) / stat1["std"] for val in vals1]
        vals2 = met[key2]
        stat2 = info(vals1)
        vals2 = [(val - stat2["mean"]) / stat2["std"] for val in vals2]
        ax[i % 3][i // 3].scatter(range(len(vals1)), vals1, label=key1)
        ax[i % 3][i // 3].scatter(range(len(vals2)), vals2, label=key2)
        ax[i % 3][i // 3].legend()
        features = [[x, x ** 2, x ** 3] for x in range(len(vals1))]
        regr1 = linear_model.LinearRegression()
        regr1.fit(features, vals1)
        pred1 = [regr1.predict([[x, x ** 2, x ** 3]]) for x in
                 range(len(vals1))]
        regr2 = linear_model.LinearRegression()
        regr2.fit(features, vals2)
        pred2 = [regr2.predict([[x, x ** 2, x ** 3]]) for x in
                 range(len(vals2))]
        m1, k1 = relations(vals1, range(len(vals1)))["lsq"]
        m2, k2 = relations(vals2, range(len(vals2)))["lsq"]
        ax[i % 3][i // 3].plot(range(len(vals1)), pred1)
        ax[i % 3][i // 3].plot(range(len(vals2)), pred2)

    plt.tight_layout()
    fig_dir.show()
    plt.waitforbuttonpress()
    plt.close()


def main():
    part1()
    part2()
    part3()


if __name__ == "__main__":
    main()
