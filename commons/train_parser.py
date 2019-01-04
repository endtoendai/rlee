"""
argument_parser.py
"""
import argparse


def get_train_args(description='endtoendai/baselines', default_args=None):
    """
    Parse arguments for training agents and return hyperparameters as a
    Namespace.

    Parameters
    ----------
    description: str
        Description for the argument parser. Defaults to endtoendai/baselines.

    Returns
    -------
    args
        Namespace containing hyperparameter options specified by user or set
        by default.
    """

    parser = argparse.ArgumentParser(description)
    parser.add_argument('--env-id', action='store', dest='ENV_ID',
                        default='Pong', type=str,
                        help='Environment to train the agent in. Defaults to Pong.')
    parser.add_argument('--agent', action='store', dest='AGENT',
                        default='dqn2015', type=str,
                        help='Environment to train the agent in. Defaults to dqn2015.')

    # Hyperparameters for DQN
    parser.add_argument('--nb-steps', action='store', dest='NB_STEPS',
                        default=10000000, type=int,
                        help='Number of steps for training DQN.')
    parser.add_argument('--discount', action='store', dest='DISCOUNT',
                        default=0.99, type=float,
                        help='Discount factor for DQN.')
    parser.add_argument('--target-update-freq', action='store', dest='TARGET_UPDATE_FREQ',
                        default=10000, type=int,
                        help='Target network update frequency for DQN.')
    parser.add_argument('--no-huber-loss', action='store_true', dest='NO_HUBER_LOSS',
                        help='Disable Huber loss (Smooth L1 loss).')
    parser.add_argument('--eval-freq', action='store', dest='EVAL_FREQ',
                        default=10, type=int,
                        help='Evaluate agent after every N training episodes. Defaults to 10.')

    # Hyperparameters for RMSprop
    # https://twitter.com/FlorinGogianu/status/1080139414695759872
    # TODO Check weight decay hyperparameter again: is this the missing 0.95 hyperparameter?
    parser.add_argument('--rmsprop-lr', action='store', dest='RMSPROP_LR',
                        default=2.5e-4, type=float,
                        help='RMSprop learning rate. Defaults to 2.5e-4')
    parser.add_argument('--rmsprop-alpha', action='store', dest='RMSPROP_ALPHA',
                        default=0.95, type=float,
                        help='RMSprop smoothing constant. Defaults to 0.95')
    parser.add_argument('--rmsprop-eps', action='store', dest='RMSPROP_EPS',
                        default=0.01, type=float,
                        help='RMSprop constant term in denominator to improve numerical stability . Defaults to 0.01')
    parser.add_argument('--rmsprop-weight-decay', action='store', dest='RMSPROP_WEIGHT_DECAY',
                        default=0, type=float,
                        help='RMSprop weight decay . Defaults to 0.')
    parser.add_argument('--rmsprop-momentum', action='store', dest='RMSPROP_MOMENTUM',
                        default=0, type=float,
                        help='RMSprop momentum . Defaults to 0.')
    parser.add_argument('--rmsprop-not-centered', action='store_true', dest='RMSPROP_NOT_CENTERED',
                        help='RMSprop is not centered. Defaults to False.')

    # Hyperparameters for Replay Buffer
    parser.add_argument('--replay-buffer-size', action='store', dest='REPLAY_BUFFER_SIZE',
                        default=1000000, type=int,
                        help='Size of the experience replay buffer. Defaults to 1000000')
    parser.add_argument('--batch-size', action='store', dest='BATCH_SIZE',
                        default=32, type=int,
                        help='Batch size for sampling from experience replay buffer. Defaults to 32.')
    parser.add_argument('--min-replay-buffer-size', action='store', dest='MIN_REPLAY_BUFFER_SIZE',
                        default=10000, type=int,
                        help='Minimum replay buffer size before sampling. Defaults to 32.')

    # Hyperparameters for epsilon decay
    parser.add_argument('--epsilon-decay-start', action='store', dest='EPSILON_DECAY_START',
                        default=1, type=float,
                        help='Starting epsilon value. Defaults to 1.')
    parser.add_argument('--epsilon-decay-final', action='store', dest='EPSILON_DECAY_FINAL',
                        default=0.1, type=float,
                        help='Minimum epsilon value. Defaults to 0.1.')
    parser.add_argument('--epsilon-decay-duration', action='store', dest='EPSILON_DECAY_DURATION',
                        default=1000000, type=int,
                        help='Number of frames to decay epsilon for. Defaults to 1000000.')

    args = parser.parse_args()

    if args.ENV_ID not in ['Pong']:
        raise ValueError('{} is not a supported environment.'.format(args.ENV_ID))

    args.USE_HUBER_LOSS = not args.NO_HUBER_LOSS
    args.RMSPROP_CENTERED = not args.RMSPROP_NOT_CENTERED

    return args
