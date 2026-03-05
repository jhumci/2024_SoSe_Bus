def map_lin(z):
    E_max = 1
    E_min = 0
    z_max = 65535
    z_min = 0
    beta_0 = E_min
    beta_1 = (E_max - E_min) / (z_max - z_min)
    return beta_0 + beta_1 * z

def map_log_log_lin(z):
    """
    Transformiert ADC-Werte in Lux-Werte basierend auf dem Log-Log-Fit:
    log10(Lux) = beta_1 * log10(ADC) + beta_0
    """
    # 1. Log-Transformation des Inputs
    log_z = np.log10(z)
    
    # 2. Lineares Mapping im Log-Raum (unter Verwendung der gefitteten Parameter)
    log_E = -2.3332 * log_z + 11.9614
    
    # 3. Rücktransformation (Exponentialfunktion zur Basis 10)
    return 10**log_E
