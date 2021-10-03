import csv
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple, Union

from puts.logger import logger

# local modules
from .constants import CODE, KEYWORDS
from .db_helpers import check_and_insert_one_record
from .models.record import Record


def get_record_obj(
    accountID: str,
    date: str,
    ref_code: str = "",
    debitAmount: str = "",
    creditAmount: str = "",
    ref_1: str = "",
    ref_2: str = "",
    ref_3: str = "",
    debug: bool = False,
) -> Record:
    # type check
    for i in (
        type(accountID),
        type(date),
        type(ref_code),
        type(debitAmount),
        type(creditAmount),
        type(ref_1),
        type(ref_2),
        type(ref_3),
    ):
        if i != str:
            raise TypeError
    ...
    accountID = accountID.strip()
    date = date.strip()
    ref_code = ref_code.strip()
    debitAmount = debitAmount.strip()
    creditAmount = creditAmount.strip()
    ref_1 = ref_1.strip()
    ref_2 = ref_2.strip()
    ref_3 = ref_3.strip()

    try:
        # debit (deduction from account)
        amount = -1 * float(debitAmount)
    except:
        # credit (addition to account)
        amount = float(creditAmount)

    date_obj: datetime = datetime.strptime(date, "%d %b %Y")
    # date_sortable: str = date_obj.strftime("%Y-%m-%d")
    bank_ref_code: str = CODE[ref_code] if ref_code in CODE else ref_code
    ref_long: str = ref_1 + " " + ref_2 + " " + ref_3
    label: str = ref_long
    for keyword in KEYWORDS:
        if keyword in ref_long:
            label = KEYWORDS[keyword]
            break

    ### some special cases for label classification
    special_case_map = {
        "Quick Cheque Deposit": "Cheque Deposit",
        "Funds Transfer": "Funds Transfer",
        "Cash Deposit Machine": "Cash Deposit",
        "Cash Withdrawal": "Cash Withdrawal",
        "Interest Earned": "Interest Earned",
        "Coin Deposit Fee": "Coin Deposit",
        "Coin Deposit Machine": "Coin Deposit",
    }
    if label == ref_long and bank_ref_code in special_case_map:
        label = special_case_map[bank_ref_code]

    rec: Record = Record(
        date_time=date_obj,
        account_id=accountID,
        amount=amount,
        label=label,
        bank_ref_code=bank_ref_code,
        reference=ref_long,
        imported=True,
    )
    return rec


def insert_records_from_csv(
    filepath: Union[str, Path], username: str, debug=False
) -> dict:
    accountID = ""
    statementDate = ""
    availableBalance = 0
    ledgerBalance = 0
    insertions_count = 0
    failed_insertions_count = 0
    records: List[Record] = []

    filepath: Path = Path(filepath)
    assert filepath.is_file()

    with filepath.open() as csvfile:
        spamreader = csv.reader(csvfile)

        for row in spamreader:
            if row == []:
                # this is an empty line
                pass
            elif "Account Details For:" in row:
                accountID = row[1].strip()
            elif "Statement as at:" in row:
                statementDate = row[1]
            elif "Available Balance:" in row:
                availableBalance = float(row[1].strip())
            # A ledger balance is a balance in an account at the beginning of each day
            elif "Ledger Balance:" in row:
                ledgerBalance = float(row[1].strip())
            elif "Transaction Date" in row:
                # this is the header row, ignore this row
                pass
            else:
                if len(row) == 8:
                    rec = get_record_obj(
                        accountID=accountID,
                        date=row[0].strip(),
                        ref_code=row[1].strip(),
                        debitAmount=row[2].strip(),
                        creditAmount=row[3].strip(),
                        ref_1=row[4].strip(),
                        ref_2=row[5].strip(),
                        ref_3=row[6].strip(),
                        debug=debug,
                    )
                elif len(row) == 9 or len(row) == 10:
                    rec = get_record_obj(
                        accountID=accountID,
                        date=row[0].strip(),
                        ref_code=row[1].strip(),
                        debitAmount=row[2].strip(),
                        creditAmount=row[3].strip(),
                        ref_1=row[4].strip(),
                        ref_2=row[5].strip() + " + " + row[6].strip(),
                        ref_3=row[7].strip(),
                        debug=debug,
                    )
                else:
                    logger.warning(f"Unexpected number of columns({len(row)})")
                    continue

                records.append(rec)
                try:
                    check_and_insert_one_record(rec, username)
                    insertions_count += 1
                except:
                    failed_insertions_count += 1

    data = {
        "accountID": accountID,
        "statementDate": statementDate,
        "availableBalance": availableBalance,
        "ledgerBalance": ledgerBalance,
        "records": records,
        "insertions_count": insertions_count,
        "failed_insertions_count": failed_insertions_count,
    }
    return data
