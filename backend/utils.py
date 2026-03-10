import math

def evaluate_expression(expression: str, unit_mode: str = 'degrees') -> str:
    """
    Safely evaluates a mathematical expression using Python's math module,
    respecting the specified unit mode for trigonometric functions.
    """
    # Define a restricted set of allowed globals to prevent arbitrary code execution.
    allowed_globals = {
        '__builtins__': None, # Disable built-in functions for security
        'pi': math.pi,
        'e': math.e,
        'abs': abs,
        'round': round,
        'min': min,
        'max': max,
        'sqrt': math.sqrt,
        'log': math.log,
        'log10': math.log10,
        'exp': math.exp,
        'ceil': math.ceil,
        'floor': math.floor,
        'pow': math.pow,
    }

    # Wrap trigonometric functions to handle 'degrees' or 'radians' conversion.
    if unit_mode == 'degrees':
        allowed_globals['sin'] = lambda x: math.sin(math.radians(x))
        allowed_globals['cos'] = lambda x: math.cos(math.radians(x))
        allowed_globals['tan'] = lambda x: math.tan(math.radians(x))
        allowed_globals['asin'] = lambda x: math.degrees(math.asin(x)) # arcsin result in degrees
        allowed_globals['acos'] = lambda x: math.degrees(math.acos(x))
        allowed_globals['atan'] = lambda x: math.degrees(math.atan(x))
    elif unit_mode == 'radians':
        allowed_globals['sin'] = math.sin
        allowed_globals['cos'] = math.cos
        allowed_globals['tan'] = math.tan
        allowed_globals['asin'] = math.asin
        allowed_globals['acos'] = math.acos
        allowed_globals['atan'] = math.atan
    else:
        raise ValueError("Invalid unit mode. Must be 'degrees' or 'radians'.")

    try:
        # Evaluate the expression using the restricted globals and an empty locals dictionary.
        result = eval(expression, allowed_globals, {})
        
        # Format floating point results to avoid excessive precision and convert to int if whole number
        if isinstance(result, (float, int)):
            if float(result).is_integer():
                return str(int(result))
            return f"{result:.10f}".rstrip('0').rstrip('.')
        return str(result)
    except (SyntaxError, TypeError, NameError, ValueError, ZeroDivisionError, OverflowError) as e:
        # Catch common evaluation errors and re-raise as a ValueError for API error handling.
        raise ValueError(f"Invalid expression or calculation error: {e}")
    except Exception as e:
        # Catch any other unexpected errors.
        raise ValueError(f"An unexpected error occurred during evaluation: {e}")

