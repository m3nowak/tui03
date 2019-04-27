from statistics import mean

from common import load_json
from tui_gen.models import parse_raw_course_dict
from tui_gen.gen_alg import genetic_algorithm


def test_pop_size(pop_sizes, cross_prob, mutate_prob, stale_val, prepared_dict, scoring_dict):

    for pop_size in pop_sizes:
        scores = []
        times = []
        generations = []
        for _ in range(10):
            alg_gen_report = genetic_algorithm(
                prepared_dict, pop_size, cross_prob,
                mutate_prob, stale_val, scoring_dict, False)

            scores.append(alg_gen_report.score)
            times.append(alg_gen_report.time_taken.total_seconds())
            generations.append(alg_gen_report.generations)
        print("pop_size  = {}\nscore,time,generations\n{}\t{}\t{}\n======"
              .format(pop_size, mean(scores), mean(times), mean(generations)))


def test_cross_prob(pop_size, cross_probs, mutate_prob, stale_val, prepared_dict, scoring_dict):
    for cross_prob in cross_probs:
        scores = []
        times = []
        generations = []
        for _ in range(10):
            alg_gen_report = genetic_algorithm(
                prepared_dict, pop_size, cross_prob,
                mutate_prob, stale_val, scoring_dict, False)

            scores.append(alg_gen_report.score)
            times.append(alg_gen_report.time_taken.total_seconds())
            generations.append(alg_gen_report.generations)
        print("cross_prob  = {}\nscore,time,generations\n{}\t{}\t{}\n======"
              .format(cross_prob, mean(scores), mean(times), mean(generations)))


def test_mutate_prob(pop_size, cross_prob, mutate_probs, stale_val, prepared_dict, scoring_dict):
    for mutate_prob in mutate_probs:
        scores = []
        times = []
        generations = []
        for _ in range(10):
            alg_gen_report = genetic_algorithm(
                prepared_dict, pop_size, cross_prob,
                mutate_prob, stale_val, scoring_dict, False)

            scores.append(alg_gen_report.score)
            times.append(alg_gen_report.time_taken.total_seconds())
            generations.append(alg_gen_report.generations)
        print("mutate_prob  = {}\nscore,time,generations\n{}\t{}\t{}\n======"
              .format(mutate_prob, mean(scores), mean(times), mean(generations)))


def test_stale_val(pop_size, cross_prob, mutate_prob, stale_vals, prepared_dict, scoring_dict):
    for stale_val in stale_vals:
        scores = []
        times = []
        generations = []
        for _ in range(100):
            alg_gen_report = genetic_algorithm(
                prepared_dict, pop_size, cross_prob,
                mutate_prob, stale_val, scoring_dict, False)

            scores.append(alg_gen_report.score)
            times.append(alg_gen_report.time_taken.total_seconds())
            generations.append(alg_gen_report.generations)
        print("stale_val  = {}\nscore,time,generations\n{}\t{}\t{}\n======"
              .format(stale_val, mean(scores), mean(times), mean(generations)))

def test_nothing(pop_size, cross_prob, mutate_prob, stale_val, prepared_dict, scoring_dict):
    scores = []
    times = []
    generations = []
    for _ in range(100):
        alg_gen_report = genetic_algorithm(
            prepared_dict, pop_size, cross_prob,
            mutate_prob, stale_val, scoring_dict, False)

        scores.append(alg_gen_report.score)
        times.append(alg_gen_report.time_taken.total_seconds())
        generations.append(alg_gen_report.generations)
    print("stale_val  = {}\nscore,time,generations\n{}\t{}\t{}\n======"
            .format(stale_val, mean(scores), mean(times), mean(generations)))

def main():
    #parser = argparse.ArgumentParser(description="PWR scheduling using genetic algorithm")
    #parser.add_argument('problem', help="JSON file of problem")

    #args = parser.parse_args()
    input_filepath = './artifacts/art15.json'

    raw_dict = load_json(input_filepath)
    prepared_dict = parse_raw_course_dict(raw_dict)
    scoring_dict = raw_dict.get("scoring", {})

    pop_sizes = [10, 20, 50, 100, 200]
    pop_size_def = 50
    cross_probs = [0.6, 0.7, 0.8]
    cross_prob_def = 0.7
    mutate_probs = [0.02, 0.05, 0.1, 0.15, 0.2]
    mutate_prob_def = 0.1
    stale_vals = [5, 10, 15, 20, 25]
    stale_val_def = 15
    #alg_gen_report = genetic_algorithm(
    #            prepared_dict, 200, 0.8,
    #            0.2, 20, scoring_dict)
    #print(alg_gen_report.printable_summary())
    test_stale_val(pop_size_def, cross_prob_def, mutate_prob_def,
                  stale_vals, prepared_dict, scoring_dict)


if __name__ == "__main__":
    main()
