""" 
This module contains exceptions used by the verilog to gds module
"""

__all__ = ('ParsingError','CellNotFound','PinNotDefined','MissingMetalLayers','WrongInstanceName','NoHorizontalTracks')

class ParsingError(Exception):
    """ Base class for all parsing errors"""

class CellNotFound(ParsingError):
    """ Raised when a cell name is given but not found in a cell library"""

class PinNotDefined(ParsingError):
    """ Raised when there are no pin layers in layermap file """

class MissingMetalLayers(ParsingError):
    """ Raised when there are no metal layers in layermap file """

class WrongInstanceName(ParsingError):
    """ Raised when instance name does not follow the convention for matrices and single cells """

class NoHorizontalTracks(ParsingError):
    """ Raised when there are no available horizontal tracks """
