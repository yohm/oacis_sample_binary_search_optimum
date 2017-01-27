# oacis_sample_binary_search_optimum

Finding a parameter search which maximizes the output by binary search.

## Algorithm

A sample one-dimensional binary search to find a ParameterSet which maximizes the specified output.

1. Find the PS having the largest "output".
1. Create two ParameterSets at the midpoints between the found PS and its neighbors.
1. Go back to 1 until we obtain enough resolution.

## Prerequisites

Register a simulator for testing using the following command.
It will make a new Simulator named "binary\_search\_optimum\_test".
However, the algorithm is designed to work not only for this simulator but for general cases.

```sh
oacis_ruby prepare_simulator.rb
```

## How to run

The algorithm is implemented in Python.

```sh
oacis_python find_best_param.py
```

# LICENSE

The MIT License (MIT)

Copyright (c) 2017 RIKEN, AICS

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

