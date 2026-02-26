def letter_frequency(text):
    """
    Docstring para letter_frequency
    
    :param text: Descripción
    """
    frequency = {}
    
    for char in text:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1
    return frequency


print(letter_frequency("banana"))
