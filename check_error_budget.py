import sys
import random
import time

# Simulated error budget check using mocked availability metric

# Configuration
SLO_THRESHOLD = 0.999  # e.g. 99.9% availability required

# Simulate a dynamic availability result (mocked for CI/CD demo)
# You can hard-code for a specific result, or randomise to simulate both outcomes
mock_availability = random.choice([0.998, 0.9991, 0.9975, 1.0])  # Random example values

# Print the simulated availability
print(" Simulating availability check...")
time.sleep(1)
print(f"ℹ  Simulated availability: {mock_availability * 100:.2f}%")

# Compare to SLO threshold
if mock_availability < SLO_THRESHOLD:
    print(" SLO violated. Deployment should be halted.")
    sys.exit(1)  # Fail the pipeline
else:
    print(" SLO met. Proceeding with deployment.")
    sys.exit(0)  # Allow deployment
