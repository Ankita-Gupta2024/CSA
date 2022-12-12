def check_rf_output(testcase, stage):
    output = []
    expected = []
    with open(f"testcases\\TC{testcase}\\ExpectedResults\\{stage}_RFResult.txt", "r") as f:
        temp = f.readlines()
        for line in temp:
            if not ("State" in line or "----" in line):
                expected.append(line)
    with open(f"testcases\\TC{testcase}\\{stage}_RFResult.txt", "r") as f:
        temp = f.readlines()
        for line in temp:
            if not ("State" in line or "----" in line):
                output.append(line)

    return expected == output


def check_demem_output(testcase, stage):
    output = []
    expected = []
    with open(
        f"testcases\\TC{testcase}\\ExpectedResults\\{stage}_DMEMResult.txt", "r"
    ) as f:
        expected = f.readlines()
    with open(f"testcases\\TC{testcase}\\{stage}_DMEMResult.txt", "r") as f:
        output = f.readlines()
    return expected == output


for i in range(5):
    
    
    
    
    
