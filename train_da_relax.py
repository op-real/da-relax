import os
import argparse
import importlib

from da_relax.train import da_learner

from da_relax.tools import flag_tools
from da_relax.tools import timer_tools
from da_relax.tools import logging_tools


parser = argparse.ArgumentParser()
parser.add_argument('--log_base_dir', type=str, 
        default=os.path.join(os.getcwd(), 'log'))
parser.add_argument('--log_sub_dir', type=str, default='test')
parser.add_argument('--exp_name', type=str, default='toy_example')
parser.add_argument('--config_dir', type=str, default='da_relax.configs')
parser.add_argument('--config_file', type=str, default='toy_config')
parser.add_argument('--args', type=str, action='append', default=[])


FLAGS = parser.parse_args()


def get_config_cls():
    config_module = importlib.import_module(
            FLAGS.config_dir+'.'+FLAGS.config_file)
    config_cls = config_module.Config
    return config_cls


def main():
    timer = timer_tools.Timer()
    if FLAGS.log_sub_dir == 'auto_d':
        FLAGS.log_sub_dir = logging_tools.get_datetime()
    if FLAGS.log_sub_dir == 'auto_n':
        FLAGS.log_sub_dir = logging_tools.get_unique_dir()
    # pass args to config
    cfg_cls = get_config_cls()
    flags = flag_tools.Flags()
    flags.log_dir = os.path.join(
            FLAGS.log_base_dir,
            FLAGS.exp_name,
            FLAGS.log_sub_dir)
    flags.env_id = FLAGS.env_id
    flags.args = FLAGS.args
    logging_tools.config_logging(flags.log_dir)
    repr_ckpt = os.path.join(FLAGS.log_base_dir, FLAGS.repr_ckpt_sub_path)
    setattr(flags, 'repr_model_cfg.model_ckpt', repr_ckpt)
    flags.reward_mode = FLAGS.reward_mode
    ##
    cfg = cfg_cls(flags)
    flag_tools.save_flags(cfg.flags, flags.log_dir)
    agent = dqn_repr_agent.DqnReprAgent(**cfg.args)
    agent.train()
    print('Total time cost: {:.4g}s.'.format(timer.time_cost()))


if __name__ == '__main__':
    main()