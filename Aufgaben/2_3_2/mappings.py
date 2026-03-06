import math

LN10   = math.log(10)
BETA_1 = -2.3332
BETA_0 = 11.9614

def map_log_log_lin(z):
    """Rechnet ADC-Rohwert in Beleuchtungsstaerke (Lux) um."""
    if z < 1:
        z = 1
    log10_z = math.log(z) / LN10
    log10_E = BETA_1 * log10_z + BETA_0
    return math.exp(log10_E * LN10)
import math

def map_lin(z):
    U_max = 3.3
    U_min = 0
    z_max = 65535
    z_min = 0
    beta_0 = U_min
    beta_1 = (U_max - U_min) / (z_max - z_min)
    return beta_0 + beta_1 * z

BETA_1 = -2.3332
BETA_0 = 11.9614
LN10 = math.log(10)  # ≈ 2.302585

def map_log_log_lin(z):
    if z < 1:
        z = 1
    log10_z = math.log(z) / LN10
    log10_E = BETA_1 * log10_z + BETA_0
    return math.exp(log10_E * LN10)