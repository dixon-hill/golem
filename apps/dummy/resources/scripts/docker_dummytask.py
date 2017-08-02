# TODO use functions from file other than this one - add computing.py to resources

from __future__ import print_function

import os
import hashlib
import random
import time

import params  # This module is generated before this script is run

"""Functions used in the computation of subtasks of the dummy task"""



def check_pow(proof, input_data, difficulty):
    """
    :param long proof:
    :param str input_data:
    :param int difficulty:
    :rtype bool:
    """
    sha = hashlib.sha256()
    sha.update(input_data)
    sha.update('%x' % proof)
    h = int(sha.hexdigest()[0:8], 16)
    return h <= difficulty


def find_pow(input_data, difficulty, result_size):
    """
    :param str input_data:
    :param int difficulty:
    :param int result_size:
    :rtype long:
    """
    num_bits = result_size * 4
    # This ensures that the generated number will not start with 0's as hex
    solution = (1 << (num_bits - 1)) | random.getrandbits(num_bits - 1)
    while True:
        if check_pow(solution, input_data, difficulty):
            return solution
        solution += 1


def run_dummy_task(data_file: str, subtask_string: str, difficulty: int, result_size: int):
    """Find a string S of result_size bytes such that the hash of the contents
    of the data_file, subtask_data and S produce sha256 hash H such that
    4 leftmost bytes of H is less or equal difficulty.
    :param str data_file: file with shared task data
    :param str subtask_string: subtask-specific part of data
    :param int difficulty: required difficulty
    :param int result_size: size of the solution string S
    :rtype DummyTaskResult\
    """
    print('[DUMMY TASK] computation started, data_file = ', data_file,
          ', result_size = ', result_size,
          ', difficulty = 0x%08x' % difficulty) # TODO remove that print
    t0 = time.clock()

    with open(data_file, 'r') as f:
        shared_input = f.read()
    solution = find_pow(shared_input + subtask_string, difficulty, result_size)
    result = '%x' % solution
    assert len(result) == result_size

    print('[DUMMY TASK] computation finished, time =', time.clock() - t0, 'sec')
    return {'data': result, 'result_type': 0}

OUTPUT_DIR = "/golem/output"
WORK_DIR = "/golem/work" # we don't need that, all the work is done in memory
RESOURCES_DIR = "/golem/resources"

def run(data_file, subtask_string, difficulty, result_size, out_file): # TODO types

    in_path = os.path.join(RESOURCES_DIR, data_file)
    out_path = os.path.join(OUTPUT_DIR, out_file)

    solution = run_dummy_task(in_path, subtask_string, difficulty, result_size)

    with open(out_path, "w") as f: #TODO try catch
        f.write("{}".format(solution))

# TODO send subtask data as string!
run(params.data_file, params.subtask_data, params.difficulty, params.result_size, params.result_file)