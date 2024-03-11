from climate_health.assessment.multi_location_evaluator import MultiLocationEvaluator
from ..data_fixtures import full_data, train_data, future_climate_data, good_predictions, bad_predictions
import pytest

@pytest.mark.xfail
def test_multi_location_evaluator(full_data, good_predictions, bad_predictions):
    evaluator = MultiLocationEvaluator(model_names=['bad_model', 'good_model'],
                                       truth=full_data)
    evaluator.add_predictions('good_model', good_predictions)
    evaluator.add_predictions('bad_model', bad_predictions)
    results = evaluator.get_results()
    assert results['good_model']['mae'] < results['bad_model']['mae']  # Output here should be synched up with plotting