def l_set(p_act, h_room, PAR_OND, PAR_OFFD, l_man, l_last):
    """
    Tageslichtschaltung mit Hysterese.

    p_act:    Anwesenheit (True/False)
    h_room:   Raumhelligkeit in Lux
    PAR_OND:  Einschaltschwellwert in Lux  (z.B. 100)
    PAR_OFFD: Ausschaltschwellwert in Lux  (z.B. 300, muss > PAR_OND sein)
    l_man:    Manuelle Einschaltung (True/False)
    l_last:   Letzter Schaltzustand (True/False)
    """
    if l_man:
        return True
    if not p_act:
        return False
    if h_room < PAR_OND:
        return True
    if h_room > PAR_OFFD:
        return False
    return l_last
