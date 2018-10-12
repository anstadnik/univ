from univ_statistics import info
import unittest
import random

class Test_info(unittest.TestCase):
    def test_nums(self):
        nums = random.sample(range(100), 10)
        data = info(nums)
        self.assertCountEqual(nums, data["nums"])

    def test_len(self):
        nums = random.sample(range(100), random.randint(4, 10))
        data = info(nums)
        self.assertEqual(len(nums), data["len"])

    def test_range(self):
        nums = list(range(2, 24))
        data = info(nums)
        self.assertEqual(21, data["range"])

    def test_mean(self):
        nums = [23, 22, 24, 24, 23, 20, 25]
        data = info(nums)
        self.assertEqual(data["mean"], 23)

    def test_median_0(self):
        nums = [1, 3, 3, 6, 7, 8, 9]
        data = info(nums)
        self.assertAlmostEqual(data["median"], 6)

    def test_median_1(self):
        nums = [1, 2, 3, 4, 5, 6, 8, 9]
        data = info(nums)
        self.assertAlmostEqual(data["median"], 4.5)

    def test_median_2(self):
        nums = [26, 36, 34, 25, 32, 40, 41, 27, 28, 32, 35, 38, 41, 42, 45]
        data = info(nums)
        self.assertAlmostEqual(data["median"], 35)

    def test_median_3(self):
        nums = [2, 4, 5, 4, 8, 7, 8, 7, 3, 1]
        data = info(nums)
        self.assertEqual(data["median"], 4.5)

    def test_mode_1(self):
        nums = [3, 1, 8, 4, 6, 1, 5, 1, 3, 8, 5, 7]
        data = info(nums)
        self.assertCountEqual(data["mode"], [1])

    def test_mode_2(self):
        nums = [2, 6, 4, 5, 8, 7]
        data = info(nums)
        self.assertCountEqual(data["mode"], [])

    def test_mode_3(self):
        nums = [1, 4, 5, 8, 3, 4, 3, 2, 5]
        data = info(nums)
        self.assertCountEqual(data["mode"], [3, 4, 5])

    def test_perncetiles(self):
        nums = [8, 9, 12, 13, 16, 17, 18, 20, 22, 30, 31, 40]
        data = info(nums)
        self.assertListEqual([12.25, 17.5, 28], data["quartiles"])

    def test_variance_and_std_of_sample(self):
        nums = [4, 5, 6, 7, 7, 8, 12]
        data = info(nums)
        self.assertAlmostEqual(data["var_of_sample"], 6.67, places = 2)
        self.assertAlmostEqual(data["std_of_sample"], 2.58, places = 2)

def suite():
    suites_list = []
    test_classes = [Test_info]
    loader = unittest.TestLoader()
    for test_class in test_classes:
        suites_list.append(loader.loadTestsFromTestCase(test_class))
    big_suite = unittest.TestSuite(suites_list)
    return big_suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
