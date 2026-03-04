def best_seller(sales):
    """
    Docstring para best_seller
    
    :param sales: Descripción
    """
    prodotto_top = None
    vendite_max = 0
    
    for prodotto, vendite in sales.items():
        if vendite > vendite_max:
            vendite_max = vendite
            prodotto_top = prodotto
                
    return prodotto_top


print(best_seller({'shirt': 20, 'jeans': 15, 'jacket': 5}))