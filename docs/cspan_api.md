# STC [cspan](../include/stc/cspan.h): Multi-dimensional Array View
![Array](pics/array.jpg)

The **cspan** is templated non-owning multi-dimensional view of an array. 

See the c++ class [std::mdspan](https://en.cppreference.com/w/cpp/container/mdspan) for a similar functionality.

## Header file and declaration

```c
#include <stc/cspan.h>
using_cspan(SpanType, ValueType, Rank);                                    // define SpanType with ValueType elements.
                                                                           // Rank is number of dimensions (max 4 atm.)
// Shorthands:
using_cspan2(S, ValueType);                                                // define span types S1, S2 with Ranks 1, 2.
using_cspan3(S, ValueType);                                                // define span types S1, S2, S3 with Ranks 1, 2, 3.
using_cspan4(S, ValueType);                                                // define span types S1.., S4 with Ranks 1, 2, 3, 4.
```
## Methods

```c
SpanType            cspan_make(ValueType* data,  size_t xdim, ...);         // make N-dimensional cspan
SpanType            cspan_from(STCContainer* cnt);                          // create a 1D cspan from a compatible STC container
SpanType            cspan_from_array(ValueType array[]);                    // create a 1D cspan from a C array.
SpanType&           cspan_literal(SpanType, {val1, val2, ...});             // create a 1D cspan compound literal

void                cspan_reshape(const SpanType* self, size_t xdim, ...);     // change the extent of each dimension

size_t              cspan_size(const SpanType* self);                       // return number of elements
unsigned            cspan_rank(const SpanType* self);                       // return number of dimensions
ValueType*          cspan_at(SpanType* self, size_t x, ...);                // access element
size_t              cspan_index(const SpanType* self, size_t x, ...);       // index of element

SpanType            cspan_slice1(SpanType1* self, size_t x0, size_t width); // get a slice of a 1D cspan
SpanType            cspan_slice2(SpanType2* self, size_t x0, size_t width); // get a slice of a 2D cspan
SpanType            cspan_slice3(SpanType3* self, size_t x0, size_t width); // get a slice of a 3D cspan
SpanType            cspan_slice4(SpanType4* self, size_t x0, size_t width); // get a slice of a 4D cspan

// Ex usage 1: MySpan2 ms2 = cspan_3to2(&ms3, ms3.dim[0]-1); // last x slice
// Ex usage 2: ms2 = (MySpan2)cspan_3to2(&ms3, 0); // first x slice
SpanType3           cspan_4to3(SpanType4* self, size_t x);                  // return a 3D subspan
SpanType2           cspan_4to2(SpanType4* self, size_t x, size_t y);        // return a 2D subspan
SpanType1           cspan_4to1(SpanType4* self, size_t x, size_t y, size_t z); // return a 1D subspan
SpanType2           cspan_3to2(SpanType3* self, size_t x);                  // return a 2D subspan
SpanType1           cspan_3to1(SpanType3* self, size_t x, size_t y);        // return a 1D subspan
SpanType1           cspan_2to1(SpanType2* self, size_t x);                  // return a 1D subspan

SpanType_iter       SpanType_begin(const SpanType* self);
SpanTyåe_iter       SpanType_end(const SpanType* self);
void                SpanType_next(SpanType_iter* it);
```
## Types

| Type name        | Type definition                                      | Used to represent... |
|:-----------------|:-----------------------------------------------------|:---------------------|
| SpanType         | `struct { ValueType *data; uint32_t dim[RANK]; }`    | The SpanType         |
| SpanType`_value` | `ValueType`                                          | The ValueType        |
| SpanType`_iter`  | `struct { ValueType *ref; ... }`                     | Iterator type        |

## Example
```c
#include <stdio.h>
#define i_val float
#include <stc/cstack.h>

#include <stc/cspan.h>
using_cspan3(FS, float); // Shorthand to define span types FS1, FS2, and FS3.

int main()
{
    int xd = 6, yd = 4, zd = 3;
    c_AUTO (cstack_float, vec) {
        c_FORRANGE (i, xd*yd*zd)
            cstack_float_push(&vec, i);

        // define arr[xd][yd][zd] cspan
        FS3 span3 = cspan_make(vec.data, xd, yd, zd);
        *cspan_at(&span3, 4, 3, 2) = 3.14f;
        printf("index: %d", (int)cspan_index(&span3, 4, 3, 2));

        FS1 span1 = cspan_3to1(&span3, 4, 3);
        printf("\niterate span1: ");
        c_FOREACH (i, FS1, span1)
            printf("%g ", *i.ref);

        FS2 span2 = cspan_3to2(&span3, 4);
        printf("\niterate span2: ");
        c_FOREACH (i, FS2, span2)
            printf("%g ", *i.ref);

        puts("\niterate span3 by dimensions:");
        c_FORRANGE (i, span3.dim[0]) {
            c_FORRANGE (j, span3.dim[1]) {
                c_FORRANGE (k, span3.dim[2])
                    printf(" %g", *cspan_at(&span3, i, j, k));
                printf(" |");
            }
            puts("");
        }

        printf("%g\n", *cspan_at(&span3, 4, 3, 2));
        printf("%g\n", *cspan_at(&span2, 3, 2));
        printf("%g\n", *cspan_at(&span1, 2));
    }
}
```
Output:
```
index: 59
iterate span1: 57 58 3.14
iterate span2: 48 49 50 51 52 53 54 55 56 57 58 3.14
iterate span3 by dimensions:
 0 1 2 | 3 4 5 | 6 7 8 | 9 10 11 |
 12 13 14 | 15 16 17 | 18 19 20 | 21 22 23 |
 24 25 26 | 27 28 29 | 30 31 32 | 33 34 35 |
 36 37 38 | 39 40 41 | 42 43 44 | 45 46 47 |
 48 49 50 | 51 52 53 | 54 55 56 | 57 58 3.14 |
 60 61 62 | 63 64 65 | 66 67 68 | 69 70 71 |
3.14
3.14
3.14
```