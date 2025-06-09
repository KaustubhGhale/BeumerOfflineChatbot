def evaluate_access(row):
    # Example Boolean logic: Access = True if Flight Destination is Mumbai and IATA is 6E
    destination = row.get('Flight Destination', '').strip().lower()
    iata = row.get('IATA', '').strip().upper()

    if destination == 'mumbai' and iata == '6E':
        return True
    return False
