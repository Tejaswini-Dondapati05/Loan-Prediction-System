import joblib

model = joblib.load("loan_id.pkl")

print("MODEL TYPE:")
print(type(model))

print("\nMODEL:")
print(model)

print("\nMODEL STEPS:")

if hasattr(model, "named_steps"):
    for name, step in model.named_steps.items():
        print(name, "=>", type(step))

print("\nHAS PREPROCESSOR:")

if hasattr(model, "named_steps"):
    print("preprocessor" in model.named_steps)