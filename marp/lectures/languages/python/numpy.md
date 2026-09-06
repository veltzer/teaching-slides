---
tags:
- languages:python
- concepts:data-science
- concepts:performance
- concepts:numerical-computing
- tools:numpy
level: intermediate
category: language
audience:
- audiences:developers
- audiences:data-scientists

---

# NumPy and Python
## The Foundation of Numerical Computing in Python
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

## What This Lecture Covers

1. What NumPy is and why every data library builds on it
1. The `ndarray` — typed, contiguous memory
1. Vectorization — moving loops from Python into C
1. Broadcasting — arithmetic across different shapes
1. Indexing, views, and copies
1. Aggregations, axes, and linear algebra
1. Random numbers and file I/O
1. Performance habits and knowing NumPy's limits

---

## What Is NumPy?

- The fundamental array library of scientific Python
- One core object: the `ndarray` — an N-dimensional typed array
- Array math implemented in **C**, not in the interpreter
- The common data format of the ecosystem — pandas, SciPy,
  scikit-learn, and Matplotlib all speak NumPy arrays
- If you do numbers in Python, you are already using it

---

## Why Not Plain Python Lists?

- A list stores **pointers** to boxed objects scattered on the heap
- Every element carries full object overhead — type, refcount, value
- A loop pays interpreter cost for **every single element**
- Caches hate it: each access chases a pointer somewhere else
- Fine for a hundred items; hopeless for a hundred million

---

## Lists and Arrays in Memory

![memory](svg/lectures/languages/python/numpy/memory.svg)

---

## The ndarray

- One block of **contiguous memory** with a single `dtype`
- `shape` describes the dimensions: `(3, 4)`, `(1000,)`, `(64, 64, 3)`
- Element access is arithmetic, not pointer chasing
- No boxing: a million `float64` values cost eight megabytes, period
- This layout is the contract that makes fast math possible

---

## Creating Arrays

```python
import numpy as np

a = np.array([1.0, 2.5, 3.7])
z = np.zeros((3, 4))
o = np.ones(10)
r = np.arange(0, 10, 2)
x = np.linspace(0.0, 1.0, 101)
```

- Constructors take a **shape**; `arange`/`linspace` build ranges
- Prefer `linspace` when you care about the endpoint and count

---

## Data Types

```python
a = np.array([1, 2, 3], dtype=np.int32)
b = a.astype(np.float64)
print(a.dtype, a.itemsize)
```

- One `dtype` per array — that uniformity **is** the speed contract
- Integers, floats, booleans, complex — in fixed sizes
- `NaN` exists only for floats — integer arrays cannot hold "missing"
- Conversions are explicit with `astype`; upcasts can double memory

---

## Vectorization

```python
salaries = np.array([98_000, 84_000, 121_000])

monthly = salaries / 12
raised = salaries * 1.1
senior = salaries > 100_000
taxed = np.where(senior, salaries * 0.55, salaries * 0.7)
```

- Operators work on **whole arrays** — no visible loop
- Each operation is one call into a compiled C loop
- Comparisons produce boolean arrays — the basis for masks

---

## One Call, Whole Array

![vectorize](svg/lectures/languages/python/numpy/vectorize.svg)

---

## Broadcasting

- Arithmetic between arrays of **different shapes** — without copies
- Align shapes from the right; each dimension must be equal or 1
- Size-1 dimensions are logically **stretched** to match
- The stretch is virtual — no memory is duplicated
- Most "add a row/column to a matrix" tasks are one line

---

## Broadcasting in Code

```python
m = np.zeros((3, 4))
row = np.array([1.0, 2.0, 3.0, 4.0])
col = np.array([[10.0], [20.0], [30.0]])

m + row    # (3,4) + (4,)   row is stretched down
m + col    # (3,4) + (3,1)  column is stretched across
```

- Shape mismatch that cannot broadcast raises immediately
- When in doubt, print `a.shape` — debugging starts there

---

## How Broadcasting Stretches

![broadcasting](svg/lectures/languages/python/numpy/broadcasting.svg)

---

## Indexing and Slicing

```python
a = np.arange(12).reshape(3, 4)

a[0, 2]       # one element
a[1]          # one row
a[:, 1]       # one column
a[0:2, 1:3]   # a sub-matrix
```

- Multi-dimensional indexing takes one bracket, comma-separated
- Slices look exactly like list slicing — but behave differently

---

## Views vs Copies

```python
s = a[:, 1]        # a VIEW — shares a's memory
s[0] = 99          # a changed too!

c = a[:, 1].copy() # independent data
```

- Slicing returns a **view** — a window into the same buffer
- Views make slicing free; mutation travels through them
- When you need independence, say so: `.copy()`

---

## Views Share the Buffer

![views](svg/lectures/languages/python/numpy/views.svg)

---

## Masks and Fancy Indexing

```python
a[a > 5]                 # boolean mask
a[(a > 2) & (a < 9)]     # combined conditions

idx = np.array([2, 0, 1])
a[idx]                   # rows in a chosen order
```

- Masking selects by condition; fancy indexing selects by position
- Both return **copies**, unlike plain slices
- Combine conditions with `&`, `|`, `~` — with parentheses

---

## Reshaping

```python
a.reshape(4, 3)   # same data, new shape
a.T               # transpose
a.ravel()         # flatten to 1-D
```

- `reshape` is free when the data can stay in place — it's a view
- Transpose never copies — it just swaps the stride bookkeeping
- `-1` lets NumPy infer one dimension: `a.reshape(2, -1)`

---

## Aggregations and the axis Argument

```python
a.sum()          # one number — everything
a.sum(axis=0)    # collapse rows: one value per column
a.sum(axis=1)    # collapse columns: one value per row
a.mean(), a.std(), a.min(), a.argmax()
```

- `axis` names the dimension that **disappears**
- Works uniformly across `sum`, `mean`, `min`, `argmax`, and friends

---

## What axis Means

![axis](svg/lectures/languages/python/numpy/axis.svg)

---

## Linear Algebra

```python
A = np.array([[2.0, 1.0], [1.0, 3.0]])
b = np.array([1.0, 2.0])

x = np.linalg.solve(A, b)   # solve A @ x == b
y = A @ x                   # matrix multiply
vals, vecs = np.linalg.eig(A)
```

- `@` is matrix multiplication; `*` stays element-wise
- `np.linalg` covers solve, inverse, decompositions, eigenvalues
- Backed by optimized BLAS/LAPACK — this part uses many cores

---

## Random Numbers

```python
rng = np.random.default_rng(seed=42)

u = rng.random(1_000)
n = rng.normal(0.0, 1.0, size=(3, 4))
pick = rng.choice(["a", "b", "c"], size=10)
```

- Use the **generator API** — seedable, reproducible, no global state
- The old `np.random.rand` style still works but don't start there
- One seeded generator per experiment makes runs repeatable

---

## Saving and Loading

```python
np.save("weights.npy", a)
a = np.load("weights.npy")

np.savez("model.npz", weights=a, bias=b)
data = np.loadtxt("table.csv", delimiter=",", skiprows=1)
```

- `.npy` is fast, exact, and keeps the `dtype` and shape
- `.npz` bundles several named arrays in one file
- For rich tabular data, hand over to pandas or Polars

---

## Performance Habits

- Replace every Python loop over elements with array operations
- Preallocate output arrays; never grow arrays in a loop
- Watch `dtype`: an accidental `float64` upcast doubles memory
- Prefer views over copies; copy only when you must own the data
- Measure first — `%timeit` in a notebook settles arguments

---

## The Ecosystem Standard

- pandas columns, SciPy routines, scikit-learn inputs — all arrays
- Matplotlib plots arrays; image and audio libraries produce them
- The `ndarray` is the **interchange format** of scientific Python
- Learn NumPy once and every downstream library feels familiar
- Even GPU libraries copy its API almost verbatim

---

## The Foundation of the Stack

![stack](svg/lectures/languages/python/numpy/stack.svg)

---

## Where NumPy Stops

- Mostly **single-threaded** — linear algebra is the exception
- Everything must fit in RAM — no lazy evaluation, no streaming
- No named columns — rows and columns carry no labels
- Tabular work with mixed types belongs in pandas or Polars
- On GPUs, JAX, PyTorch, and CuPy take over — same array ideas

---

## Summary

- NumPy is one idea done well: **typed, contiguous arrays**
- Vectorization moves loops from the interpreter into C
- Broadcasting gives shape-aware arithmetic without copies
- Slices are **views** — know when memory is shared
- The whole scientific Python stack stands on this foundation

---

## Where to Start

1. Rewrite one loop-heavy script with arrays and no explicit loops
1. Learn shapes cold: print `a.shape` until it is second nature
1. Practice `axis` on small matrices until aggregations feel obvious
1. Read the broadcasting rules once — then trust them

The mental shift is loops → whole-array thinking; the rest follows.

---

## Questions?

- Arrays are typed contiguous memory — that is the whole trick
- Vectorize, broadcast, and mind your views
- NumPy is the floor the rest of the data stack stands on

## Thank You
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)
