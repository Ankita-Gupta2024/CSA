def decimalToBinary(n):
    # converting decimal to binary
    # and removing the prefix(0b)
    return "{:032b}".format(n)

def binaryToDecimal(n):
    return int(n,2)

def twosCompliment(n):
    if n[0] == "0":
        return(int("0b" + n, 2))
    else:
        return -(
            -int(
                "0b" + n,
                2,
            )
            & 0b11111111111
        )

def reset(state):
    # state.EX["Read_data1"] = 0
    # state.EX["Read_data2"] = 0
    # state.EX["Imm"] = 0
    # state.EX["Rs"] = 0
    # state.EX["Rt"] = 0
    # state.EX["Wrt_reg_addr"] = 0
    state.EX["is_I_type"] = False
    state.EX["rd_mem"] = 0
    state.EX["wrt_mem"] = 0
    state.EX["alu_op"] = 0
    state.EX["wrt_enable"] = 0

def detectHazard(state, rs):
    
    if rs == state.EX["Wrt_reg_addr"] and state.MEM["rd_mem"]==0:
        # EX to 1st
        return state.MEM["ALUresult"]
    elif rs == state.WB["Wrt_reg_addr"] and state.WB["wrt_enable"]:
        # EX to 2nd
        # MEM to 2nd
        return state.WB["Wrt_data"]
    elif rs == state.MEM["Wrt_reg_addr"] and state.MEM["rd_mem"] != 0:
        # MEM to 1st
        state.EX["nop"] = True
        return state.WB["Wrt_data"]
    else:
        return 0
    
