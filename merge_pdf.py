from pypdf import PdfMerger


for year in [19, 20, 21, 22, 23]:
    for code in [11, 12, 13, 21, 22, 23]:
        for time in ['m', 's', 'w']:

            # print(code, code in [12, 22])
            # print(code, code in [12, 22], time, time != 'm')
            # if code not in [12, 22] and time == 'm':
            #     # print("CONTINUE")
            #     continue
            qp = f"pp\\0417_{time}{year}_qp_{code}.pdf"
            ms = f"pp\\0417_{time}{year}_ms_{code}.pdf"

            try:
                merger = PdfMerger()
                merger.append(qp)
                merger.append(ms)

                merger.write(f"ict\\0478_{time}{year}_qp_{code}.pdf")
                merger.close()

            except FileNotFoundError:
                continue
            print(qp, ms)