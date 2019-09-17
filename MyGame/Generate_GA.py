import airplane_backend_class as Gee
import airplane_backend_variables as val

play = Gee.GeneticAlgorithmClass()

if val.Running_mode == 'development':
    play.generating()
    play.printing_sequence_data()
