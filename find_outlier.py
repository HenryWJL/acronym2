import sys
import argparse

def make_parser():
    parser = argparse.ArgumentParser(
        description="Find the meshes outliers.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--log_path",
        default="/home/wangjunlin/project/log.txt",
        help="The log file used for recording the terminal's output."
    )
    parser.add_argument(
        "--outlier_save_path",
        default="/home/wangjunlin/project/outlier.txt",
        help="The file used for storing the outliers."
    )
    return parser


def main(argv=sys.argv[1:]):
    parser = make_parser()
    args = parser.parse_args(argv)
    
    with open(args.log_path, 'r') as f:
        lines = f.readlines()
        
    outlier = []
    for idx in range(1, len(lines)):
        if (lines[idx].startswith('Output')):
            continue
        else:
            if (lines[idx - 1].startswith('Output')):
                continue
            else:
                outlier_fname = lines[idx - 1].split('/')[-1].split('.')[0]
                outlier.append(outlier_fname)
                
    with open(args.outlier_save_path, 'w') as f:
        outlier = [item + '\n' for item in outlier]
        f.writelines(outlier)


if __name__ == '__main__':
    main()
