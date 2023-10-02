from data import preprocess_data
from heston_model import HestonModel
from optimizer import error_func, genetic_optimizer, ModelParams
from plots import MARKET_DATA_VS_MODEL_PREDICTION, VOLATILITY_SURFACE

# Initialize data
S0 = 1590.75  # As per 19 Aug 2023
df = preprocess_data()

# Optimize (kappa, theta, v0, rho, n)
# params = genetic_optimizer(10, df, S0)[0]
params = [0.12238657453694513, 0.045856009966231126, 0.022798199341096836, -0.024794244048504166, 0.8215528911870628]
# Error = 0.028

kappa, theta, v0, rho, n = params
model = HestonModel(n, rho, kappa, theta, v0, 0.072)

# Create Plots
MARKET_DATA_VS_MODEL_PREDICTION(model, S0, df)
VOLATILITY_SURFACE(model, S0,  model.r)
