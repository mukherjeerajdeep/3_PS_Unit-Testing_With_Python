# Yatzy Game

## You can use this code to play Yatzy. A whole game with all 14 categories
is quite long. Here you can see a full game played with only two categories.

```text
>>> from yatzy_game import *
>>> random.seed(1234)
>>> import functools
>>> stub_input = functools.partial(next, iter(["4,5", "6", "ones", "1,1,1,3", "1,1,3,6", "twos"]))
>>> play_yatzy_with_categories([ones, twos], input_source=stub_input)
Your roll is:
[1, 1, 1, 4, 5]
[1, 1, 1, 1, 6]
[1, 1, 1, 1, 6]
Hint: available categories and scores:
[(4, 'ones'), (0, 'twos')]
Your score is now 4
Your roll is:
[1, 1, 1, 2, 3]
[1, 1, 2, 3, 6]
[2, 4, 4, 5, 5]
Hint: available categories and scores:
[(2, 'twos')]
Your score is now 6
ones:       4
twos:       2
<BLANKLINE>
Final Score: 6
```

## This next game is very similar, but with different choices for the re-rolls.

```text
>>> random.seed(4321)
>>> stub_input = functools.partial(next, iter(["2,3,4", "3,6", "ones", "1,3,4,5", "4,4,5", "twos"]))
>>> play_yatzy_with_categories([ones, twos], input_source=stub_input)
Your roll is:
[1, 1, 2, 3, 4]
you chose to re-roll '2,3,4'
[1, 1, 1, 3, 6]
you chose to re-roll '3,6'
[1, 1, 1, 1, 6]
Hint: available categories and scores:
    Category 'ones' would score 4
    Category 'twos' would score 0
you chose category 'ones'
Your score is now 4
Your roll is:
[1, 2, 3, 4, 5]
you chose to re-roll '1,3,4,5'
[2, 2, 4, 4, 5]
you chose to re-roll '4,4,5'
[2, 2, 4, 4, 6]
Hint: available categories and scores:
    Category 'twos' would score 4
you chose category 'twos'
Your score is now 8
ones:       4
twos:       4
<BLANKLINE>
Final Score: 8
```
## This game has two more complex categories, 'small_straight' and 'four_of_a_kind'

```text
>>> random.seed(4321)
>>> stub_input = functools.partial(next, iter(["2,3,4", "3,6", "four_of_a_kind", "", "", "small_straight"]))
>>> play_yatzy_with_categories([small_straight, four_of_a_kind], input_source=stub_input)
Your roll is:
[1, 1, 2, 3, 4]
you chose to re-roll '2,3,4'
[1, 1, 1, 3, 6]
you chose to re-roll '3,6'
[1, 1, 1, 1, 6]
Hint: available categories and scores:
    Category 'four_of_a_kind' would score 4
    Category 'small_straight' would score 0
you chose category 'four_of_a_kind'
Your score is now 4
Your roll is:
[1, 2, 3, 4, 5]
you chose to re-roll ''
[1, 2, 3, 4, 5]
you chose to re-roll ''
[1, 2, 3, 4, 5]
Hint: available categories and scores:
    Category 'small_straight' would score 15
you chose category 'small_straight'
Your score is now 19
small_straight:       15
four_of_a_kind:       4
<BLANKLINE>
Final Score: 19
```

##  Run doctest from the terminal 

```text
YatzyGameWithDoctest>python -m doctest  .\yatzy.py
YatzyGameWithDoctest>
YatzyGameWithDoctest>
YatzyGameWithDoctest>python -m doctest  .\yatzy.py -v
Trying:
    chance([5,5,5,5,5])
Expecting:
    25
ok
Trying:
    chance([1,2,3,4,5])
Expecting:
    15
ok
Trying:
    dice_counts([1,2,2,3,3])
Expecting:
    {1: 1, 2: 2, 3: 2, 4: 0, 5: 0, 6: 0}

```

## The `...` dots are used as a wildcard for the doctest as PyTest default set them as wildcard

Elipsis avoids the exact object/date returned by the REPL to get it checked by doctest. 

```python
    >>> scores_in_categories([1,1,2,2,2], (ones, full_house)) #doctest: +ELLIPSIS
    [(8, <function full_house at ...>), (2, <function ones at ...>)]
```

The special string/annotation let doctest to let know to ignore the details as such for the exceptions. 
Here is that `#doctest: +IGNORE_EXCEPTION_DETAIL`

```python
    >>> dice_counts("12345")  #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    TypeError:  Can't convert 'int' object to str implicitly
    """
```