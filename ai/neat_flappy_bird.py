import neat

from FlapPyBird import FlappyBirdGame, constants
from ai import visualize


def create_config(conf_file):
    # have everything set to default settings for now, can technically change the config file.
    return neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        conf_file
    )


def fitness(genomes, conf):
    """
    Runs one simulation for every genome and updates its fitness.
    Args:
        genomes: list of genomes.
        conf: configuration object for neat package.

    Returns:

    """
    # dispatch genomes to flappy bird instance
    # create a flappy bird game instance and pass it the genomes and configuration files
    # this will automatically set the genome fitnesses
    game_instance = FlappyBirdGame(genomes)


def run(epochs):
    conf_filepath = './ai/configs/flappy_ai.config'

    # make a config file
    conf = create_config(conf_filepath)
    constants.conf = conf

    # make a new population
    pop = neat.Population(conf)

    # make statistical reporters
    stats = neat.StatisticsReporter()
    pop.add_reporter(neat.StdOutReporter(True))
    pop.add_reporter(stats)

    # make a checkpointer to save progress every 10 epochs
    pop.add_reporter(neat.Checkpointer(10))

    # find the winner
    winner = pop.run(fitness, epochs)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    winner_net = neat.nn.FeedForwardNetwork.create(winner, conf)

    node_names = {-1: 'Pipe1 Midpt', -2: 'Pipe2 Midpt', -3: 'Height', -4:'Velocity', -5 : 'rotation', 0: 'FLAP'}
    visualize.draw_net(conf, winner, True, node_names=node_names)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)
