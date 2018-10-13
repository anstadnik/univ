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

