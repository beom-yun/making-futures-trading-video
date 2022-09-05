import pandas as pd


def read_csv_file(file):
    columns = ['주문번호', '체결번호', '종목코드', '종목명', '구분', "'주문가격/수량", 'LIMIT',
               'STOP', "'체결가/수량", '미체결', '상태', '원주문', '종류', '유효일',
               '주문시간', '체결시간', '통화', '거래소']

    try:
        df = pd.read_csv(file, skiprows=1, encoding='euc-kr')

        for column in columns:
            if column not in df.columns:
                print("'[4551] 해외선옵 주문체결상세' 확인")
                return None

        df.drop(columns=['주문번호', '체결번호', 'Unnamed: 6', "'주문가격/수량",
                         'LIMIT', 'STOP', '미체결', '상태', '종류', '원주문', '유효일', '체결시간'], inplace=True)
        df.rename(columns={"'체결가/수량": '체결가',
                  'Unnamed: 10': '수량'}, inplace=True)

        result = df_to_dict(df)
        return result if result else None
    except:
        print('get_csv error')
        return None


def df_to_dict(df):
    result = []
    new_transaction = {}

    try:
        for i in range(len(df)-1, -1, -1):
            if i % 2:
                for k, v in df.iloc[i].items():
                    new_transaction[k] = v
            else:
                new_transaction['청산가'] = df.iloc[i]['체결가']
                new_transaction['청산시간'] = df.iloc[i]['주문시간']
                result.append(new_transaction)
                new_transaction = {}
        return result
    except:
        print('df_to_dict error')
        return None


# if __name__ == '__main__':
    # ret = read_csv_file('example/[4551] 해외선옵 주문체결상세.csv')
#     for x in ret:
#         print(x)
