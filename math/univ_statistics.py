import math

def _mean(arg: list):
    return sum(arg)/len(arg)

def _median(arg: list):
    if len(arg) % 2:
        ind = (len(arg) + 1) // 2
        return arg[ind - 1]
    ind1, ind2 = (len(arg) // 2), len(arg) // 2 + 1
    return (arg[ind1 - 1] + arg[ind2 - 1]) / 2

# TODO make it work with small lists
def _percentile(arg: list, n):
    if type(n) == list:
        return [_percentile(arg, val) for val in n]
    pos = (n / 100) * (len(arg) + 1)
    frac, whole = math.modf(pos)
    whole = max(0, int(whole - 1))
    return arg[whole] + frac * (arg[whole + 1] - arg[whole])

def _mode(arg: list):
    occurs = {}
    maximum = 0
    for item in arg:
        if item in occurs:
            occurs[item] += 1
            if occurs[item] > maximum:
                maximum = occurs[item]
        else:
            occurs[item] = 0
    if maximum == 0:
        return []
    ret = []
    for key in occurs:
        if occurs[key] == maximum:
            ret.append(key)
    return ret

def _var(arg: list, ddof = 0):
    m = _mean(arg)
    return sum([(item - m) ** 2 for item in arg]) / (len(arg) - ddof)

def _std(arg: list, ddof = 0):
    return math.sqrt(_var(arg, ddof))

def info(nums: list):
    """Returns useful info for an array

    Args:
        nums: list of numbers

    Returns:
        Dictionary with such fields:
            nums
            len
            range
            mean
            median
            mode
            var: variance
            std: standart deviation
            quartiles: values for [0, 25, 50, 75, 100] quartiles"""
    if len(nums) < 4:
        raise RuntimeError("Too few elements")
    nums.sort()
    data = {}
    data["nums"] = nums
    data["len"] = len(nums)
    data["range"] = max(nums) - min(nums)
    data["mean"] = _mean(nums)
    data["median"] = _median(nums)
    data["mode"] = _mode(nums)
    data["var"] = _var(nums, ddof = 0)
    data["std"] = _std(nums, ddof = 0)
    data["var_of_sample"] = _var(nums, ddof = 1)
    data["std_of_sample"] = _std(nums, ddof = 1)
    data["quartiles"] = _percentile(nums, [25, 50, 75])
    for key, value in data.items():
        print(key, "=", value)
    return data

def _cov(x: list, y: list):
    """Calculates the covariance

    :x: list: TODO
    :y: list: TODO
    :returns: TODO

    """
    mX, mY = _mean(x), _mean(y)
    assert len(x) == len(y)
    return (1 / len(x)) * sum([(x_i - mX) * (y_i - mY) for x_i, y_i in zip(x, y)])

def least_squares(x: list, y: list):
    """Returns parameters for least squares

    :x: list: TODO
    :y: list: TODO
    :returns: TODO

    """
    m = _cov(x, y) / _var(x)
    k = _mean(y) - m * _mean(x)
    return m, k
def _coef_Det(x: list, y: list):
    """Returns coefficient of determination

    :x: list: TODO
    :y: list: TODO
    :returns: TODO

    """
    m, k = least_squares(x, y)
    y_ = list(map(lambda x: m * x + k, x))
    mY = _mean(y)
    sub_mean = sum([(yi - mY) ** 2 for yi in y])
    sub_approx = sum([(yi - y_i) ** 2 for yi, y_i in map(y, y_)])
    return 1 - sub_approx / sub_mean
# def coef_Exp(x: list, y: list):
#     """Returns parameters for exponential relationship

#     :x: list: TODO
#     :y: list: TODO
#     :returns: TODO

#     """

def _coef_Pearson(x: list, y: list):
    """Returns Pearson's coefficient

    :x: list: TODO
    :y: list: TODO
    :returns: TODO

    """
    return _cov(x, y) / (_std(x) * _std(y))
def _coef_Spear(x: list, y: list):
    """Returns Spearman's coefficiend

    :x: list: TODO
    :y: list: TODO
    :returns: TODO

    """
    sorted_x = sorted(x)
    rX = [sorted_x.index(v) for v in x]
    sorted_y = sorted(y)
    rY = [sorted_y.indey(v) for v in y]
    return _coef_Pearson(rX, rY)
def relations(x: list, y: list):
    """Calculates different kinds of relations and coefficients

    :x:list: TODO
    :y:list: TODO
    :returns: TODO

    """
    data = {}
    data["cov"] = _cov(x, y)
    data["lsq"] = least_squares(x, y)
    data["coefP"] = _coef_Pearson(x, y)
    # data["coefExp"] = _coef_Exp(x, y)
    # data["coefPow"] = _coef_Pow(x, y)
    data["coefDet"] = _coef_Det(x, y)
    data["coefS"] = _coef_Spear(x, y)
