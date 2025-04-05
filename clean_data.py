import json
import pandas as pd

# Load the data from data.json
with open("data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Convert to DataFrame
df = pd.DataFrame(data)

# Convert column names to lowercase
df.columns = df.columns.str.lower()

# Convert strings back to arrays by splitting on commas and stripping whitespace
# Filter out empty strings that might come from trailing commas
df["job levels"] = df["job levels"].apply(
    lambda x: (
        [item.strip() for item in x.strip(",").split(",") if item.strip()] if x else []
    )
)
df["test type"] = df["test type"].apply(
    lambda x: (
        [item.strip() for item in x.strip(",").split(",") if item.strip()] if x else []
    )
)
df["languages"] = df["languages"].apply(
    lambda x: (
        [item.strip() for item in x.strip(",").split(",") if item.strip()] if x else []
    )
)

# Save the processed data with unescaped forward slashes
with open("processed_data.json", "w", encoding="utf-8") as f:
    json.dump(df.to_dict(orient="records"), f, indent=4, ensure_ascii=False)
