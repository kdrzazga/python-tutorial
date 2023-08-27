# Find first unique element in an array
def find_unique_element(array):
    frequency_map = {}
    for element in array:
        frequency_map[element] = frequency_map.get(element, 0) + 1

    for key, value in frequency_map.items():
        if 1 == value:
            return key
    return -1


# In an array, find first element, that sum with following element = 9
# e.g  (1, 3, 6, 3, 10, 20) -> 3


def find_1st_element_that_sums_with_next(arr, expected_sum):
    for index in range(len(arr) - 1):
        if arr[index] + arr[index + 1] == expected_sum:
            return arr[index]


# Write a function that takes a list of integers and returns sum of even numbers


def sum_even_numbers(lst):
    even_nums = []
    for elem in lst:
        if elem % 2 == 0:
            even_nums.append(elem)

    return sum(even_nums)


# function that takes a string as input and returns the reverse of the string and capilatizes each 2nd letter

def reverse_cap_2nd(s):
    return ''.join(c.upper() if i % 2 == 0 else c for i, c in enumerate(reversed(s)))


# function that takes two lists of integers as input and returns a new list
# that contains only the elements that are common to both lists or elements
# divisible by 3 from the first list
def find_common_divisible_3(l1, l2):
    common_elements = list(set(l1).intersection(l2))
    return [x for x in common_elements if x % 3 == 0]


if __name__ == '__main__':
    test_tuple = (1, 2, 3, 1, 3, 150)

    assert find_unique_element(test_tuple) == 2
    assert find_1st_element_that_sums_with_next(test_tuple, 4) == 3
    assert sum_even_numbers(test_tuple) == 152
    assert reverse_cap_2nd("Hello World") == 'DlRoW OlLeH'
    tpl1 = (1, 3, 5, 6, 7, 11, 15, 21, 24)
    tpl2 = (11, 12, 15, 16, 7, 11, 24)
    assert find_common_divisible_3(tpl1, tpl2) == [24, 15]
I
