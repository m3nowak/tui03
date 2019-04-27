"""
Module containing class descripting genetic algorithm solution and details.
"""

import hashlib

from tui_gen.gen_alg.rating import create_fenotype


class GeneticAlgorithmReport(object):
    """
    Class descripting genetic algorithm solution and details.
    """
    _WEEKNAMES = ["PON TN", "WTO TN", "ŚRO TN", "CZW TN",
                  "PIĄ TN", "PON TP", "WTO TP", "ŚRO TP", "CZW TP", "PIĄ TP"]
    _SUMMARY_TEMPLATE = """====
    Run for {total_s} s.
    Completed {iteration_count} iterations.
    Achieved score of {score}.
    Result visualization:
    {res_vis}
    Hash of solution:
    {hash}
    ===="""

    def __init__(self, final_chromosome, score, generations, time_taken):
        self.final_chromosome = final_chromosome
        self.score = score
        self.generations = generations
        self.time_taken = time_taken

    def printable_summary(self):
        """
        Generate printable summary.
        :return unicode: printable summary
        """

        fenotype = create_fenotype(self.final_chromosome)
        res_vis_list = ["=="]
        for day_index in range(10):
            res_vis_list.append(self._WEEKNAMES[day_index])
            for time_start, time_end, group_code in fenotype[day_index]:
                res_vis_list.append("{} - {} - ({})".format(
                    time_start.strftime('%H%M'), time_end.strftime('%H%M'), group_code))
            res_vis_list.append("==")
        res_vis = "\n".join(res_vis_list)

        hash_gen_obj = hashlib.md5()
        hash_gen_obj.update(res_vis.encode('utf8'))
        hash_hex = hash_gen_obj.hexdigest()

        return self._SUMMARY_TEMPLATE.format(total_s=self.time_taken.total_seconds(),
                                             iteration_count=self.generations,
                                             score=self.score,
                                             res_vis=res_vis,
                                             hash=hash_hex)
