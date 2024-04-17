from typing import Union

from pydantic import BaseModel


class Bivariate(BaseModel):
    """
    Represents a bivariate attribute with two dimensions, X and Y.

    This class can be used to represent dimensions such as screen resolution or physical size.

    Fields:
        - x : The first dimension, which could represent width.
        - y : The second dimension, which could represent height.

    Example:
        - A screen resolution of 2560(X) x 1600(Y) pixels.
        - A picture frame size of 14.5(X) x 19.5(Y) cm.
    """
    x: Union[float, int]
    y: Union[float, int]


class Trivariate(Bivariate):
    """
    Extends the Bivariate class to include a third dimension, Z.

    This class is suitable for representing three-dimensional attributes such as the size of a physical object.

    Fields:
        z : The third dimension, which could represent depth.

    Example:
        - A bookshelf dimension of 256.3(X) x 145.5(Y) x 14.5(Z) cm.
    """
    z: Union[float, int]