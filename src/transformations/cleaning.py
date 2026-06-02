from pyspark.sql import DataFrame
from pyspark.sql.functions import col, when


def drop_high_null_columns(df: DataFrame) -> DataFrame:
    """Remove columns with too many missing values."""
    return df.drop("weight", "payer_code")


def replace_interrogation_marks(df: DataFrame) -> DataFrame:
    """Replace '?' with 'Unknown' in string columns."""
    columns = ["race", "medical_specialty", "diag_1", "diag_2", "diag_3"]
    for column in columns:
        df = df.replace("?", "Unknown", subset=[column])
    return df


def remove_invalid_gender(df: DataFrame) -> DataFrame:
    """Remove rows with invalid gender values."""
    return df.filter(col("gender") != "Unknown/Invalid")


def create_readmission_flag(df: DataFrame) -> DataFrame:
    """Create binary target column: 1 if readmitted in <30 days, 0 otherwise."""
    return df.withColumn(
        "readmitted_flag",
        when(col("readmitted") == "<30", 1).otherwise(0)
    )


def clean(df: DataFrame) -> DataFrame:
    """Apply full cleaning pipeline."""
    df = drop_high_null_columns(df)
    df = replace_interrogation_marks(df)
    df = remove_invalid_gender(df)
    df = create_readmission_flag(df)
    return df