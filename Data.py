import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Generate a log-normal distribution of 50 random numbers with mean=3 and sigma=0.5
np.random.seed(5)
hcp = np.random.lognormal(mean=3, sigma=0.5, size=50)
# # create the one dimentional data to calculate it's statistics to evaluate the generated dataset


# Generating the HCD dataset using the Gamma distribution model
hcd = np.random.gamma(shape=8, scale=37.50, size=50)


# # save the data

# Now let's generate the BCA dataset using the normal distribution model


np.random.seed(6)

batch_factor = np.random.normal(
    loc=0,
    scale=1,
    size=50
)


np.random.seed(10)

bca_noise = np.random.normal(
    loc=0,
    scale=40,
    size=50
)

bca = 500 + (35 * batch_factor) + bca_noise
# print("Mean:", np.mean(bca))
# print("Median:", np.median(bca))
# print("SD:", np.std(bca, ddof=1))
# print("Minimum:", np.min(bca))
# print("Maximum:", np.max(bca))

# correlation = np.corrcoef(batch_factor, bca)[0, 1]
# print("Correlation:", correlation)

# Now create the D-Ag dataset uusing Beta distribution model
np.random.seed(5)

alpha = 8
beta = 3

dAg_beta = np.random.beta(alpha, beta, size=50)

dAg = 0.13 + dAg_beta * (4 - 0.13)
# print("Mean:", np.mean(dAg))
# print("Median:", np.median(dAg))
# print("SD:", np.std(dAg, ddof=1))
# print("Minimum:", np.min(dAg))
# print("Maximum:", np.max(dAg))
# print("Skewness:", skew(dAg))


# Generate the complete dataset by combining all the generated datasets into a single dataframe
batch_ids = [f"B{i:03d}" for i in range(1, 51)]
df = pd.DataFrame({
    "Batch_ID": batch_ids,
    "HCP_ng_mL": hcp,
    "HCD_ng_mL": hcd,
    "BCA_ug_mL": bca,
    "D-Ag_DU_mL": dAg
})
# print(df.head())
# print(df.shape)

# Intentionally create the outliers in the dataset to test the OOS detection
df.loc[7, "HCP_ng_mL"] = 158.987
df.loc[13, "HCP_ng_mL"] = 0.587

df.loc[14, "HCD_ng_mL"] = 1100
df.loc[21, "HCD_ng_mL"] = 1042

df.loc[28, "BCA_ug_mL"] = 800.876
df.loc[43, "BCA_ug_mL"] = 780
df.loc[48, "BCA_ug_mL"] = 760

df.loc[6, "D-Ag_DU_mL"] = 0.0567
df.loc[20, "D-Ag_DU_mL"] = 4.30

# Now let's create the column that showing the pass or OSS for the specific assay based
# on the acceptance criteria
df["HCP_Status"] = np.where(
    df["HCP_ng_mL"].between(1.06, 124.31),
    "Pass",
    "OOS"
)

df["HCD_Status"] = np.where(
    df["HCD_ng_mL"].between(5, 1000),
    "Pass",
    "OOS"
)

df["BCA_Status"] = np.where(
    df["BCA_ug_mL"].between(0, 750),
    "Pass",
    "OOS"
)

df["D_Ag_Status"] = np.where(
    df["D-Ag_DU_mL"].between(0.13, 4.00),
    "Pass",
    "OOS"
)
# Now create the overall status column based on the individual assay status
status_columns = [
    "HCP_Status",
    "HCD_Status",
    "BCA_Status",
    "D_Ag_Status"
]

df["Overall_Status"] = np.where(
    (df[status_columns] == "Pass").all(axis=1),
    "Pass",
    "Review"
)
print(df.head())
print(df["Overall_Status"].value_counts())

# Poping out the outliers from the dataset
review_batches = df[df["Overall_Status"] == "Review"]

print(review_batches[
    [
        "Batch_ID",
        "HCP_ng_mL",
        "HCD_ng_mL",
        "BCA_ug_mL",
        "D-Ag_DU_mL",
        "HCP_Status",
        "HCD_Status",
        "BCA_Status",
        "D_Ag_Status",
        "Overall_Status"
    ]
])

# Now let's do the descriptive statistics for the dataset to evaluate the generated dataset


# Now anayse the HCD_ng_mL column


# BCA_ug_mL column
bca_stats = df["BCA_ug_mL"].describe()
bca_skewness = df["BCA_ug_mL"].skew()
print(bca_stats)
print("BCA Skewness:", bca_skewness)


# Now the D-Ag_DU_mL column
dAg_stats = df["D-Ag_DU_mL"].describe()
dAg_skewness = df["D-Ag_DU_mL"].skew()
print(dAg_stats)
print("D-Ag Skewness:", dAg_skewness)


# Now let's calculate the coefficient of variation (CV) for each assay to evaluate the variability of the generated dataset
cv_Hcp = (df["HCP_ng_mL"].std() / df["HCP_ng_mL"].mean()) * 100
cv_Hcd = (df["HCD_ng_mL"].std() / df["HCD_ng_mL"].mean()) * 100
cv_Bca = (df["BCA_ug_mL"].std() / df["BCA_ug_mL"].mean()) * 100
cv_DAg = (df["D-Ag_DU_mL"].std() / df["D-Ag_DU_mL"].mean()) * 100
print(cv_Hcp, cv_Hcd, cv_Bca, cv_DAg)

# now the specification/OOS analysis for each assay to evaluate the generated dataset
oos_Counts = {
    "oos_Hcp": (df["HCP_Status"] == "OOS").sum(),
    "oos_Hcd": (df["HCD_Status"] == "OOS").sum(),
    "oos_Bca": (df["BCA_Status"] == "OOS").sum(),
    "oos_DAg": (df["D_Ag_Status"] == "OOS").sum()
}

print(oos_Counts)

# create a loop to display the OOS percentage for each assay
total_Count = len(df)
if total_Count > 0:
    for assay, oos_count in oos_Counts.items():
        oos_Percentage = (oos_count / total_Count) * 100
        print(f"{assay} Percentage of all batches: {oos_Percentage: .2f} %")
else:
    print("No data available to calculate OOS percentage.")


# Now calculate the OOS percentage for the overall status
review_Batch_Count = (df["Overall_Status"] == "Review").sum()
oos_Percentage = (review_Batch_Count / total_Count) * 100
print(
    f"Overall Percentage of OOS batches out of all batches: {oos_Percentage: .2f} %")
# Calculating the oos percentage for each assay to evaluate the generated dataset
for assay, oos_count in oos_Counts.items():
    oos_percentage_Assay = (oos_count / review_Batch_Count) * 100
    print(f"{assay}  Percentage out of total review batches: {oos_percentage_Assay:.2f}%")

# Now let's do the statistical outlier analysis for each assay to evaluate the generated dataset

outlier_Array = {
    "HCP": df["HCP_ng_mL"],
    "HCD": df["HCD_ng_mL"],
    "BCA": df["BCA_ug_mL"],
    "D-Ag": df["D-Ag_DU_mL"]
}

# Now create the fuction to find the outliers using the IQR method


def find_Outliers_IQR(data):
    Q1 = np.percentile(data, 25)
    Q3 = np.percentile(data, 75)
    IQR = Q3 - Q1
    # Lower bound and upper bound for outliers
    lower_Bound = Q1 - (1.5 * IQR)
    upper_Bound = Q3 + (1.5 * IQR)
    outliers = data[(data < lower_Bound) | (data > upper_Bound)]
    return outliers


# first create a empty dictonary to store the outliers for each assay
final_outliers = {}

# Now create a loop to find the outliers for each assay using the IQR method
# Hera the assay key and the data is the value for the specific key. so we assiging the key value from the
# oulier_array to the empty dictonary we created and we are passing the actua value to the fuction
#  we had created to calculate the outliers using the IQR method and we are storing the
# result in the final_outliers dictonary with the same key as the assay key.
for assay, data in outlier_Array.items():
    final_outliers[assay] = find_Outliers_IQR(data)
# printing the final outliers for each assay
for assay, outliers in final_outliers.items():
    print(f"\n{assay}")
    print("-" * 30)
    print(outliers)

# Now create the separate columns for the outliers for each assay in the dataframe and
# assign the outlier values to the specific column create an empty list
outlier_List = []
for assay, outlier in final_outliers.items():
    for index, value in outlier.items():
        outlier_List.append({
            "Batch_Id": df.loc[index, "Batch_ID"],
            "Assay": assay,
            "Value": value
        })

# create that into the dataframe
outlier_Dataframe = pd.DataFrame(outlier_List)

print(outlier_Dataframe)

# Now create a specification dictonary
specification = {
    "HCP": (1.06, 124.31),
    "HCD": (5, 1000),
    "BCA": (0, 750),
    "D-Ag": (0.13, 4.00)
}

# Create the fuction to check the specification status for the outlier values


def create_Specification(assay, value):
    lower_Limit, upper_Limit = specification[assay]
    if lower_Limit <= value <= upper_Limit:
        return "Pass"
    else:
        return "OOS"


# Now apply this to the outlier dataframe
outlier_Dataframe["Specification_Status"] = outlier_Dataframe.apply(
    lambda row: create_Specification(row["Assay"], row["Value"]),
    axis=1
)
print(outlier_Dataframe)

outlier_Dataframe.to_excel("Outlier.xlsx", sheet_name="outlier", index=False)
# Now create the assay-wise statistical summary

summary = []

# craete the assay to column mapping
assays = {
    "HCP": "HCP_ng_mL",
    "HCD": "HCD_ng_mL",
    "BCA": "BCA_ug_mL",
    "D-Ag": "D-Ag_DU_mL"
}

# Now create a loop to iterate through all the for assay colun in the original dataset

for assay, cloumn in assays.items():
    data = df[cloumn]
    mean = data.mean()
    median = data.median()
    sd = data.std()
    cv = (sd/mean) * 100
    minimum = data.min()
    maximum = data.max()
    q1 = data.quantile(0.25)
    q2 = data.quantile(0.75)
    skewness = data.skew()
    # now create the table data from this
    summary.append({
        "Assay": assay,
        "Mean": mean,
        "Median": median,
        "SD": sd,
        "CV%": cv,
        "Minimum_Value": minimum,
        "Maximum_Value": maximum,
        "Q1": q1,
        "Q2": q2,
        "Skewness": skewness
    })

statistical_Summary = pd.DataFrame(summary)
print(statistical_Summary)
statistical_Summary.to_excel(
    "Summary.xlsx", sheet_name="statistical summary", index=False)


# Now do the distribution analysis using histogram plot first
# let's create the reusable function
out_Put_Folder = "Plots"
os.makedirs(out_Put_Folder, exist_ok=True)

for assays, columns in assays.items():
    data = df[columns]
    plt.figure(figsize=(8, 5))
    sns.histplot(
        x=data,
        bins=10,
        kde=True
    )
    plt.xlabel(f"{assays}")
    plt.ylabel("Frequency")
    plt.title(f"Distribution of {assays} assay reults")
    plot_Name = f"{assays}.png"
    file_Path = os.path.join(out_Put_Folder, plot_Name)
    plt.savefig(
        file_Path,
        dpi=300,
        bbox_inches="tight",
        transparent=True)
    plt.close()

# Now create the box plot to connect with th IQR

limits = {
    "HCP_ng_mL": (1.06, 124.31),
    "HCD_ng_mL": (5, 1000),
    "BCA_ug_mL": (0, 750),
    "D-Ag_DU_mL": (0.13, 4.00)
}

for assays, specification in limits.items():
    data = df[assays]
    plt.figure(figsize=(8, 5))
    sns.boxplot(
        y=data
    )
    lower, upper = specification
    plt.axhline(
        lower,
        color="Green",
        linestyle="--",
        label="Lower Specification Limit"
    )
    plt.axhline(
        upper,
        color="Red",
        linestyle="--",
        label="Upper Specification Limit"
    )
    # plt.axhspan(
    #     ymin=1.06,
    #     ymax=124.31,
    #     color="BLue",
    #     alpha=0.15,
    #     label="Acceptable range"
    # )
    plot_Name2 = f"{assays} boxplot.png"
    file_Path2 = os.path.join(out_Put_Folder, plot_Name2)
    plt.ylabel(f"{assays}")
    plt.title(f"Box plot for {assays} assay results")
    plt.legend()
    plt.savefig(file_Path2,
                dpi=300,
                bbox_inches="tight",
                transparent=True
                )
    plt.close()
# Added the specification criteria to show the Distribution + Specification outliers + Specification limits unpack the values inside the spcification dictonary
# take out the final 2 numbers from the baych id
# batch_Id = df["Batch_ID"].astype(str).str.extract(r"(..)$") or
batch_Id = df["Batch_ID"].apply(lambda x: str(x)[-2:])
plt.figure(figsize=(15, 8))
sns.stripplot(
    data=df,
    x=batch_Id,
    y="HCP_ng_mL"
)
# plt.show()

# Now let's calculate the correlation of the assays
correlation_Matrix = df[[
    "HCP_ng_mL", "HCD_ng_mL", "BCA_ug_mL", "D-Ag_DU_mL"
]].corr()

print(correlation_Matrix)

# Noe create tje heatmap to visully see the correlation
plt.figure(figsize=(8, 6))

sns.heatmap(
    correlation_Matrix,
    annot=True,
    fmt=".2f"
)
plt.title("Correlation Matrix of Assay Results")
plt.tight_layout()
# plt.show()


# Create the final dataframe
df_Columns = [
    "Batch_ID",
    "HCP_ng_mL",
    "HCP_Status",
    "HCD_ng_mL",
    "HCD_Status",
    "BCA_ug_mL",
    "BCA_Status",
    "D-Ag_DU_mL",
    "D_Ag_Status",
    "Overall_Status"
]
final_Df = df[df_Columns].copy()
print(final_Df.head())
df.to_csv("final_Dataset", sep="\t", index=False)
df.to_excel("final_Dataset.xlsx", sheet_name="Main sheet", index=False)
