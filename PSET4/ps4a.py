# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    sequence = sequence.lower()

    if len(sequence) == 0:
        return ['']
    else:
        first_element = sequence[0]
        rest = sequence[1:]
        permutation_rest = get_permutations(rest)

        all_permutations = []
        for perm in permutation_rest:
            for i in range(len(perm) + 1):
                all_permutations.append(perm[:i] + first_element + perm[i:])
        return all_permutations


    

if __name__ == '__main__':
#    #EXAMPLE
    # example_input = 'abc'
    # print('Input:', example_input)
    # print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    # print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)
    example_input = 'dark'
    print('Input:', example_input)
    print('Actual Output:', get_permutations(example_input))
    print('-----------------------')
    example_input = 'glues'
    print('Input:', example_input)
    print('Actual Output:', get_permutations(example_input))
    print('-----------------------')
    example_input = 'Anthony'
    print('Input:', example_input)
    print('Actual Output:', get_permutations(example_input))

    

