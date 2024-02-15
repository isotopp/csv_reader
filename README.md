# csv_reader

We have a file testdata.csv:

```
sep=,
field_a,field_b,field_c
10.0,20.0,30.0
1.0,2.0,3.0
```

We want to read this file into a frozen dataclass with slots,
but the dataclass should have field names from the csv file.

This can be done using 
[make_dataclass](https://docs.python.org/3/library/dataclasses.html#dataclasses.make_dataclass).

```python
C = make_dataclass('MyClass',
                   [('field_a', float),
                    ('field_b', float),
                    ('field_c', float),]
```

is the same as

```python
@dataclass
class C:
    field_a: float
    field_b: float
    field_c: float
```

The code shows how to do this, sanitizing field names, and typing the dataclass.
