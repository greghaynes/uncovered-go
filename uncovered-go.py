from collections import namedtuple
import sys

func_id = namedtuple('func_id', ['file', 'start_lineno'])


def ignore_fid(fid):
    return (fid.file.endswith('generated.pb.go')
            or fid.file.endswith('generated.go'))


def main():
    cover_watermark = 5
    func_info = {}
    with open(sys.argv[1], 'r') as fh:
        for line in fh:
            func_file, _, cover_pct = line.split()
            try:
                func_file, start_lineno, _ = func_file.split(':')
            except ValueError:
                if line.startswith('total:'):
                    continue
            cover_num = float(cover_pct[:-1])
            fid = func_id(func_file, start_lineno)
            if ignore_fid(fid):
                continue
            func_info[fid] = (cover_num, None)

    with open(sys.argv[2], 'r') as fh:
        for line in fh:
            cyclo_str, _, sig, func_file = line.split()
            func_file, start_lineno, _ = func_file.split(':')
            cyclo = int(cyclo_str)
            fid = func_id(func_file, start_lineno)
            if ignore_fid(fid):
                continue
            try:
                finfo = func_info[fid]
            except KeyError:
                #print('Could not find %s:%s' % (fid.file, fid.start_lineno))
                continue
            func_info[fid] = (finfo[0], cyclo)

    filtered_finfos = filter(lambda x: x[1][1] != None and x[1][0] < 5,
                             func_info.items())
    sorted_finfos = list(sorted(filtered_finfos,
                                key=lambda x: x[1][1],
                                reverse=True))

    import pdb;pdb.set_trace()
    print('a')


if __name__ == '__main__':
    main()
