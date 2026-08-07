
def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]


result = two_sum([3, 2, 4], 6)
print(result == [1, 2])
