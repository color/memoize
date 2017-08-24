# memoize

A memoize decorator.

## Getting Started

* Install memoize
```
$ pip install git+https://git+https://github.com/ColorGenomics/memoize.git@v0.2.2
```

* Use a memoize decorator
```
> from memoize import memoize
>
> @memoize
> def return_one():
>   print 'first time'
>   return 1
>
> return_one()
=> 'first time'
=> 1
> return_one()
=> 1
```
