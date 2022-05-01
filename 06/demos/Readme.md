# Different kind of Test-Doubles used 

[](http://xunitpatterns.com)
[](https://en.wikipedia.org/wiki/Test_double)

## Test double with Simple `Stubbing` and using `Mock class`

In the `check()` method we check if the pressure is in allowed range, if it is outside then we 
raise an alarm. 

Here we can see that the `Alarm class` is dependent on the `Sensor class` because it needs the data 
from the `Sensor class` to determine the tire pressure. The `check()` function uses a method from
Sensor class named `sample_pressure()`

**Alarm Class:**
```python

    def __init__(self, sensor=None):
        self._low_pressure_threshold = 17
        self._high_pressure_threshold = 21
        self._sensor = sensor or Sensor()
        self._is_alarm_on = False
        
    def check(self):
        pressure = self._sensor.sample_pressure()
        if pressure < self._low_pressure_threshold \
                or self._high_pressure_threshold < pressure:
            self._is_alarm_on = True
```

**Sensor Class:**
```python
    _OFFSET = 16

    def sample_pressure(self):
        pressure_telemetry_value = self.simulate_pressure()
        return Sensor._OFFSET + pressure_telemetry_value
```
Now in the test we need to write a sensor stub and also in production code we need to remove 
hard-coded dependency in the `__init__()` method to use either the real sensor or stubbed sensor, by
`self._sensor = sensor or Sensor()`.

It is stubbed in the test, the new stub `class StubSensor` is created and returned. The that is used 
when an `object/instance` of `Alarm()` is created and `checked()` is called for that. The sensor 
argument passed is the `StubSensor()`. 

In this case the dependency object/instance of type Sensor is stubbed with the test-double. The same 
`sample_pressure()` is created in test as the real one. 

```python
class StubSensor:
    def sample_pressure(self):
        return 15


def test_low_pressure_activates_alarm():
    alarm = Alarm(sensor=StubSensor())
    alarm.check()
    assert alarm.is_alarm_on
```
This is simple stubbing but we need to write our handwritten stub clas/methods here. We can use a 
framework instead of that. This is the steps 

1. We stub the sensor `stub_sensor = Mock(Sensor)`  
2. Setting the value of the tire-pressure using that `Mock` object of type `Sensor()`.
3. Passing that test-double or the instance during the call of the Alarm as argument.
4. The return_value used here is a property of Mock() class, see [](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.return_value)

```python
def test_normal_pressure_alarm_stays_off():
    stub_sensor = Mock(Sensor) ---(1)
    stub_sensor.sample_pressure.return_value = 18  ---(2)/(4)
    alarm = Alarm(stub_sensor) ---(3)
    alarm.check()
    assert not alarm.is_alarm_on
```

## Using the `Fake method`. 

Now this two methods are dependent on the file passed, however using a stubbed-file will make the test
much faster. Again a tightly coupled file object than wamted loosely coupled instance we are handling.

Here the below methods are file dependant.
*     _file.readline()
*     _file.tell()
*     _file.seek

```python
    def _find_page_breaks(self):
        """Read the file and note the positions of the page breaks,
        so we can access them quickly"""
        self.breaks = [0]

        while True:
            line = self._file.readline() --- (1)
            if not line:
                break
            if "PAGE_BREAK" in line:
                self.breaks.append(self._file.tell())
        self.breaks.append(self._file.tell()) --- (2)

    def get_html_page(self, page):
        """Return html page with the given number (zero indexed)"""
        page_start = self.breaks[page]
        page_end = self.breaks[page+1]
        html = ""
        self._file.seek(page_start)  --- (3)
        while self._file.tell() != page_end:
            line = self._file.readline()  --- (1)
            if "PAGE_BREAK" in line:
                continue
            line = line.rstrip()
            html += html_converter.escape(line, quote=True)
            html += "<br />"
        return html
```

Here we used `Fake` than stub. Module named StringIO class to immediate the file object.
We fake this out by

```python
def test_convert_quotes():
    fake_file = io.StringIO("quote: ' ")
    converter = HtmlPagesConverter(file=fake_file)
```
Or by creating the pages in this case. 
```python
def test_access_second_page():
    fake_file = io.StringIO("""\
page one
PAGE_BREAK
page two
PAGE_BREAK
page three
""")
    converter = HtmlPagesConverter(file=fake_file)
```

## Using the dummy. 

The use of dummy here is in the method declaration as an optional argument. It is `additional_rules=None` 
which will help to pass None if the user don't want to use the `additional_rules` other than `fizz/buzz`  

```python
def fizzbuzz(n, additional_rules=None):
    """
    Convert a number to it's name in the game FizzBuzz
    >>> fizzbuzz(2)
    '2'
    >>> fizzbuzz(3)
    'Fizz'
    >>> fizzbuzz(5)
```

## Using `spy` or `Mock` to verify a method is called or not.

When using the basic method without any checking the is_valid() for the SingleSignOnRegistry class. 

```python
    def handle(self, request, sso_token):
        if self.sso_registry:        
            return Response("Hello {0}!".format(request.name))
        else:
            return Response("Please sign in")
```

Then to pass the test we are using `dummy` which is `None` here for this test, `service = MyService(None)`.

```python
def test_hello_name_return_sign_in_if_invalid_SSO_passed():
    service = MyService(None)
    response = service.handle(Request("Emily"), SSOToken())
    assert response.text == "Please sign in"
```

Using the spy we can verify that the is_valid() is called. 

1. We used `Mock(<Class or Type to mock>)` to create a spy. 
2. Create a token by `token = SSOToken()`
3. Test the method `handle()` under test `service.handle(Request("Emily"), token)`
4. Spy verifies that the `is_valid()` method is called with the `token` by `assert_called_with()` method. 

```python
def test_single_sign_on():
    # given
    spy_sso_registry = Mock(SingleSignOnRegistry) --- (1)
    service = MyService(spy_sso_registry)    
    token = SSOToken() --- (2)
    # when
    service.handle(Request("Emily"), token) --- (3)
    # then
    spy_sso_registry.is_valid.assert_called_with(token)
```

Now we can modify our handle() method to call the dependency method is_valid() and spy verifies 
that `self.sso_registry.is_valid(sso_token)`.

```python
    def handle(self, request, sso_token):
        if self.sso_registry.is_valid(sso_token): --- (1)
            return Response("Hello {0}!".format(request.name))
        else:
            return Response("Please sign in")
```


Check this by removing the is_valid() here, then the stub will pass but the spy will fail :
```python
    def handle(self, request, sso_token):
        if self.sso_registry.is_valid(sso_token) to if self.sso_registry:
```

Using the spy but a small modification when passing an invalid token. We set the return_value to False when 
setting the spy. Then we assert the result as we did before. The changed lines are 
`spy_sso_registry.is_valid.return_value = False` and `assert response.text == "Please sign in"`

```python
def test_single_sign_on_with_invalid_token():
    spy_sso_registry = Mock(SingleSignOnRegistry)
    spy_sso_registry.is_valid.return_value = False ---(1)
    service = MyService(spy_sso_registry)
    token = SSOToken()
    response = service.handle(Request("Emily"), token)
    spy_sso_registry.is_valid.assert_called_with(token) ---(From Previous Test)
    assert response.text == "Please sign in" ---(2)
```
![Spy_Func_Ref](https://user-images.githubusercontent.com/43293317/166157391-fcbb5c3d-c3d6-4326-ad1c-05dc7d78aa1c.PNG)

1. **_Spy is exactly has same methods as the original method_**. So we can say it listens how MyService class works
on the method calls. 
2. **_The stub can't fail a test but the spy can fail a test._**.
3. **_Spy records all the call it receives, so assertions are possible_** for the verification of the calls.
4. Using spy to check **_interaction between two objects_** happening smoothly. 

Mock in other way uses the same thing however it prints a nice stack trace when the assertions fail. Here is 
the code for the test, the `confirm_token()` replaces the actual `is_valid()` when called at line (1). It is used
as a HOT Plugin for the `is_valid()` used with the `mock_sso_registry` instance. 


```python
def confirm_token(correct_token):
    def is_valid(actual_token):
        if actual_token != correct_token:
            raise ValueError("wrong token received")
    return is_valid


def test_single_sign_on_receives_correct_token():
    mock_sso_registry = Mock(SingleSignOnRegistry)
    correct_token = SSOToken()
    mock_sso_registry.is_valid = Mock(side_effect=confirm_token(correct_token)) --- (1)
    service = MyService(mock_sso_registry)
    service.handle(Request("Emily"), correct_token)
    mock_sso_registry.is_valid.assert_called()
```
