import numpy as np
import math
import scipy.stats as st

# nums = [8, 9, 12, 13, 16, 17, 18, 20, 22, 30, 31, 40]

def percentile(arg: np.array, n):
    """Counts a n-th percentile"""
    if np.isscalar(n):
        pos = (n / 100) * (len(arg) + 1)
        frac, whole = math.modf(pos)
        whole = max(0, int(whole - 1))
        return arg[whole] + frac * (arg[whole + 1] - arg[whole])
    return [percentile(arg, val) for val in n]


def info(nums):
    """Returns useful info for an array"""
    if type(nums) == list:
        nums = np.array(nums)
    nums.sort()
    data = {}
    data["nums"] = nums
    data["len"] = len(nums)
    data["mean"] = nums.mean()
    data["median"] = np.median(nums)
    data["mode"], _ = st.mode(nums)
    data["variance"] = nums.var(ddof=1)
    data["std"] = nums.std(ddof=1)
    data["quartiles"] = percentile(nums, np.arange(25, 100, 25))
    for key, value in data.items():
        print(key, "=", value)
    return data


# info(nums)
