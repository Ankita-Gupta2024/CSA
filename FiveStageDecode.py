from conversion import *

def FS_decode(state,register):
    reset(state)
    instruction = state.ID["Instr"]

    #R-type---------------------------------------------------------------------------------

    if instruction[-7:] == "0110011":  
        state.EX["Rs"] = instruction[-20:-15]
        state.EX["Rt"] = instruction[-25:-20]
        state.EX["Wrt_reg_addr"] = instruction[-12:-7]

        rs1 = binaryToDecimal(state.EX["Rs"])
        rs2 = binaryToDecimal(state.EX["Rt"])
        state.EX["Wrt_reg_addr"] = binaryToDecimal(state.EX["Wrt_reg_addr"])

        if detectHazard(state, rs1) != 0:
            state.EX["Read_data1"] = detectHazard(state, rs1)
        else:
            state.EX["Read_data1"] = register.readRF(rs1)
        
        if detectHazard(state, rs2) != 0:
            state.EX["Read_data2"] = detectHazard(state, rs2)
        else:
            state.EX["Read_data2"] = register.readRF(rs2)
        

        state.EX["wrt_enable"] = 1
        state.EX["is_I_type"] = False

        if instruction[-15:-12] == "000" and instruction[-32:-25] == "0000000":
            # add func
            state.EX["alu_op"] = "add"

        elif instruction[-15:-12] == "000" and instruction[-32:-25] == "0100000":
            # sub func
            state.EX["alu_op"] = "sub"

        elif instruction[-15:-12] == "100" and instruction[-32:-25] == "0000000":
            # xor func
            state.EX["alu_op"] = "xor"

        elif instruction[-15:-12] == "110" and instruction[-32:-25] == "0000000":
            # or func
            state.EX["alu_op"] = "or"

        elif instruction[-15:-12] == "111" and instruction[-32:-25] == "0000000":
            # AND func
            state.EX["alu_op"] = "and"

    #I-type ---------------------------------------------------------------------------------


    elif instruction[-7:] == "0010011":  # I-type
        state.EX["Rs"] = instruction[-20:-15]
        state.EX["Imm"] = instruction[-32:-20]
        state.EX["Wrt_reg_addr"] = instruction[-12:-7]
        
        rs1 = binaryToDecimal(state.EX["Rs"])
        state.EX["Wrt_reg_addr"] = binaryToDecimal(state.EX["Wrt_reg_addr"])

        if detectHazard(state, rs1) != 0:
            state.EX["Read_data1"] = detectHazard(state, rs1)
        else:
            state.EX["Read_data1"] = register.readRF(rs1)

        state.EX["is_I_type"] = True
        state.EX["wrt_enable"] = 1

        if instruction[-15:-12] == "000":
            # Addi func
            state.EX["alu_op"] = "addi"

        elif instruction[-15:-12] == "100":
            # xori
            state.EX["alu_op"] = "xori"

        elif instruction[-15:-12] == "110":
            # ori
            state.EX["alu_op"] = "ori"

        elif instruction[-15:-12] == "111":
            # andi
            state.EX["alu_op"] = "andi"
    
    #Load-type --------------------------------------------------------------------
    
    elif instruction[-7:] == "0000011":  
        state.EX["Rs"] = instruction[-20:-15]
        state.EX["Imm"] = instruction[-32:-20]
        state.EX["Wrt_reg_addr"] = instruction[-12:-7]

        rs1 = binaryToDecimal(state.EX["Rs"])   
        state.EX["Wrt_reg_addr"] = binaryToDecimal(state.EX["Wrt_reg_addr"])

        if detectHazard(state, rs1) != 0:
            state.EX["Read_data1"] = detectHazard(state, rs1)
        else:
            state.EX["Read_data1"] = register.readRF(rs1)

        state.EX["rd_mem"] = 1
        state.EX["wrt_enable"] = 1
        state.EX["is_I_type"] = True
        state.EX["alu_op"] = "lw"
        
    #Store-type ---------------------------------------------------------------------------------------

    elif instruction[-7:] == "0100011": 
        state.EX["Rs"] = instruction[-20:-15]
        state.EX["Imm"] = "".join((instruction[-32:-25], instruction[-12:-7]))
        state.EX["Rt"] = instruction[-25:-20]

        rs1 = binaryToDecimal(state.EX["Rs"])
        rs2 = binaryToDecimal(state.EX["Rt"])

        if detectHazard(state, rs1) != 0:
            state.EX["Read_data1"] = detectHazard(state, rs1)
        else:
            state.EX["Read_data1"] = register.readRF(rs1)
        
        if detectHazard(state, rs2) != 0:
            state.EX["Read_data2"] = detectHazard(state, rs2)
        else:
            state.EX["Read_data2"] = register.readRF(rs2)

        state.EX["is_I_type"] = True
        state.EX["wrt_mem"] = 1
        state.EX["alu_op"] = "sw"

    #Branch-type --------------------------------------------------------------------

    elif instruction[-7:] == "1100011":

        state.EX["Rs"] = instruction[-20:-15]
        state.EX["Imm"] = "".join(
            (
                instruction[-32],
                instruction[-8],
                instruction[-31:-25],
                instruction[-12:-8],
                "0",
            )
        )
        state.EX["Rt"] = instruction[-25:-20]

        rs1 = binaryToDecimal(state.EX["Rs"])
        rs2 = binaryToDecimal(state.EX["Rt"])

        if detectHazard(state, rs1) != 0:
            state.EX["Read_data1"] = detectHazard(state, rs1)
        else:
            state.EX["Read_data1"] = register.readRF(rs1)
        
        if detectHazard(state, rs2) != 0:
            state.EX["Read_data2"] = detectHazard(state, rs2)
        else:
            state.EX["Read_data2"] = register.readRF(rs2)

        state.EX["is_I_type"] = True

        if instruction[-15:-12] == "000":
            # BEQ func
            state.EX["alu_op"] = "beq"

        elif instruction[-15:-12] == "001":
            # BNE
            state.EX["alu_op"] = "bne"

    #JAL-type ---------------------------------------------------------------------------------------------------------
    
    elif instruction[-7:] == "1101111":  
        state.EX["Imm"] = "".join((instruction[-32], instruction[-20:-12], instruction[-21],instruction[-31:-21] ))
        state.EX["Wrt_reg_addr"] = instruction[-12:-7]
        state.EX["Wrt_reg_addr"] = binaryToDecimal(state.EX["Wrt_reg_addr"])
        state.EX["wrt_enable"] = 1
        state.EX["alu_op"] = "jal"
    
    else:
        state.IF["nop"] = True

    if state.EX["is_I_type"]:
        state.EX["Imm"] = twosCompliment(state.EX["Imm"])
        