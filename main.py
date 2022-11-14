from argparse import ArgumentParser
from etl import etl

# how to run:
# python main.py --db='test.sql' --tracks='unique_tracks.txt' --plays='triplets_sample_20p.txt' --amount_of_plays=100


def main():
    parser = ArgumentParser()
    parser.add_argument('--db', type=str, required=True)
    parser.add_argument('--tracks', type=str, required=True)
    parser.add_argument('--plays', type=str, required=True)
    parser.add_argument('--amount_of_plays', type=int)
    args = parser.parse_args()

    etl(args.db, args.tracks, args.plays, args.amount_of_plays)
    input("\n...")


if __name__ == '__main__':
    main()
