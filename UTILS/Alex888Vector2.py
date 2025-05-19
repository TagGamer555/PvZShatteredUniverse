"""Alex888Vector2.py is a small library that implements a single class, Vector2, a 2D Vector, that aims towards general-purposeness.
To create an instance of the Vector2 class, simply give it:
* x and y as floats or integers
* None(s), which are interpreted as 0.0
* A list/tuple of values, the first two elements are picked as x and y
* A dictionary with x and y key-value pairs, which are assigned to x and y

Vector2 allows you to calculate:
* 2D Vector addition
* 2D Vector subtraction
* Multiplication of 2D Vector x and y values by a scalar or another 2D Vector
* Division of a 2D Vector x and y values by a scalar or another 2D Vector
* Dot and cross products of two 2D Vectors
* Logic operations: AND, OR, XOR, NAND, NOR, XNOR
* Angle between two 2D Vectors
* Swapped 2D Vectors with x and y values swapped
* 2D Vector with the reciprocal of values of the original 2D Vector
... And more! Use help(Vector2) to see all methods, including their docstrings."""

from math import hypot, acos, degrees, floor, ceil, sin, cos, radians, sqrt
import warnings

class ExtraItemsWarning(Warning): pass
class ThisIsNotFunnyWarning(Warning): pass

class Vector2:
    def __init__(self, x=0.0, y=0.0):
        # complex numbers
        if isinstance(x, complex): self.x = x.real; self.y = x.imag; return

        # lists and tuples
        # they work the same way, so we can pack them into one check
        if isinstance(x, (list, tuple)):
            if len(x) >= 2:
                # only pick the first 2 (and check if they're valid!)
                
                # do not print the whole list/tuple - only the relevant two values that were picked
                # and use ellipsis (as a string) to signify that there's more stuff

                if isinstance(x[0], (int, float)): self.x = x[0]
                elif x[0] is None: self.x = 0.0
                else: raise TypeError(f"The first item of the {type(x)} '{x[:2]+['...']}' is not a valid number or None")
                
                if isinstance(x[1], (int, float)): self.y = x[1]
                elif x[1] is None: self.y = 0.0
                else: raise TypeError(f"The second item of the {type(x)} '{x[:2]+['...']}' is not a valid number or None")

                if len(x) > 2: warnings.warn(f"The {type(x)} '{x[:2]+['...']}' contains more than 2 elements, - the rest will be ignored", ExtraItemsWarning)
                return
            else: raise TypeError(f"Input {type(x)} must have at least two values, got '{x}'")
        
        # dicts
        if isinstance(x, dict):
            if "x" in x and "y" in x:
                # check if x and y are valid values in the first place before assigning them

                if isinstance(x["x"], (int, float)): self.x = x["x"]
                elif x["x"] is None: self.x = 0.0
                else: raise TypeError(f"The 'x' value of the dict '{x}' is not a valid number or None, got {x["x"]}")

                if isinstance(x["y"], (int, float)): self.y = x["y"]
                elif x["y"] is None: self.y = 0.0
                else: raise TypeError(f"The 'y' value of the dict '{x}' is not a valid number or None, got {x["y"]}")

                keys = set(x.keys()); required = {"x", "y"}; has_extra_keys = bool(keys - required)
                if has_extra_keys: warnings.warn(f"The dict '{x}' contains more keys other than 'x' and 'y', - the rest will be ignored", ExtraItemsWarning)
                return
            raise TypeError(f"Incorrect dictionary format: '{x}'\nThe dictionary must have a key-value pair for both key 'x' and key 'y'")
        
        # special error if a set or frozenset is used (unordered - bad!)
        # be helpful and print lists if sets are used, and tuples if frozensets are used (dynamically adapts to whatever you're coding!)
        if isinstance(x, (set, frozenset)): raise TypeError(f"Cannot use '{x}', a {type(x)}, as they are unordered. It is required you use {'lists' if type(x) == set else 'tuples'} instead")

        # I thought of including this easter egg :)
        if x == False: self.x = 0.0; self.y = 0.0; warnings.warn("Why are you using 'False'? Is this some kind of joke I don't understand?", ThisIsNotFunnyWarning); return
        
        # reals and integers
        # also replace None with 0
        if isinstance(x, (int, float)): self.x = x
        elif x is None: self.x = 0.0
        else: raise TypeError(f"Vector2 x value must be a complex, list, tuple, dict, int, float, or None, but got '{x}'")
        if isinstance(y, (int, float)): self.y = y
        elif y is None: self.y = 0.0
        else: raise TypeError(f"Vector2 y value must be a int, float, or None, got '{y}'")

        # do a final conversion to guarantee we're dealing with floats regardless of what 'x' and 'y' were initially
        self.x = float(self.x); self.y = float(self.y)
    
    def __repr__(self): return f"Vector2({self.x}, {self.y})"
    def __str__(self): return f"2D Vector [{self.x}, {self.y}]"
    
    def __add__(self, other):
        """Add two 2D Vectors"""
        if type(self) == type(other): return Vector2(self.x + other.x, self.y + other.y)
        raise TypeError(f"Cannot add '{self}' to '{other}'")
    
    def __sub__(self, other):
        """Subtract one 2D Vector from another"""
        if type(self) == type(other): return Vector2(self.x - other.x, self.y - other.y)
        raise TypeError(f"Cannot subtract '{other}' from '{self}'")
    
    def __mul__(self, other):
        """Multiply a 2D Vector by a scalar or another 2D Vector"""
        if type(self) == type(other): return Vector2(self.x * other.x, self.y * other.y)
        elif isinstance(other, int) or isinstance(other, float): return Vector2(self.x * other, self.y * other)
        raise TypeError(f"Cannot multiply '{self}' by '{other}'")
    
    def __rmul__(self, scalar):
        """Perform a reserved multiplication of a 2D Vector by a scalar"""
        return self.__mul__(scalar)
    
    def __truediv__(self, other):
        """Divide a 2D Vector by a scalar or another 2D Vector"""
        if type(self) == type(other): return Vector2(self.x / other.x, self.y / other.y)
        elif isinstance(other, int) or isinstance(other, float): return Vector2(self.x / other, self.y / other)
        raise TypeError(f"Cannot divide '{self}' by '{other}'")
    
    def magnitude(self):
        """Return the magnitude of this 2D Vector"""
        return hypot(self.x, self.y)
    
    def normalize(self):
        """Return this 2D Vector normalized"""
        mag = self.magnitude() # cached to reduce the number of calculations
        return self / mag if mag != 0 else Vector2(0, 0)
    
    def dot(self, other):
        """Calculate dot product of two 2D Vectors"""
        if type(self) == type(other): return self.x * other.x + self.y * other.y
        raise TypeError(f"Cannot calculate dot product of '{self}' and '{other}'")
    
    def cross(self, other):
        """Calculate cross product of two 2D Vectors"""
        if type(self) == type(other): return self.x * other.y - self.y * other.x
        raise TypeError(f"Cannot calculate cross product of '{self}' and '{other}'")
    
    def angle_to(self, other):
        """Calculate the angle between two 2D Vectors in degrees
        If either of the 2D Vectors' magnitude is 0, it returns 0 without raising ZeroDivisionError"""
        if type(self) == type(other): 
            mag_product = self.magnitude() * other.magnitude() # cached to reduce the number of calculations
            return degrees(acos(self.dot(other) / (mag_product))) if (mag_product != 0) else 0.0 # output 0 (I pity you, coder...)
        raise TypeError(f"Cannot calculate angle from '{self}' to '{other}'")
    
    def distance_to(self, other):
        """Calculate the distance between two 2D Vectors"""
        if type(self) == type(other): return sqrt((other.x - self.x)**2 + (other.y - self.y)**2)
    
    def swapped(self):
        """Return this 2D Vector with x and y values swapped"""
        return Vector2(self.y, self.x)
    
    def mirror_x(self):
        """Return a new 2D Vector which has been mirrored along the x axis"""
        return Vector2(-self.x, self.y)
    
    def mirror_y(self):
        """Return a new 2D Vector which has been mirrored along the y axis"""
        return Vector2(self.x, -self.y)
    
    def mirror_xy(self):
        """Return a new 2D Vector which has been mirrored along the x and y axes"""
        return Vector2(-self.x, -self.y)
    
    def rotate_vector(self, angle):
        """Rotate this 2D Vector around the origin O(0,0) at certain angle in degrees"""
        if isinstance(angle, (float, int)):
            angle = radians(angle)
            return Vector2(self.x * cos(angle) - self.y * sin(angle), self.x * sin(angle) + self.y * cos(angle))
        raise ValueError(f"Angle must be a number, got {angle}")
    
    def reciprocal(self):
        """Return a 2D Vector values of which are reciprocals of this 2D Vector's x and y values"""
        new_x = 1/self.x if self.x != 0 else float('inf')
        new_y = 1/self.y if self.y != 0 else float('inf')
        return Vector2(new_x, new_y)
    
    def __eq__(self, other):
        """Equality check between this 2D Vector and other object, such as another 2D Vector
        If it's a 2D Vector comparison, compare the equality of their x and y values
        Otherwise, return False"""
        if type(self) == type(other): return self.x == other.x and self.y == other.y
        return False
    
    def __hash__(self):
        """Return a hashed version of this 2D Vector"""
        return hash((self.x, self.y))
    
    def __neg__(self):
        """Return a negated/inversed version of this 2D Vector"""
        return Vector2(-self.x, -self.y)
    
    def round(self):
        """Round this 2D Vector"""
        return Vector2(round(self.x), round(self.y))
    
    def floor(self):
        """Apply floor to this 2D Vector
        Floor removes all decimals after the decimal point"""
        return Vector2(floor(self.x), floor(self.y))
    
    def ceil(self):
        """Apply ceiling to this 2D Vector
        Ceiling removes the decimal point if it exists and adds +1
        If there was no decimal point to begin with, nothing happens"""
        return Vector2(ceil(self.x), ceil(self.y))
    
    def __iadd__(self, other):
        """Add two 2D Vectors via +="""
        if type(self) == type(other):
            self.x += other.x
            self.y += other.y
            return self
        raise TypeError(f"Cannot add '{self}' to '{other}'")

    def __isub__(self, other):
        """Subtract one 2D Vector from another via -="""
        if type(self) == type(other):
            self.x -= other.x
            self.y -= other.y
            return self
        raise TypeError(f"Cannot subtract '{other}' from '{self}'")

    def __imul__(self, other):
        """Multiply a 2D Vector by a scalar or a 2D Vector via *="""
        if type(self) == type(other):
            self.x *= other.x
            self.y *= other.y
            return self
        elif isinstance(other, (int, float)):
            self.x *= other
            self.y *= other
            return self
        raise TypeError(f"Cannot multiply '{self}' by '{other}'")

    def __itruediv__(self, other):
        """Divide a 2D Vector by a scalar or a 2D Vector via /="""
        if type(self) == type(other):
            self.x /= other.x
            self.y /= other.y
            return self
        elif isinstance(other, (int, float)):
            self.x /= other
            self.y /= other
            return self
        raise TypeError(f"Cannot divide '{self}' by '{other}'")
    
    def copy(self):
        """Returns a copy of this 2D Vector"""
        return Vector2(self.x, self.y)
    
    def AND(self):
        """Returns True if both x and y are not zero, otherwise False"""
        return True if self.x != 0.0 and self.y != 0.0 else False
    
    def OR(self):
        """Returns True if either x or y are not zero, otherwise False"""
        return True if self.x != 0.0 or self.y != 0.0 else False
    
    def XOR(self):
        """Returns True if either x or y are zero or not zero, but not both, otherwise False"""
        # bool(0.0) evaluates to False
        return True if bool(self.x) != bool(self.y) else False
    
    def NAND(self):
        """Returns True if either x or y are zero, otherwise False"""
        return not self.AND()
    
    def NOR(self):
        """Returns True if both x and y are zero, otherwise False"""
        return not self.OR()
    
    def XNOR(self):
        """Returns True if both x and y are either zero or not zero, but not either, otherwise False"""
        return not self.XOR()
    
    def to_list(self):
        """Return this 2D Vector as a list"""
        return [self.x, self.y]
    
    def to_tuple(self):
        """Return this 2D Vector as a tuple"""
        return (self.x, self.y)
    
    def to_dict(self):
        """Return this 2D Vector as a dict"""
        return {"x": self.x, "y": self.y}
    
    def to_range(self):
        """Return this 2D Vector as a range (both x and y are floored beforehand)"""
        return range(floor(self.x), floor(self.y))
    
    def min(self):
        """Return the smallest scalar part of this 2D Vector"""
        return min(self.x, self.y)
    
    def max(self):
        """Return the biggest scalar part of this 2D Vector"""
        return max(self.x, self.y)
    
    def eq(self):
        """Return True if both x and y values of this 2D Vector are equal, otherwise False"""
        return self.x == self.y
    
    def floor_eq(self):
        """Return True if both x and y floored values of this 2D Vector are equal, otherwise False"""
        return floor(self.x) == floor(self.y)
    
    def go_to_origin(self):
        """Center this 2D Vector at the origin O(0,0) and return it"""
        self.x, self.y = 0, 0
        return self
    
    def is_in_range(self, start_x, start_y, end_x, end_y):
        """Returns a tuple of boolean values, which contains two elements:
        * True if x value of this 2D Vector is between start_x and end_x, otherwise False
        * True if y value of this 2D Vector is between start_y and end_y, otherwise False"""
        # check if all of the input values are numbers
        if all([isinstance(i, (int, float)) for i in [start_x, start_y, end_x, end_y]]): return (start_x <= self.x <= end_x, start_y <= self.y <= end_y)
