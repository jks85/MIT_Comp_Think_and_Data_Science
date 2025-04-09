###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1
def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    # Code is not optimized as right branch branch is not necessary
    # It is always optimal to take the heaviest egg
    # The right branch has been included to implement a classic binary tree dp algo with memoization
    # Memoization would not be needed if the right branch was excluded as each branch would have a
    # unique target weight


    #set initial egg count
    egg_count = 0

    # check if egg weights/target weight are in memo_dict
    if (egg_weights,target_weight) in memo:
        egg_count = memo[(egg_weights,target_weight)]

    # check if target weight is 0 or egg list is empty (base case)
    if egg_weights == tuple() or target_weight == 0:
        egg_count = 0

    # if heaviest egg doesn't fit take nothing (branch right)
    elif egg_weights[-1] > target_weight:

        # remove heaviest egg from egg list
        # target weight unchanged
        # recursive call

        egg_count = dp_make_weight(egg_weights[:-1], target_weight, memo)

    # if heaviest egg fits (branch left)
        # always optimal to take egg/go left within this subtree
        # using right branch for practice implementing memoization in dp
        # will remove heaviest egg from list if it is not selected (right branch)

    elif egg_weights[-1] <= target_weight:

        # take heaviest egg/explore left branch
        # update target_weight and list of egg_weights
        # recursive call storing egg count with heavy egg

        updated_target_weight = target_weight - egg_weights[-1]
        updated_egg_weights = tuple(weight for weight in egg_weights if weight <= updated_target_weight)
        egg_count_with = 1 + dp_make_weight(updated_egg_weights, updated_target_weight, memo)


        # don't take egg/explore right branch
        # remove heaviest egg from egg list
        # recursive call

        egg_count_without = dp_make_weight(egg_weights[:-1],target_weight, memo)

        # compare left/right result and take smaller result
        # always pick left branch egg count


        egg_count = egg_count_with

        # update memo_dict
        memo[(egg_weights, target_weight)] = egg_count

    return egg_count




# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights =", str(egg_weights))
    print("n = ", n)
    print("Expected output: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()
    print('')

 ## additional tests
    egg_weights = (1, 5, 10, 20)
    n = 500
    print("Egg weights =", str(egg_weights))
    print("n = ", n)
    print("Expected output: 3 (3 * 20 + 0 * 10 + 0 * 5 + 0 * 1 = 5)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()


# note dp_make_weight() starts to noticeably slow down ~ n = 300.
# still only takes a few seconds with n = 500
# took a long time for n = 1000 (waited ~30 seconds and it hadn't finished)