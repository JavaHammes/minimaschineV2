class Error():

    error_value = 0
    possible_values = [
        404, # Method name not existing
        403, # Too less elements
        402, # Wrong input (command)
        401, # Wrong input (value)
        400, # No HOLD
    ]

    def __init__(self, error_value):
        self.error_value = error_value

    def importance(self):
        importance_level = 0
        for value in self.possible_values:
            if self.error_value == value:
                return importance_level
            importance_level += 1

        return importance_level
