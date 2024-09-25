# parameter_utils.py
# Contains utils used to calculate parameters and create user-friendly abstractions.

def get_inverse_instruction(instruction, asset_type):
    """
    Determine the inverse instruction based on the current instruction and asset type.

    :param instruction: The original instruction (e.g., "BUY", "SELL", etc.).
    :param asset_type: The asset type (either "EQUITY" or "OPTION").
    :return: The inverse instruction.
    """
    
    # Define the inverse logic based on the asset type
    if asset_type == "EQUITY":
        inverse_instruction = {
            "BUY": "SELL",
            "SELL": "BUY",
            "BUY_TO_COVER": "SELL_SHORT",
            "SELL_SHORT": "BUY_TO_COVER"
        }.get(instruction, None)
    elif asset_type == "OPTION":
        inverse_instruction = {
            "BUY_TO_OPEN": "SELL_TO_CLOSE",
            "SELL_TO_CLOSE": "BUY_TO_OPEN",
            "SELL_TO_OPEN": "BUY_TO_CLOSE",
            "BUY_TO_CLOSE": "SELL_TO_OPEN"
        }.get(instruction, None)
    else:
        raise ValueError(f"Invalid asset type: {asset_type}")

    if inverse_instruction is None:
        raise ValueError(f"Invalid instruction: {instruction} for asset type: {asset_type}")

    return inverse_instruction
