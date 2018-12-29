a tool to diff dict list set data output like the npm package [deep_diff](https://www.npmjs.com/package/deep-diff)

# install
`pip install deep-diff`
# USAGE

diff dict
```
from deep_diff import diff
diff({'a':1,'c':1},{'b':1,'c':1})
'[{'kind': 'D', 'path': ['a'], 'lhs': 1},
 {'kind': 'N', 'path': ['b'], 'rhs': 1}]'
```

Except path
```
from deep_diff import diff
diff({'a':1,'c':1},{'b':1,'c':1},[['a'],['b']])
''
```

more use can see test.py

``` json
[ { kind: 'E',
    path: [ 'name' ],
    lhs: 'my object',
    rhs: 'updated object' },
  { kind: 'E',
    path: [ 'details', 'with', 2 ],
    lhs: 'elements',
    rhs: 'more' },
  { kind: 'A',
    path: [ 'details', 'with' ],
    index: 3,
    item: { kind: 'N', rhs: 'elements' } },
  { kind: 'A',
    path: [ 'details', 'with' ],
    index: 4,
    item: { kind: 'N', rhs: { than: 'before' } } } ]
```

### Differences

Differences are reported as one or more change records. Change records have the following structure:

* `kind` - indicates the kind of change; will be one of the following:
  * `N` - indicates a newly added property/element
  * `D` - indicates a property/element was deleted
  * `E` - indicates a property/element was edited
  * `A` - indicates a change occurred within an array
* `path` - the property path (from the left-hand-side root)
* `lhs` - the value on the left-hand-side of the comparison (undefined if kind == 'N')
* `rhs` - the value on the right-hand-side of the comparison (undefined if kind == 'D')
* `index` - when kind == 'A', indicates the array index where the change occurred
* `item` - when kind == 'A', contains a nested change record indicating the change that occurred at the array index
