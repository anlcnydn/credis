#!/usr/bin/env python
import patch_socket
import timeit, cProfile

import credis

rds = credis.Connection()
rds.connect()

def bench_simple():
    'the operation for benchmark'
    rds.execute(('SET', 'test', 100))

def bench_pipeline():
    pipe = [ ('SET', 1, 1),
             ('INCR', 1),
             ('INCRBY', 1, 1),
             ('GET', 1),
           ]
    rds.execute_pipeline(pipe)

bench = bench_pipeline

# record once
patch_socket.run_with_recording(rds._sock, bench)

timeit.main(['-s', 'from __main__ import patch_socket, rds, bench',
            '-n', '10000', 'patch_socket.run_with_replay(rds._sock, bench)'])

cProfile.run('for i in xrange(10000):patch_socket.run_with_replay(rds._sock, bench)',
             sort='time')

