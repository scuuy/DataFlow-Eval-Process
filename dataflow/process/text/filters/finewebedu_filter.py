from dataflow.Eval.Text import FineWebEduScorer
from dataflow.core import TextFilter
import numpy as np
from dataflow.utils.registry import PROCESSOR_REGISTRY

@PROCESSOR_REGISTRY.register()
class FineWebEduFilter(TextFilter):

    def __init__(self, args_dict: dict):
        super().__init__(args_dict)
        self.min_score = args_dict['min_score']
        self.max_score = args_dict['max_score']
        scorer_args = args_dict.get('scorer_args', {})
        scorer_args['model_cache_dir'] = args_dict.get('model_cache_dir')
        self.scorer = FineWebEduScorer(scorer_args)
        self.filter_name = 'FineWebEduFilter'

    def filter_func(self, dataset):
        _, scores = self.scorer(dataset)
        metric_scores = np.array(scores['Default'])
        metric_filter = (self.min_score <= metric_scores) & (metric_scores <= self.max_score)
        return metric_filter.astype(int)
