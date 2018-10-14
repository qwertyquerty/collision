# collision.py

- [Classes](#classes)
- [Collisions](#colissions)
- [Examples](#examples)

## Info

Collision is a python library meant for collision detection between convex polygons, circles, and points.

### Insallation

To get the latest stable version:

`pip install collision`

Or to get the latest development version:

`pip install https://github.com/qwertyquerty/collision/archive/master.zip`

## Classes

### ***class*** `collision.vec(x, y)`

A 2D vector/point class

**Properties:**

- `x` *(int) or (float)* - The x-coordinate
- `y` *(int) or (float)* - The y-coordinate

**Methods:**

##### *func* `copy()` &rarr; `collision.vec`

Return a copy of the vector

##### *func* `set(v)`

Copy another vectors values onto the vector

- `v` *(collision.vec)* - The vector to copy from

##### *func* `perp()` &rarr; `collision.vec`

Return the vector rotated perpandicularly

##### *func* `rotate(angle)` &rarr; `collision.vec`

Return the vector rotated the angle

- `angle` *(int) or (float)* - Radians to rotate the point

##### *func* `reverse()` &rarr; `collision.vec`

Return a reversed version of the vector

##### *func* `normalize()` &rarr; `collision.vec`

Return a normalized version of the vector

##### *func* `project(v)` &rarr; `collision.vec`

Return the vector projected onto the passed vector

- `v` *(collision.vec)* - The vector to project upon

##### *func* `project_n(v)` &rarr; `collision.vec`

Return the vector projected onto a unit vector

- `v` *(collision.vec)* - The vector to project upon

##### *func* `reflect(axis)` &rarr; `collision.vec`

Return the vector reflected upon the passed axis vector

- `axis` *(collision.vec)* - The axis to reflect upon

##### *func* `reflect_n(axis)` &rarr; `collision.vec`

Return the vector reflected upon the passed axis unit vector

- `axis` *(collision.vec)* - The axis to reflect upon

##### *func* `dot(v)` &rarr; `int or float`

Returns the dot product of the vector and another

- `v` *(collision.vec)* - The other vector for the dot product

##### *func* `ln()` &rarr; `int or float`

Returns the length of the vector

##### *func* `ln2()` &rarr; `int or float`

Returns the squared length of the vector

------

### ***class*** `collision.Circle(pos, radius)`

A simple circle with a position and radius

**Properties:**

- `pos` *(collision.vec)* - The center coordinate of the circle
- `radius` *(int) or (float)* - The radius of the circle

**Methods:**

##### *func* `get_aabb()` &rarr; `collision.Poly`

Returns the AABB bounding box of the circle

------

### ***class*** `collision.Poly(pos, points)`

A convex polygon with a position, a list of points relative to that position, and an angle

**Properties:**

- `pos` *(collision.vec)* - The center coordinate of the circle
- `points` *(list[collision.vec])* - A list of points relative to the position. **These should be in counterclockwise order.** This property should not be directly changed.
- `angle` *(int) or (float)* - The angle which the polygon is rotated. Changing this will cause the polygon to be recalculated.

**Class Methods:**

##### *func* `Poly.from_box(pos, width, height)` &rarr; `collision.Poly`

Creates a polygon from

- `pos` *(collision.vec)* - The center coordinate of the polygon/box
- `width` *(int) or (float)* - The width of the box
- `height` *(int) or (float)* - The height of the box

**Methods:**

##### *func* `get_aabb()` &rarr; `collision.Poly`

Returns the AABB bounding box of the polygon

##### *func* `set_points(points)`

Change the base points relative to the position. After this is done, the polygon will be recalculated again. Angle will be preserved. Use this instead of editing the `points` property.

##### *func* `rotate(angle)`

Rotate all of the base points about the origin (position) of the polygon. This will cause a recalculation of the polygon.

- `angle` *(int) or (float)* - The angle to rotate the points


##### *func* `translate(v)`

Translate all of the base points relative to the origin (position) of the polygon. This will cause a recalculation of the polygon.

- `v` *(collision.vec)* - The vector to translate the poitnts with

##### *func* `get_centroid()` &rarr; `collision.vec`

Get the centroid of the polygon. The arithmatic mean of all of the points.


------

### ***class*** `collision.Response()`

The result of a collision between two objects. May optionally be passed to collision tests to retrieve additional information. At its cleared state, it may seem to have odd values. Ignore these, they are just there to make generating the response more efficient. The response should be ignored unless there is a sucessful collision.

**Properties:**

- `a` *(collision shape)* - The first object in the collision test
- `b` *(collision shape)* - The second object in the collision test
- `overlap` *(int) or (float)* - Magnitude of the overlap on the shortest colliding axis
- `overlap_n` *(collision.vec)* - The shortest colliding axis (unit vector)
- `overlap_v` *(collision.vec)* - The overlap vector. If this is subtracted from the position of `a`, `a` and `b` will no longer be colliding.
- `a_in_b` *(bool)* - Whether `a` is fully inside of `b`
- `b_in_a` *(bool)* - Whether `b` is fully inside of `a`

**Methods:**

##### *func* `clear()` &rarr; `collision.Response`

Clears the Response for re-use, and returns itself

# To be finished
