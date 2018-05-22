import cx_Oracle
import os
import time
from multiprocessing import Pool
from optparse import OptionParser


def benchmark(options):
    params = eval(options.bind) if options.bind else {}
    with cx_Oracle.connect(options.db) as db:
        try:
            cursor = db.cursor()
            before = time.clock()
            for i in range(options.requests):
                cursor.execute(options.sql, params)
            return (time.clock()-before)/options.requests
        except KeyboardInterrupt:
            pass
        finally:
            cursor.close()


class Orabench:
    def __init__(self, options):
        self.options = options
        print("Requests=%d, Concurrency=%d" % (self.options.requests,
                                               self.options.concurrency))

    def run(self):
        pool = Pool(processes=self.options.concurrency)
        result = pool.map_async(
            benchmark, [self.options]*self.options.concurrency)
        L = result.get()
        avg = sum(L)/len(L)
        print("Average=%.4f (%.4f requests per second)" % (avg, 1/avg))


if __name__ == "__main__":
    opt = OptionParser()
    opt.add_option("-d", "--database", help="EZCONNECT string", action="store",
                   type="string", dest="db")
    opt.add_option("-n", "--requests", help="number of requests", action="store",
                   type="int", dest="requests", default=10)
    opt.add_option("-c", "--concurrency", help="number of concurrent connections",
                   action="store", type="int", dest="concurrency", default=1)
    opt.add_option("-s", "--sql", help="SQL query or PL/SQL block",
                   action="store", type="string", dest="sql")
    opt.add_option("-b", "--bind", help="dictionary of bind parameters",
                   action="store", type="string", dest="bind")
    (options, args) = opt.parse_args()
    bench = Orabench(options)
    bench.run()
