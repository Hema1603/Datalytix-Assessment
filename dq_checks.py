def run_dq_checks(df, rules):

    report=[]

    for column,max_null in rules["null_rate"].items():

        rate=df[column].isna().mean()

        report.append({
            "rule":"null_rate",
            "column":column,
            "pass":rate<=max_null,
            "value":rate
        })

    for column in rules["unique"]:

        dup=df[column].duplicated().sum()

        report.append({
            "rule":"unique",
            "column":column,
            "pass":dup==0,
            "duplicates":dup
        })

    return report
