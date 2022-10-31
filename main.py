from argparse import ArgumentParser


def save_to_db(db, tracks, sample):
    tracks = open(tracks, 'r', errors="ignore")
    sample = open(sample, 'r', errors="ignore")
    data1 = tracks.readline()
    data2 = sample.readline()
    print(data1)
    print(data2)
    return


def main():
    parser = ArgumentParser()
    parser.add_argument('--db', type=str, required=True)
    parser.add_argument('--tracks', type=str, required=True)
    parser.add_argument('--sample', type=str, required=True)
    args = parser.parse_args()

    save_to_db(args.db, args.tracks, args.sample)
    input()


if __name__ == '__main__':
    main()
