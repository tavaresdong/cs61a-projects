##############################################################
# An alternative implementation of the tree data abstraction #
##############################################################

def tree(root, branches=[]):
    for branch in branches:
        assert is_tree(branch), 'branches must be trees'
    return {'<root>': root, '<branches>': branches}

def root(t):
    return t['<root>']

def branches(t):
    return t['<branches>']

def is_tree(t):
    if type(t) != dict or '<root>' not in t or '<branches>' not in t:
        return False
    for branch in branches(t):
        if not is_tree(branch):
            return False
    return True

def is_leaf(t):
    return not branches(t)

numbers = tree(1, [tree(2), tree(3, [tree(4), tree(5)]), tree(6, [tree(7)])])

def print_tree(t, indent=0):
    """Print a representation of this tree in which each node is
    indented by two spaces times its depth from the root.

    >>> print_tree(tree(1))
    1
    >>> print_tree(tree(1, [tree(2)]))
    1
      2
    >>> print_tree(numbers)
    1
      2
      3
        4
        5
      6
        7
    """
    print('  ' * indent + str(root(t)))
    for branch in branches(t):
        print_tree(branch, indent + 1)

###########
# Mobiles #
###########

def mobile(left, right):
    """Construct a mobile from a left side and a right side."""
    return tree(None, [left, right])

def sides(m):
    """Select the sides of a mobile."""
    return branches(m)

def side(length, mobile_or_weight):
    """Construct a side: a length of rod with a mobile or weight at the end."""
    return tree(length, [mobile_or_weight])

def length(s):
    """Select the length of a side."""
    return root(s)

def end(s):
    """Select the mobile or weight hanging at the end of a side."""
    return branches(s)[0]

def weight(size):
    """Construct a weight of some size."""
    assert size > 0
    "*** YOUR CODE HERE ***"
    return tree(size)

def size(w):
    """Select the size of a weight."""
    "*** YOUR CODE HERE ***"
    return root(w)

def is_weight(w):
    """Whether w is a weight, not a mobile."""
    "*** YOUR CODE HERE ***"
    return is_leaf(w)

def examples():
    t = mobile(side(1, weight(2)),
               side(2, weight(1)))
    u = mobile(side(5, weight(1)),
               side(1, mobile(side(2, weight(3)),
                              side(3, weight(2)))))
    v = mobile(side(4, t), side(2, u))
    return (t, u, v)


def total_weight(m):
    """Return the total weight of m, a weight or mobile.

    >>> t, u, v = examples()
    >>> total_weight(t)
    3
    >>> total_weight(u)
    6
    >>> total_weight(v)
    9
    """
    if is_weight(m):
        return size(m)
    else:
        return sum([total_weight(end(s)) for s in sides(m)])

def with_totals(m):
    """Return a mobile with total weights stored as the root of each mobile.

    >>> t, u, v = examples()
    >>> print_tree(t)
    None
      1
        2
      2
        1
    >>> print_tree(with_totals(t))
    3
      1
        2
      2
        1
    >>> print_tree(t)  # t should not change
    None
      1
        2
      2
        1
    >>> print_tree(with_totals(v))
    9
      4
        3
          1
            2
          2
            1
      2
        6
          5
            1
          1
            5
              2
                3
              3
                2
    >>> print_tree(v)  # v should not change
    None
      4
        None
          1
            2
          2
            1
      2
        None
          5
            1
          1
            None
              2
                3
              3
                2
    """
    "*** YOUR CODE HERE ***"
    # use abstraction barriers
    def withtotal_recur(mob):
        sum_weight, nbranches = 0, []
        if is_weight(mob):
            return size(mob), tree(size(mob))
        for side in sides(mob):
            w, t = withtotal_recur(side)
            sum_weight += w
            # with + operator, the right hand size must also be a list
            nbranches += [t]
        if length(mob) == None:
            return sum_weight, tree(sum_weight, nbranches)
        else:
            return sum_weight, tree(length(mob), nbranches)
    total_w, mob_tree = withtotal_recur(m)
    return mob_tree


def balanced(m):
    """Return whether m is balanced.

    >>> t, u, v = examples()
    >>> balanced(t)
    True
    >>> balanced(v)
    True
    >>> w = mobile(side(3, t), side(2, u))
    >>> balanced(w)
    False
    >>> balanced(mobile(side(1, v), side(1, w)))
    False
    >>> balanced(mobile(side(1, w), side(1, v)))
    False
    """
    "*** YOUR CODE HERE ***"
    def weight_balance(mob):
        if is_weight(mob):
            return True, size(mob)
        else:
            left, right = sides(mob)
            ba_l, wt_l = weight_balance(end(left))
            ba_r, wt_r = weight_balance(end(right))
            if not ba_l or not ba_l:
                return False, 0
            if wt_l * length(left) != wt_r * length(right):
                return False, 0
            return True, wt_l + wt_r
    balance, total_weight = weight_balance(m)
    return balance

############
# Mutation #
############

def make_withdraw(balance, password):
    """Return a password-protected withdraw function.

    >>> w = make_withdraw(100, 'hax0r')
    >>> w(25, 'hax0r')
    75
    >>> w(90, 'hax0r')
    'Insufficient funds'
    >>> w(25, 'hwat')
    'Incorrect password'
    >>> w(25, 'hax0r')
    50
    >>> w(75, 'a')
    'Incorrect password'
    >>> w(10, 'hax0r')
    40
    >>> w(20, 'n00b')
    'Incorrect password'
    >>> w(10, 'hax0r')
    "Your account is locked. Attempts: ['hwat', 'a', 'n00b']"
    >>> w(10, 'l33t')
    "Your account is locked. Attempts: ['hwat', 'a', 'n00b']"
    """
    "*** YOUR CODE HERE ***"
    wrong_pws = []
    def withdraw(deposit, pw):
        nonlocal wrong_pws
        nonlocal password
        nonlocal balance
        if len(wrong_pws) == 3:
            return "Your account is locked. Attempts: ['{0}', '{1}', '{2}']".format(wrong_pws[0], \
                    wrong_pws[1], wrong_pws[2])
        elif pw != password:
            wrong_pws += [pw]
            return 'Incorrect password'
        else:
            if balance < deposit:
                return 'Insufficient funds'
            balance = balance - deposit
            return balance
    return withdraw


            


def make_joint(withdraw, old_password, new_password):
    """Return a password-protected withdraw function that has joint access to
    the balance of withdraw.

    >>> w = make_withdraw(100, 'hax0r')
    >>> w(25, 'hax0r')
    75
    >>> make_joint(w, 'my', 'secret')
    'Incorrect password'
    >>> j = make_joint(w, 'hax0r', 'secret')
    >>> w(25, 'secret')
    'Incorrect password'
    >>> j(25, 'secret')
    50
    >>> j(25, 'hax0r')
    25
    >>> j(100, 'secret')
    'Insufficient funds'

    >>> j2 = make_joint(j, 'secret', 'code')
    >>> j2(5, 'code')
    20
    >>> j2(5, 'secret')
    15
    >>> j2(5, 'hax0r')
    10

    >>> j2(25, 'password')
    'Incorrect password'
    >>> j2(5, 'secret')
    "Your account is locked. Attempts: ['my', 'secret', 'password']"
    >>> j(5, 'secret')
    "Your account is locked. Attempts: ['my', 'secret', 'password']"
    >>> w(5, 'hax0r')
    "Your account is locked. Attempts: ['my', 'secret', 'password']"
    >>> make_joint(w, 'hax0r', 'hello')
    "Your account is locked. Attempts: ['my', 'secret', 'password']"
    """
    "*** YOUR CODE HERE ***"
    # test old_password
    test_withdraw = withdraw(0, old_password)
    if not isinstance(test_withdraw, int):
        return test_withdraw 
    def joint_withdraw(deposit, pw):
        if pw == new_password:
            return withdraw(deposit, old_password)
        else:
            return withdraw(deposit, pw)
    return joint_withdraw


###########
# Objects #
###########

class VendingMachine:
    """A vending machine that vends some product for some price.

    >>> v = VendingMachine('candy', 10)
    >>> v.vend()
    'Machine is out of stock.'
    >>> v.restock(2)
    'Current candy stock: 2'
    >>> v.vend()
    'You must deposit $10 more.'
    >>> v.deposit(7)
    'Current balance: $7'
    >>> v.vend()
    'You must deposit $3 more.'
    >>> v.deposit(5)
    'Current balance: $12'
    >>> v.vend()
    'Here is your candy and $2 change.'
    >>> v.deposit(10)
    'Current balance: $10'
    >>> v.vend()
    'Here is your candy.'
    >>> v.deposit(15)
    'Machine is out of stock. Here is your $15.'
    """
    "*** YOUR CODE HERE ***"
    def __init__(self, pname, pprice):
        self.prod_name = pname
        self.prod_price = pprice
        self.stock = 0
        self.balance = 0

    def vend(self):
        if self.stock == 0:
            return 'Machine is out of stock.'
        elif self.balance < self.prod_price:
            return 'You must deposit ${0} more.'.format(self.prod_price - self.balance)
        else:
            if self.balance == self.prod_price:
                self.balance = 0
                self.stock -= 1
                return 'Here is your {0}.'.format(self.prod_name)
            else:
                change = self.balance - self.prod_price
                self.balance = 0
                self.stock -= 1
                return 'Here is your {0} and ${1} change.'.format(self.prod_name, change)


    def restock(self, amount):
        assert amount >= 0
        self.stock += amount
        return 'Current {0} stock: {1}'.format(self.prod_name, self.stock)

    def deposit(self, money):
        if self.stock == 0:
            return 'Machine is out of stock. Here is your ${0}.'.format(money)
        else:
            self.balance += money
            return 'Current balance: ${0}'.format(self.balance)


class MissManners:
    """A container class that only forward messages that say please.

    >>> v = VendingMachine('teaspoon', 10)
    >>> v.restock(2)
    'Current teaspoon stock: 2'

    >>> m = MissManners(v)
    >>> m.ask('vend')
    'You must learn to say please first.'
    >>> m.ask('please vend')
    'You must deposit $10 more.'
    >>> m.ask('please deposit', 20)
    'Current balance: $20'
    >>> m.ask('now will you vend?')
    'You must learn to say please first.'
    >>> m.ask('please hand over a teaspoon')
    'Thanks for asking, but I know not how to hand over a teaspoon.'
    >>> m.ask('please vend')
    'Here is your teaspoon and $10 change.'

    >>> really_fussy = MissManners(m)
    >>> really_fussy.ask('deposit', 10)
    'You must learn to say please first.'
    >>> really_fussy.ask('please deposit', 10)
    'Thanks for asking, but I know not how to deposit.'
    >>> really_fussy.ask('please please deposit', 10)
    'Thanks for asking, but I know not how to please deposit.'
    >>> really_fussy.ask('please ask', 'please deposit', 10)
    'Current balance: $10'
    """
    "*** YOUR CODE HERE ***"
    def __init__(self, obj):
        self.callee = obj

    def ask(self, query, *args):
        # split the query, the first string should be please
        # and the second string should be the function to call
        if not query.lower().lstrip().startswith('please'):
            return 'You must learn to say please first.'
        func_to_call = query[6:].lstrip()
        if hasattr(self.callee, func_to_call):
            func = getattr(self.callee, func_to_call)
            return func(*args)
        else:
            return 'Thanks for asking, but I know not how to {}.'.format(func_to_call)





#############
# Challenge #
#############


