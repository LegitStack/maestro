"""
Just put pickles for use with importlib.resources in here.

# bins:
we have pull data/models/<model_name>/labels/bins.pkl as bins.vector.pkl

# xgboost and lightgbm feature lists:
we have pull data/models/<model_name>/labels/xgb_feature.pkl as xgb_feature.pkl
we have pull data/models/<model_name>/labels/lgb_feature.pkl as lgb_feature.pkl

# labels for the bins:
we have pull data/models/<model_name>/labels/dmap.pkl as dmap.pkl

we have pull data/models/<model_name>/glm/MyGLM_base.pkl as model.glmbase.pkl
we have pull data/models/<model_name>/xgboost_lightgbm/lightgbm.pkl as lightgbm.booster.pkl
we have pull data/models/<model_name>/xgboost_lightgbm/xgboost.pkl as xgboost.pipeline.pkl

we have pull data/interim/<model_name>/experian_input.pkl as input.df.pkl
we have pull data/interim/<model_name>/experian_bizaggs.pkl as bizaggs.df.pkl
we have pull data/interim/<model_name>/experian_scored.pkl as scored.df.pkl

Also, once it's a script, say which script produces these files.
"""
