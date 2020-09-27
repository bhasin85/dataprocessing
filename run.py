import argparse

from data_processor import DataProcessor
from file_parser import FileParser

parser = argparse.ArgumentParser()
parser.add_argument('--spec_file', help='Spec file', required=True, default="spec.json")
parser.add_argument('--type', choices=['fp', 'dp'], help='Options: fp-> file processor, dp-> data processor', required=True)

parser.add_argument('--lines', help='Number of lines of sample data', default=10)
parser.add_argument('--generate_fix_width_file', help='Generate fixed width file')
parser.add_argument('--fix_width_file', help='Fixed width file for delimited file')
parser.add_argument('--generate_delimited_file', help='Generate delimited file')
parser.add_argument('--generate_csv_file', help='Generate CSV file')
parser.add_argument('--csv_file', help='CSV file to hash')
parser.add_argument('--hash_csv_file', help='Hashed CSV file')
args = parser.parse_args()


if args.type == 'fp':
    fp = FileParser(spec_file=args.spec_file)
    if args.generate_fix_width_file:
        if args.lines:
            fp.generate_fixed_width_file(fixed_width_file=args.generate_fix_width_file, lines_count=args.lines)
        else:
            fp.generate_fixed_width_file(fixed_width_file=args.generate_fix_width_file)
    elif args.generate_delimited_file:
        fp.generate_delimited_file(fixed_width_file=args.fix_width_file,
                                   delimited_file=args.generate_delimited_file)
elif args.type == 'dp':
    dp = DataProcessor(spec_file=args.spec_file)
    if args.generate_csv_file:
        if args.lines:
            dp.generate_csv_file(csv_file=args.generate_csv_file, lines_count=args.lines)
        else:
            dp.generate_csv_file(csv_file=args.generate_csv_file)
    elif args.hash_csv_file:
        dp.hash_csv_file(csv_file=args.csv_file, hash_file=args.hash_csv_file)
