# Parameterized Test Start

## Example for PyTest

This kind of writing test will bring a lot of duplication 
```python
from tennis import score_tennis

def test_0_0_love_all():
    assert score_tennis(0, 0) == "Love-All"

def test_1_1_love_all():
    assert score_tennis(1, 1) == "Fifteen-All"

def test_2_2_love_all():
    assert score_tennis(0, 0) == "Thirty-All"
```

Once we make them parameterized `pytest` then the argument of the function would be the parameters, in this case the `player1_points`, `player2_points` and `expected_score`.

The special annotation helps to parameterize the tests `@pytest.mark.parametrize`. This decorator takes the parameters and the `list` of **iterable** which can be a list, dict or tuple based on the supplied parameters. In this case our each test case is 

```yaml
(0, 0, "Love-All") -> 
    player1_points -> 0
    player2_points -> 0
    expected_score -> "Love-All"
```

```python
@pytest.mark.parametrize("player1_points, player2_points, expected_score",
                         [(0, 0, "Love-All"),
                          (1, 1, "Fifteen-All"),
                          (2, 2, "Thirty-All"),
                          (2, 1, "Thirty-Fifteen"),
                          (3, 1, "Forty-Fifteen"),
                          (4, 1, "Win for Player 1"),
                          (4, 3, "Advantage Player 1"),
                          (4, 5, "Advantage Player 2"),
                          ])
def test_score_tennis(player1_points, player2_points, expected_score):
    assert score_tennis(player1_points, player2_points) == expected_score
```

## Example for UnitTest

Same can be written in legacy `unittest` as well. Both are same but with some biolier plate in the `unittest`

The disadvantage is if one of this fails without the use of `with.subtest` then rest of the test case are deemed to fail as well

```python
def test_score_tennis(self):
    test_cases = [
        (0, 0, "Love-All"),
        (1, 1, "Fifteen-All"),
        (2, 2, "Thirty-All"),
        (2, 1, "Thirty-Fifteen"),
        (3, 1, "Forty-Fifteen"),
        (4, 1, "Win for Player 1"),
        (4, 3, "Advantage Player 1"),
        # (4, 5, "Advantage Player 2"),
    ]
    for player1_points, player2_points, expected_score in test_cases:
        with self.subTest(f"{player1_points}, {player2_points} -> {expected_score}"):
            self.assertEqual(expected_score, score_tennis(player1_points, player2_points))
```

## Coverage Tests

Needed to download :
```text
 python -m pip install coverage
 python -m pip install pytest-cov
```

### With Coverage

Then we need to run `python.exe -m coverage` to generate the report inside the root folder. Then the `python.exe -m coverage html` will generate a sub-folder in the root path and inside it, there will be `index.html` which contains the report. 

![](C:\Rajdeep_Mukherjee\PluralSight_Python\3_PS_Unit-Testing_With_Python\07\demos\code\ParameterisedTennis\cov1.PNG)

### With Pytest-Cov

More controlled way of gathering the reports. 
The command to be used here is :

```text
python.exe -m pytest --cov-report html:cov_html --cov=tennis .
    --cov-report - The report name
    html:cov_html - kind of report generation
    --cov=tennis - Which modules we want to gather coverage matrix  
    . - which folder the script should look in
```

This can be executed with branch information as well. More detailed and clearer highlights.
`python.exe -m pytest --cov-report html:cov_html --cov-branch --cov=tennis .`

Go inside the `cov_html` and open th index.html in browser. 