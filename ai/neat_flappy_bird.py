import neat


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

    for gid, genome in genomes:
        # for each genome, repeat
        # define initial genome fitness
        # genome.fitness

        # run the network
        net = neat.nn.FeedForwardNetwork.create(genome, conf)

        # calculate and assign fitness
        for xi, xo in zip(train_input, train_output):
            pred = net.activate(xi)
            genome.fitness -= sd(pred[0], xo)
            # print('fitness of', gid, 'is', sd(pred[0], xo))


def run(epochs):
    conf_filepath = './configs/flappy_ai.config'

    # make a config file
    conf = create_config(conf_filepath)

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

    corr, total = 0., 0.

    for xi, xo in zip(test_inputs, test_outputs):
        output = winner_net.activate(xi)
        print("input {!r}, expected output {!r}, got {!r}".format(xi, xo, output), end='')
        if output[0] > 0.6:
            output = 1
        else:
            output = 0

        if abs(xo - output) < 0.05:
            corr += 1
            print(' [correct]')
        else:
            print(' [incorrect]')
        total += 1

    print("Test acc:", corr / total)
    node_names = {-1: 'A', -2: 'B', 0: 'A XOR B'}
    visualize.draw_net(conf, winner, True, node_names=node_names)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)


run(3000)
